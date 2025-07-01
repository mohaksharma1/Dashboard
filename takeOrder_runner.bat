@echo off
:run_script
START "" /B python "splash/view.py"
RMDIR /S /Q Dashboard
C:\Users\mohak\AppData\Local\BraveSoftware\Brave-Browser\Application\chrome_proxy.exe  --profile-directory=Default --app-id=dpckklemgligkjpihmopkkknllapmclp
python "src/takeOrder.py"
IF %ERRORLEVEL% EQU 1 (
    echo Script returned code 1, rerunning...
    goto run_script
) ELSE (
    echo Script exited with code %ERRORLEVEL%, stopping.
)


