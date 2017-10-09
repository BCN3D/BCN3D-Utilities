#!/bin/bash

#BCN3D Technologies - Fundacio CIM
#Bash script for loading Bootloader and Firmware to BCN3D Electronics
#under UNIX machines.
#Marc Cobler Cosmen - October 2015

#Variables
OPTIONS="Firmware-Sigma Firmware-Sigmax Bootloader Everything-Sigma Everything-Sigmax Update TestCommunication Exit"
FILESDIR=~/bcn3d-utilities/Firmware\ uploader\ scripts/Files
DIR=~/bcn3d-utilities/Firmware\ uploader\ scripts/Unix/
#File where the packages needed are listed
PACKAGES="./Packages.list"
BOOTLOADER="BCN3D-stk500boot.hex"
FIRMWARES=""
STATUS=false
defaultComPort=0

#User functions
function checkInternet {
	wget -q --tries=5 --timeout=20 --spider http://google.com
	if [[ $? -eq 0 ]]; then
    STATUS=true
		printf "System is ONLINE \n\n"
	fi
}

function checkInstalledPackages {
	#Look for needed packages and install them if needed
	while IFS= read -re package
	do
		if dpkg-query --show $package; then
			printf "You have already $package installed \n\n"
	 	else
			printf "You don\'t have $package installed \n\n"
			printf "Do you want to "install" it? "
			read -p "[y/n] : " INSTALL < /dev/tty
			if [ $INSTALL == "y" ]; then
				sudo apt-get -qq -y install $package
		 	else
				printf "Program will not work properly. Please install the packages \n"
		 	fi
	 fi
 done < $PACKAGES
}

function updateGithub {
	#Update the repository from github
	#Pull from github the new changes
	printf "Do you want to download updates from Github? "
	read -p "[y/n] : " UPDATES
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

function listFirmwaresigma {
	FIRMWARES="$(ls ../Files | grep "Sigma*")"
	printf "Which firmware Sigma do you want to upload? \n"
	printf "Remember if you want to change the firmware you have to reboot script \n\n"
	#Let's print the options and select them
	select firmware in $FIRMWARES; do
		printf "The selected Firmware is: $firmware \n"
		break
	done
}
 
function listFirmwaresigmax {
	FIRMWARES="$(ls ../Files | grep "sigmaX*")"
	printf "Which firmware Sigmax do you want to upload? \n"
	printf "Remember if you want to change the firmware you have to reboot script \n\n"
	#Let's print the options and select them
	select firmwaresigmax in $FIRMWARES; do
		printf "The selected Firmware is: $firmwaresigmax \n"
		break
	done
}

function comPorts {
	if [[ $(ls -lA /dev/ | grep ttyUSB*) ]]; then
		printf "These are the COM Ports available: \n"
		ls -lA /dev/ | grep ttyUSB*
		printf "Select your COM Port: "
		read -p "[Number] : " COMPORT

	else
		printf "There is no Board connected. Please verify and reconnect."
		menu
	fi
}

function loadFirmware {
  printf "Uploading the firmware..."
	cd ../Files
	#check if parameter 1 is zero length. Then select the com port
	if [ -z "$1" ]; then
		comPorts
		sudo avrdude -p m2560 -c avrispmkII -P /dev/ttyUSB$COMPORT -D -U flash:w:$firmware:i
	else #The comport is passed by default as 0
		printf "USING DEFAULT COMPORT "
		printf "%s\n" "$1"
		sudo avrdude -p m2560 -c avrispmkII -P /dev/ttyUSB$1 -D -U flash:w:$firmware:i
	fi
}

function loadFirmwareSigmax {
  printf "Uploading the firmware..."
	cd ../Files
	#check if parameter 1 is zero length. Then select the com port
	if [ -z "$1" ]; then
		comPorts
		sudo avrdude -p m2560 -c avrispmkII -P /dev/ttyUSB$COMPORT -D -U flash:w:$firmwaresigmax:i
	else #The comport is passed by default as 0
		printf "USING DEFAULT COMPORT "
		printf "%s\n" "$1"
		sudo avrdude -p m2560 -c avrispmkII -P /dev/ttyUSB$1 -D -U flash:w:$firmwaresigmax:i
	fi
}

function loadBootloader {
	cd ../Files
	printf "Please make sure that the programmmer is connected! \n\n"
	printf "SETTING THE CHIP FUSES... \n"
	sudo avrdude -c avrispmkII -p m2560 -P usb -u -U lfuse:w:0xFF:m -U hfuse:w:0xD8:m -U efuse:w:0xFD:m -v
	printf "BURNING THE BOOTLOADER... \n"
	sudo avrdude -c avrispmkII -p m2560 -P usb -u -U flash:w:$BOOTLOADER:i
}

function testCommunication {
	sudo avrdude -c avrispmkII -p m2560 -P usb -vvvv
}

function printHeader {
	printf "============================================================"
	printf "\n\n"
	printf "FIRMWARE UPLOADER FOR BCN3D ELECTRONICS"
	printf "\n\n"
	printf "============================================================"
	printf "\n"
}

function menu {
	printHeader
	#printf "\n"
	#we're going to run a Select to make a simple menu
	select opt in $OPTIONS; do
		if [ "$opt" = "Firmware-Sigma" ]; then
			printf "Firmware Sigma it is! \n"
			#Now we're going to load the firmware
			loadFirmware
			sleep 2
			menu
		elif [ "$opt" = "Firmware-Sigmax" ]; then
			printf "Firmware Sigmax it is! \n"
			#Now we're going to load the firmware
			loadFirmwareSigmax
			sleep 2
			menu
		elif [ "$opt" = "Bootloader" ]; then
			printf "Bootloader it is! \n"
			#Now we're going to load the Bootloader
			loadBootloader
			sleep 2
			menu		
		elif [ "$opt" = "Everything-Sigma" ]; then
			loadBootloader
			sleep 2
			loadFirmware $defaultComPort
			menu
		elif [ "$opt" = "Everything-Sigmax" ]; then
			loadBootloader
			sleep 2
			loadFirmwareSigmax $defaultComPort
			menu
		elif [ "$opt" = "Update" ]; then
			#Update the Github Repository. Only if there's internet
			updateGithub
			menu
		elif [ "$opt" = "TestCommunication" ]; then
			#Test the connection with the programmer and the board
			testCommunication
			menu
		elif [ "$opt" = "Exit" ]; then
			printf "Bye! see you soon \n\n"
			sleep 1
			clear
			exit
		else
			printf "Please, enter a valid option! \n"
		fi
done
}

#----------------------------------------------------------------
#										MAIN LOOP
#----------------------------------------------------------------
clear
checkInternet
checkInstalledPackages
#List the available firmwares and select it
listFirmwaresigma
listFirmwaresigmax
#show the menu
menu
