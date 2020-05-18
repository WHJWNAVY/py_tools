@echo off
set pkgname=
set /p pkgname=Input Package Name:
set inscmd=pip install -i https://pypi.douban.com/simple/ %pkgname%
echo %inscmd%
%inscmd%
pause