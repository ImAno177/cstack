from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).resolve().parents[1] / 'scripts' / 'sync_upstream_skills.py'
spec = importlib.util.spec_from_file_location('sync_upstream_skills', MODULE_PATH)
sync = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(sync)


class UpstreamSyncTests(unittest.TestCase):
    def test_copy_failure_keeps_original(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'source'
            target = root / 'target'
            source.mkdir()
            target.mkdir()
            (source / 'SKILL.md').write_text('new', encoding='utf-8')
            (target / 'SKILL.md').write_text('old', encoding='utf-8')
            with patch.object(sync.shutil, 'copytree', side_effect=OSError('disk full')):
                with self.assertRaisesRegex(OSError, 'disk full'):
                    sync.replace_managed_path(source, target)
            self.assertEqual((target / 'SKILL.md').read_text(), 'old')

    def test_stage_rename_failure_restores_original(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'source'
            target = root / 'target'
            source.mkdir()
            target.mkdir()
            (source / 'SKILL.md').write_text('new', encoding='utf-8')
            (target / 'SKILL.md').write_text('old', encoding='utf-8')
            original_rename = Path.rename

            def rename(path, destination):
                if path.parent.name.startswith('.target-stage-'):
                    raise OSError('stage install failed')
                return original_rename(path, destination)

            with patch.object(Path, 'rename', rename):
                with self.assertRaisesRegex(OSError, 'stage install failed'):
                    sync.replace_managed_path(source, target)
            self.assertEqual((target / 'SKILL.md').read_text(), 'old')

    def test_write_then_check_lock_and_detect_tampering(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / 'skills' / 'hf-cli'
            target.mkdir(parents=True)
            (target / 'SKILL.md').write_text('safe', encoding='utf-8')
            upstream = {'name': 'hf-cli', 'repository': 'huggingface/skills', 'ref': 'main',
                        'path': 'skills/hf-cli', 'destination': 'skills/hf-cli'}
            record = {**sync.entry_identity(upstream), 'commit': 'a' * 40,
                      'sha256': sync.directory_sha256(target)}
            lock = root / '.cstack' / 'upstreams.lock.json'
            sync.atomic_write_json(lock, {'version': 1, 'skills': [record]})
            sync.verify_lock(root, [upstream], lock)
            (target / 'SKILL.md').write_text('tampered', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'content differs'):
                sync.verify_lock(root, [upstream], lock)

    def test_reject_path_traversal(self):
        entry = {'name': 'sample', 'repository': 'good/repo', 'path': '../secret',
                 'destination': 'skills/entry'}
        with self.assertRaisesRegex(ValueError, 'unsafe upstream path'):
            sync.validate_specs([entry])

    def test_reject_nested_destination(self):
        entry = {'name': 'sample', 'repository': 'good/repo', 'path': 'skills/sample',
                 'destination': 'skills/group/sample'}
        with self.assertRaisesRegex(ValueError, r'must be skills/<name>'):
            sync.validate_specs([entry])


if __name__ == '__main__':
    unittest.main()
