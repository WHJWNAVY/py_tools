@echo off
:start_qrcode
set cur_path="%cd%\py-get-qrcode.py"
python %cur_path%
rem pause
goto start_qrcode: