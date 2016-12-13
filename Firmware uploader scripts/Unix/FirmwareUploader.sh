#!/bin/bash

#BCN3D Technologies - Fundacio CIM
#Bash script for loading Bootloader and Firmware to BCN3D Electronics
#under UNIX machines.
#Marc Cobler Cosmen - October 2015

#Variables
OPTIONS="Bootloader Firmware Everything Update Exit"
FILESDIR=~/bcn3d-utilities/Firmware\ uploader\ scripts/Files
DIR=~/bcn3d-utilities/Firmware\ uploader\ scripts/Unix/
PACKAGES=(flex byacc bison gcc libusb-dev avr-libc avrdude setserial)
BOOTLOADER=BCN3D-stk500boot.hex
FIRMWARES = ""
STATUS = false
#User functions
function checkInternet {
	wget -q --tries=5 --timeout=20 --spider http://google.com
	if [[ $? -eq 0 ]]; then
    STATUS=true
		printf "System is ONLINE \n\n"
	fi
}

function checkInstalledPackages {
	#Look for needed packages
	for i in ${PACKAGES[*]}; do
		if dpkg-query --show $i; then
			printf "You have already $i installed \n\n"
		else
			printf "You don\'t have $i installed \n\n"
			printf "Do you want to "install" it? "[y/n]""
			read INSTALL
			if [ $INSTALL == "y" ]; then
				sudo apt-get install $i
			else
				printf "Program will not work properly. Please install the packages"
			fi
		fi
	done
	#clear
}

function updateGithub {
	#Update the repository from github
	#Pull from github the new changes
	printf "Do you want to download updates from Github? "[y/n]""
	read UPDATES
	if [ $UPDATES == "y" ]; then
		if [[ $STATUS == "true" ]]; then
			#connected to the internet
			git pull
		else
			#No internet
			printf "There's no internet connection...! \n Canceling sync"
		fi
	fi
}

function listFirmwares {
	FIRMWARES="$(ls ../Files | grep "Sigma*")"
	printf "Which firmware do you want to upload? \n"
	printf "Remember if you want to change the firmware you have to reboot script \n"
	#Let's print the options and select them
	select firmware in $FIRMWARES; do
		printf "The selected Firmware is: $firmware \n"
		break
	done
}

function comPorts {
	if [[ $(ls -lA /dev/ | grep ttyUSB*) ]]; then
		printf "These are the COM Ports available:"
		ls -lA /dev/ | grep ttyUSB*
		printf "Select your COM Port: [Number]"
		read COMPORT

	else
		printf "There is no Board connected. Please verify and reconnect."
		menu
	fi
}

function loadFirmware {
  printf "Uploading the firmware..."
	cd ../Files
	if [ $1 -eq 0 ]; then
		avrdude -p m2560 -c avrispmkII -P /dev/ttyUSB$1 -D -U flash:w:$firmware:i
	else
		comPorts
		avrdude -p m2560 -c avrispmkII -P /dev/ttyUSB$COMPORT -D -U flash:w:$firmware:i
	fi
	#return to menu
	menu
}

function loadBootloader {
	cd ../Files
  printf "Please make sure that the programmmer is connected! \n\n"
	printf "SETTING THE CHIP FUSES... \n"
	avrdude -c avrispmkII -p m2560 -P usb -u -U lfuse:w:0xFF:m -U hfuse:w:0xD8:m -U efuse:w:0xFD:m -v
	printf "BURNING THE BOOTLOADER... \n"
	avrdude -c avrispmkII -p m2560 -P usb -u -U flash:w:$BOOTLOADER:i
	#return to menu
	menu
}

function menu {
	printf "\n"
	#we're going to run a Select to make a simple menu
	select opt in $OPTIONS; do
		if [ "$opt" = "Firmware" ]; then
			printf "Firmware it is! \n"
			#Now we're going to load the firmware
			loadFirmware
			sleep 2
		elif [ "$opt" = "Bootloader" ]; then
			printf "Bootloader it is! \n"
			#Now we're going to load the Bootloader
			loadBootloader
			sleep 2
		elif [ "$opt" = "Exit" ]; then
			printf "Bye! see you soon \n\n"
			sleep 1
			clear
			exit
		elif [ "$opt" = "Everything" ]; then
			loadBootloader
			loadFirmware 0
			menu
		elif [ "$opt" = "Update" ]; then
			#Update the Github Repository. Only if there's internet
			updateGithub
			menu
		else
			printf "Please, enter a valid option! \n"
		fi
done
}

#----------------------------------------------------------------
#										MAIN LOOP
#----------------------------------------------------------------
clear
printf "============================================================"
printf "\n\n"
printf "FIRMWARE UPLOADER FOR BCN3D ELECTRONICS"
printf "\n\n"
printf "============================================================"
printf "\n"
checkInternet
checkInstalledPackages
#List the available firmwares and select it
listFirmwares
#show the menu
menu
