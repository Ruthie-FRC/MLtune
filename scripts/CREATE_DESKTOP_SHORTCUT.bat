@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM  Creates a shortcut on your Desktop to launch MLtune
REM  Run this once, then just double-click the shortcut on your Desktop!
REM ═══════════════════════════════════════════════════════════════════════════

echo Creating Desktop shortcut for MLtune...

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Create a shortcut on the Desktop
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%USERPROFILE%\Desktop\MLtune.lnk'); $s.TargetPath = '%SCRIPT_DIR%START.bat'; $s.WorkingDirectory = '%SCRIPT_DIR%'; $s.Description = 'Launch MLtune Unified Launcher'; $s.Save()"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ════════════════════════════════════════════════════════════════════════
    echo   SUCCESS! A shortcut called "MLtune" has been created on your Desktop.
    echo   Double-click it to launch MLtune!
    echo ════════════════════════════════════════════════════════════════════════
) else (
    echo.
    echo ERROR: Could not create shortcut. You can manually copy START.bat to your Desktop.
)

echo.
pause
