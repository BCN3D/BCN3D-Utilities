#!/bin/bash

#BCN3D Technologies - Fundacio CIM
#Bash script for loading Bootloader and Firmware to BCN3D Electronics
#under UNIX machines.
#Marc Cobler Cosmen - October 2015

#Variables
OPTIONS="Firmware Bootloader Exit"
FILE="Marlin.hex"
DIR=~/bcn3d-utilities/Firmware\ uploader\ scripts/Unix/
PACKAGES=(avrdude)

#User functions
function start {
	#Look for needed packages
	for i in ${PACKAGES[*]}; do
		if dpkg-query -W $i; then
			echo You have already $i installed
		else
			echo You don\'t have $i installed
			echo -e Do you want to "install" it? "[y/n]"
			read INSTALL
			if [ $INSTALL == "y" ]; then
				echo `sudo apt-get install $i`
			else
				echo Program will not work properly. Please "install" the packages
			fi	
		fi
	done
	#Pull from github the new changes
	echo -e Do you want to download updates from Github? "[y/n]"
	read UPDATES
	if [ $UPDATES == "y" ]; then
		git pull
	fi
}

function comPorts {
	if [[ $(ls -lA /dev/ | grep ttyUSB*) ]]; then
		echo These are the COM Ports available:
		ls -lA /dev/ | grep ttyUSB*
		echo -e "Select your COM Port: [Number]"
		read COMPORT
		
	else
		echo There is no Board connected. Please verify and reconnect.
		menu
	fi
}

function loadFirmware {
        echo Uploading the firmware...
	comPorts
	avrdude -p m2560 -c avrispmkII -P /dev/ttyUSB$COMPORT -D -U flash:w:$FILE:i
	
	#return to menu
	menu
}

function loadBootloader {
        echo Please make sure that the programmmer AVRISPmkII is connected!
        echo Uploading the Bootloader
	
	#return to menu
	menu
}

function menu {
	#we're going to run a Select to make a simple menu
	select opt in $OPTIONS; do
		if [ "$opt" = "Firmware" ]; then
			echo F detected, Firmware it is!
			#Now we're going to load the firmware
			loadFirmware
			sleep 2
		elif [ "$opt" = "Bootloader" ]; then
			echo B detected, Bootloader it is!
			#Now we're going to load the Bootloader
			loadBootloader
			sleep 2
		elif [ "$opt" = "Exit" ]; then
			echo Bye! see you soon
			sleep 1
			exit
		else
			echo Please, enter a valid option! Select the numbers
		fi
done
}


clear
start
echo -------------------------------------------------------------
echo -e "\n"
echo FIRMWARE UPLOADER FOR BCN3D ELECTRONICS
echo -e "\n"
echo ------------------------------------------------------------

echo -e "\n"
echo Select between uploading the firmware or burning the bootloader.
echo -e Press "Q" to "exit" the program.
menu

