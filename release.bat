set NAME=pyfscc
set VERSION=1.0.0
set DIR_NAME=%NAME%-%VERSION%
set ZIP_NAME=%NAME%-windows-%VERSION%
set BIN_DIR=bin
set TOP=%BIN_DIR%\%NAME%-%VERSION%

echo off

rmdir /S /Q %BIN_DIR% 2> nul

:setup_directories
echo Creating Directories...
mkdir %TOP%\
for %%A in (docs, examples) do mkdir %TOP%\%%A

:build_library
echo Building Library...
python setup.py build

:copy_files
echo Copying Release Files...
copy dist\%NAME%-%VERSION%.win32.exe %TOP%\ > nul

:copy_extras
echo Copying Extra Files...
copy docs\*.md %TOP%\docs\
copy examples\*.py %TOP%\examples\ > nul

:copy_changelog
echo Copying ChangeLog...
copy ChangeLog.md %TOP%\ > nul

:copy_readme
echo Copying README...
copy README.md %TOP%\ > nul

:zip_packages
echo Zipping Drivers...
cd %TOP%\ > nul
cd ..\ > nul
..\7za.exe a -tzip %ZIP_NAME%.zip %DIR_NAME% > nul
cd ..\ > nul