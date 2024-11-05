@echo off
setlocal enabledelayedexpansion

:: fetch date and time
set "timestamp=%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%"

:: create the folder
set "logfolder=%CD%\output\Logs\Log_%timestamp%"
mkdir "!logfolder!"

CALL C:\ProgramData\anaconda3\condabin\activate.bat aquaman

FOR /L %%i IN (1,1,40) DO (
   python YOLO2CSV.py %%i | tee "!logfolder!\log_%%i.txt"
)

pause
