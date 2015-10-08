@echo off
echo ----------------------------------------------
echo.
echo FIRMWARE UPLOADER FOR BCN3D ELECTRONICS
echo.
echo ----------------------------------------------
echo. 
echo.

:loop
 
echo Select between uploading the firmware or burning the Bootloader. 
echo "F" means Firmware and "B" means Bootloader.
echo. 
SET /P function=Enter your option: 
echo.

CD /d %~dp0

IF "%function%"=="F" (
	echo F detected! Firmware it is!
	echo.
	CALL :uploadFirmware
)

IF "%function%"=="B" (
	echo B detected! Bootloader it is!
	echo.
	CALL :burnBootloader
)


echo ------------------------
echo.
echo        finished
echo.
echo ------------------------
cls

goto loop

:: The function to upload the firmware to the board
:uploadFirmware
mode | findstr "COM*"
SET /P comPort=Please select the com port of the Board: 
echo.
echo UPLOADING THE FIRMWARE...
avrdude -p m2560 -c avrispmkII -P com%comPort% -D -U flash:w:Marlin.hex
::avrdude -p m2560 -c avrispmkII -P com%comPort% -U eeprom:w:Marlin.eep
echo.
PAUSE
cls
CALL :loop


::The funtion that burns the bootloader and sets the fuses
:burnBootloader
echo Please be sure to connect the AVRISP mkII programmer first!
echo.
PAUSE

echo SETTING THE CHIP FUSES...
avrdude -c avrispmkII -p m2560 -P usb -u -U lfuse:w:0xFF:m -U hfuse:w:0xD8:m -U efuse:w:0xFD:m -v
echo.
echo CHIP FUSES DONE!
echo.
echo BURNING THE BOOTLOADER...
echo.
avrdude -p m2560 -c avrispmkII -P usb -U flash:w:stk500boot_v2_mega2560.hex:i -D
echo.
echo BOOTLOADER DONE! YOU CAN DISCONNECT THE PROGRAMMER...
PAUSE
cls
CALL :loop