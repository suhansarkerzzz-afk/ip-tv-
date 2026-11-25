@echo off
setlocal
title Build IPTV Channel Extractor Pro
py -3 -m pip install pyinstaller requests
py -3 -m PyInstaller --noconfirm --clean --onefile --windowed --name IPTV_Channel_Extractor_Pro main.py
echo.
echo EXE created in the dist folder.
pause
