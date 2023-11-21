@echo off
echo creating exe...
pyinstaller teethpack.py --onefile --noupx
if %errorlevel% neq 0 exit /b %errorlevel%
echo packing...
tar -acvf dist/teethpack.zip ^
    README ^
    LICENSE ^
    teethpack.bat ^
    dist/teethpack.exe ^
    drophere/info.txt ^
    output/info.txt
if %errorlevel% neq 0 exit /b %errorlevel%
echo done.
pause
