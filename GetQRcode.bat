@echo off
:while_loop
set cur_path="%cd%\py-get-qrcode.py"
python %cur_path%
goto while_loop
pause