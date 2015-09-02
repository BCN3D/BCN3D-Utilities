#!/usr/bin/python

#BCN3D Technologies 
#Marc Cobler Cosmen - May 2015
#Licensed under MIT license. 



import sys 
import re
import os 
import urllib
import serial
import glob


#Now some information about the program itself

"""This program checks both the latest firmware version on the BCN3D Technologies Repository 
and the firmware installed on the printer. It let's you update your 3D printer firmware on the fly
without the need of compiling and installing IDE's.

We need to be up to date to the code repository hosted on Github and a way to know the version of the firmware. 
The communication with the printer is done by serial via USB, so we'll need to open a port at the proper baudrate
and start commucating.

In order to get the latest source code from the repository, we'll use the Releases system by Github.
In that way we'll be able to pull the latest version available.


Suggested Milestones
- Been able to get the repository in Github and pull down the changes as the program runs time after time.
- Store the repository in some place in order to get the compiled file 
- Open a serial port and get data from it
- Parse the firmware version of the printer and compare it with the last one

"""

BAUDRATE = 250000

def matchInList(text, list):
#Returns a list of matching values in a specified list
	match = [s for s in list if text in s]
	return match


def getLatestVersion():
		#First we get the webpage and look for the last Release
	url = ('https://github.com/reprapbcn/BCN3D-Firmware/releases/')
	urlContent = urllib.urlopen(url)
	data = urlContent.read()
	#Let's store the latest version because it will be very useful in the future
	#Seraching for the first .zip string
	versionMatch = re.search(r'([\d.]+)\.(zip)', data)
	if not versionMatch:
		#We didn't get a version so an error ocurred. Get out with a message
		sys.stderr.write('Couldn\'t find the Latest Version!')
		sys.exit(1)
	global version = versionMatch.group(1)
	print 'The latest firmware version available is: ',version

def downloadLatestVersion(version,base_url):
	#Now that we have the version, we can retrieve it from the internet and save it in the
	#Versions directory. We need to create it if it doesn't exists.
	#First we need to contruct the url to retrieve the content
	version_url = base_url + version + '.zip'
	dir = 'Versions'
	if not os.path.exists(dir):
		os.mkdir(dir)

	#Get a list of files in the directory "Versions" and check if we're up to date.
	#If not, download the last version from the internet.		
	releases = os.listdir('./'+ dir)
	if (version + '.zip') in releases:
		print 'Repositories up to date!'
	else:
		print 'Downloading Version... ',version
		urllib.urlretrieve(version_url, os.path.join(dir, version + '.zip'))
		print 'Done downloading!'
		#Now we need to unzip it
		print 'Inflating files...'
		os.system('unzip -q ./' + version + '.zip')
		print 'Done unziping the files!'

def openSerialPort():
	#In this function we're going to open a serial port connection with the printer and listen
	#in the firts lines the printer will write it's firmware version so we can compare.
	#The functionality is provided by the PySerial module
	#We scan the serial ports so we can choose the right one

	#Need to implement the cross platform code for Win & Linux systems
	print 'Scanning Serial Ports...'
		ports = glob.glob('/dev/tty.*')
		for port in ports:
			print port +'\n',

		#Now we need to select the correct com port. It will be something like tty.usb...
		printer_port = matchInList('tty.usb', ports)[0]
		return serial.Serial(printer_port, BAUDRATE, timeout=5)


def getDataSerialPort():
	ser = openSerialPort()
	global serial_data = ser.readline()	#Until it finds a CR '\n'
	ser.close()

def printerNeedsUpdate():
	printer_version = re.search(r'([\d.]+)', serial_data)
	version_list = version.split('.')
	printer_version_list = printer_version.split('.')
	
	if printer_version_list[0] < version_list[0] or printer_version_list[1] < version_list[1] or printer_version_list[2] < version_list[2]
		needUpdate = True
	else 
		needUpdate = False

	return needUpdate

def runUpdate():
#In this function we're going to launch avrdude and upload the corresponding .hex file
#We can achieve that by doing os.system('command') or os.popen('command')


def checkavrdude():
##Let's check if the computer already has the avrdude program. If not give an advice
	avr_dir_mac = '/usr/local/'
	installations = glob.glob(avr_dir_mac + 'CrossPack-AVR*')

	if installations:
		return True
	else:
		return False


def main():
	base_url = 'https://github.com/reprapbcn/BCN3D-Firmware/archive/'
	getLatestVersion()
	downloadLatestVersion(version, base_url)
	getDataSerialPort()

	if printerNeedsUpdate():
		if checkavrdude():
			print 'You need to install avrdude! look for CrossPack-AVR for Mac OS'
		else:
		runUpdate()
		print 'Your printer is up to date now. Enjoy!'
	else:
		print 'Your printer is already up to date. Nothing to do...'


#Just the regular boilerplate to start the program
if __name__ == '__main__':
	main()