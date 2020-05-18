@echo off
:forevery_loop
set cur_path="%cd%\py_cpp_to_html.py"
python %cur_path%
pause
goto forevery_loop