param(
    [string]$Source = (Join-Path $env:USERPROFILE '.agents\skills'),
    [string]$Repo = (Get-Location).Path,
    [int]$DebounceMilliseconds = 800
)

$sourcePath = (Resolve-Path -LiteralPath $Source).Path
$repoPath = (Resolve-Path -LiteralPath $Repo).Path
$syncScript = Join-Path $repoPath 'scripts\sync_skills.py'
$buildScript = Join-Path $repoPath 'scripts\build_plugin.py'
$watcher = [IO.FileSystemWatcher]::new($sourcePath)
$watcher.IncludeSubdirectories = $true
$watcher.NotifyFilter = [IO.NotifyFilters]::FileName -bor [IO.NotifyFilters]::LastWrite -bor [IO.NotifyFilters]::DirectoryName

Write-Output "watching $sourcePath"
Write-Output "publishing to $repoPath"

while ($true) {
    $change = $watcher.WaitForChanged([IO.WatcherChangeTypes]::All, 2000)
    if ($change.TimedOut) {
        continue
    }
    Start-Sleep -Milliseconds $DebounceMilliseconds
    do {
        $change = $watcher.WaitForChanged([IO.WatcherChangeTypes]::All, 150)
    } while (-not $change.TimedOut)
    python $syncScript --source $sourcePath --destination (Join-Path $repoPath 'source\local\skills')
    if ($LASTEXITCODE -ne 0) { throw 'local skill sync failed' }
    python $buildScript --source-root (Join-Path $repoPath 'source') --destination (Join-Path $repoPath 'plugins\cstack\skills')
    if ($LASTEXITCODE -ne 0) { throw 'plugin build failed' }
    git -C $repoPath add -- source/local plugins/cstack/skills
    git -C $repoPath diff --cached --quiet
    if ($LASTEXITCODE -ne 0) {
        git -C $repoPath commit -m 'sync local skills'
        git -C $repoPath push
    }
}
