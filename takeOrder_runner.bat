@echo off
:run_script
RMDIR /S /Q Dashboard
python "src/takeOrder.py"
IF %ERRORLEVEL% EQU 1 (
    echo Script returned code 1, rerunning...
    goto run_script
) ELSE (
    echo Script exited with code %ERRORLEVEL%, stopping.
)


