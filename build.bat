echo off
color 0A
cls
set FILE_NAME="ask_question"
set EXTENSION=".py"
set DEST_PATH="%HOMEDRIVE%\Users\%username%\AppData\Roaming\Python\Python310\site-packages\"
set SRC_PATH="C:\Users\Henry_PC\AppData\Roaming\Python\Python310\Scripts\"
echo "building ..."
py setup.py bdist_wheel
echo "built"
echo "installing ..."
pip install dist\ask_question-1.0.0-py3-none-any.whl
echo "Installed"
echo "Copying %FILE_NAME%%EXTENSION% to '%DEST_PATH%'"
copy "%SRC_PATH%\%FILE_NAME%%EXTENSION%" "%DEST_PATH%"
echo "Listing python files"
dir "%DEST_PATH%\*.py"
echo "file copied"
echo "updating pip's cache"
pip list
echo "pip's cache has been updated"
echo "Running the python terminal"
echo "please type: import %FILE_NAME%"
echo "the filename is: %FILE_NAME%%EXTENSION%"
echo "once finished, type: exit() to exit the python interpreter"
py
echo "python terminal - ended"
echo "uninstalling the package %FILE_NAME%"
pip uninstall %FILE_NAME%
echo "package uninstalled"
echo "removing %FILE_NAME%%EXTENSION% from %DEST_PATH%"
del /Q %DEST_PATH%\%FILE_NAME%%EXTENSION%
echo "file removed"
