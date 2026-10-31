from pathlib import Path


TEST_DIRECTORIES = {"test", "tests", "__tests__"}


def ignore_test_artifacts(directory: str, names: list[str]) -> list[str]:
    ignored = []
    for name in names:
        path = Path(directory) / name
        if path.is_dir() and name.lower() in TEST_DIRECTORIES:
            ignored.append(name)
        elif path.is_file() and (".test." in name.lower() or ".spec." in name.lower() or ".test-helper." in name.lower()):
            ignored.append(name)
    return ignored
