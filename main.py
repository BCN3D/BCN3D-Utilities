#!/usr/bin/python

#BCN3D Technologies 
#Marc Cobler Cosmen - May 2015
#Licensed under MIT license. 



import sys 
import re
import os 
import urllib


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
	version = versionMatch.group(1)
	print 'The latest firmware version is: ',version









def main():
	getLatestVersion()





#Just the regular boilerplate to start the program
if __name__ == '__main__':
	main()