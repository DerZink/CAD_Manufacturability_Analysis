@echo off
echo ####################
echo start signing
set path_signExe="%UGII_BASE_DIR%\NXBIN\SignDotNet.exe"
echo NX signing EXE = %path_signExe%
set toolFolder=%~dp0
echo Tool folder = %toolFolder%
FOR %%I IN (%toolFolder%\*.exe) DO (
%path_signExe% %%I
) 
echo signing finished
echo ####################