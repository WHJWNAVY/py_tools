@echo off
:while_loop
set cur_path="%cd%\py_img_to_txt.py"
python %cur_path%
goto while_loop
pause