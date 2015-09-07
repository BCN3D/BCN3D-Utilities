@echo off
echo ----------------------------------------------
echo.
echo BOOTLOADER SCRIPT FOR 4D SYSTEMS DISPLAY
echo.
echo ----------------------------------------------
echo. 
echo.

echo This Script will upload the bootloader to the 4D Systems display
echo.

:loop

echo **************
 SET /P Choice = hit enter to begin...
IF "%Choice%"=="" scriptc LOADSIGMA /c comXX
scriptc LOADSIGMA /c com51

echo ----------------------------------------------
echo. 
echo 		FINISHED
echo.
echo ----------------------------------------------

cls

goto loop