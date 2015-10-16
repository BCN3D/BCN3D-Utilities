#!/bin/bash
#Variables
OPTIONS="Firmware Bootloader Exit"
clear
echo -------------------------------------------------------------
echo -e " \n"
echo FIRMWARE UPLOADER FOR BCN3D ELECTRONICS
echo -e "\n"
echo ------------------------------------------------------------

echo -e "\n"
echo Select between uploading the firmware or burning the bootloader.
echo -e Press "Q" to "exit" the program.

#we're going to run a Select to make a simple menu
select opt in $OPTIONS; do
	if [ "$opt" = "Firmware" ]; then
		echo F detected, Firmware it is!
		#Now we're going to load the firmware
		loadFirmware
	elif [ "$opt" = "Bootloader" ]; then
		echo B detected, Bootloader it is!
		#Now we're going to load the Bootloader
		loadBootloader
	elif [ "$opt" = "Exit" ]; then
		echo Bye! see you soon
		sleep 2
		exit
	else
		echo Please, enter a valid option! Select the numbers
	fi
done


#User functions
function loadFirmware {
	echo Uploading the firmware
}

function loadBootloader {
	echo Please make sure that the programmmer AVRISPmkII is connected!
	echo Uploading the Bootloader
}
