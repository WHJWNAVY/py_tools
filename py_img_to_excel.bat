@echo off
:start_qrcode
set cur_path="%cd%\py_img_to_excel.py"
python %cur_path%
rem pause
goto start_qrcode: