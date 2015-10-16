#!/bin/bash

echo -------------------------------------------------------------
echo -e " \n"
echo FIRMWARE UPLOADER FOR BCN3D ELECTRONICS
echo -e "\n"
echo ------------------------------------------------------------

echo -e "\n"
echo Select between uploading the firmware or burning the bootloader.
echo -e "F" means firmware and "B" means Bootloader.
echo -e Press "Q" to "exit" the program.

#until command is done when the expression is false
until [ $command Q]; do
	echo -e "Please, enter your option: \c "
	read command
	if [ $command = "F" ]; then
		echo F detected, Firmware it is!
		#Now we're going to load the firmware
	else if [ $command = "B" ]; then
		echo B detected, Bootloader it is!
		#Now we're going to load the Bootloader
	else
		echo Please, enter a valid option: F, B or Q to quit
	fi
	clear
done

#If we are here, it means we've read a Q --> quit program
echo Bye bye!

