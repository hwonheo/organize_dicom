@echo off
REM 파이썬이 설치되어 있는지 확인
python --version
IF %ERRORLEVEL% NEQ 0 (
    echo "Python is not installed. Please install Python from https://www.python.org/"
    pause
    exit /B
)

REM 필요한 패키지 설치
pip install pydicom

REM organize_dicom.py 스크립트 실행
python organize_dicom.py -b %1

pause
