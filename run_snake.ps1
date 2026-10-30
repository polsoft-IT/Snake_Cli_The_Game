<#
    Launches "Snake CLI.py" with a Python interpreter that can actually run it.

    Why: Python on Windows ships no curses module. It only exists here because
    `windows-curses` is pip-installed into Python 3.14. The 3.13 and 3.15
    installs on this machine do not have it, so `import curses` fails there
    with "No module named '_curses'".

    Usage:  .\run_snake.ps1
            .\run_snake.ps1 -PythonExe "C:\path\to\python.exe"
#>
param(
    [string]$PythonExe = "C:\Users\max\AppData\Local\Programs\Python\Python314\python.exe"
)

$ErrorActionPreference = "Stop"
$game = Join-Path $PSScriptRoot "Snake CLI.py"

if (-not (Test-Path $PythonExe)) {
    throw "Python interpreter not found: $PythonExe"
}

# Fail early with a clear message instead of a raw ModuleNotFoundError traceback.
& $PythonExe -c "import curses, _curses"
if ($LASTEXITCODE -ne 0) {
    throw "'$PythonExe' has no working curses module. Run: `"$PythonExe`" -m pip install windows-curses"
}

& $PythonExe $game
exit $LASTEXITCODE
