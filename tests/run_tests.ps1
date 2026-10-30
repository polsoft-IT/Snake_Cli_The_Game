<#
    Runs every test in this folder and prints the collected output.

    Usage:  .\tests\run_tests.ps1
            .\tests\run_tests.ps1 -PythonExe "C:\path\to\python.exe"

    Notes:
      * curses needs a real console, so the smoke test redirects its own output
        to tests\smoke_out.txt; that file is printed afterwards.
      * Only interpreters that have the curses module can run the smoke test.
#>
param(
    [string]$PythonExe = "C:\Users\max\AppData\Local\Programs\Python\Python314\python.exe"
)

$ErrorActionPreference = "Stop"
$tests = $PSScriptRoot
$log = Join-Path $tests "smoke_out.txt"

if (-not (Test-Path $PythonExe)) { throw "Python interpreter not found: $PythonExe" }

& $PythonExe -c "import curses, _curses"
if ($LASTEXITCODE -ne 0) { throw "'$PythonExe' has no curses module. Run: `"$PythonExe`" -m pip install windows-curses" }

Remove-Item $log -ErrorAction SilentlyContinue
& $PythonExe (Join-Path $tests "smoke_test_curses.py")
$exit = $LASTEXITCODE

if (Test-Path $log) {
    Get-Content $log
} else {
    Write-Output "smoke_test_curses.py produced no output (exit code $exit)."
}

exit $exit
