### BCN3D Software Utilities

This repository serves as container for all the script files we use in house for production or even for testing.
We update this repo quite often and sometimes is difficult to keep up with documentation but we'll do our best.


## Folders

In this repo you will find the following folders:

- **Firmware updater Cura:** this folder has the basic phyton code for Cura that looks for new releases of our BCN3D Sigma Firmware and let's you upgrade the version of the 3D printer.
- **Firmware uploader scripts:** it contains the scripts for windows and UNIX systems to upload the latest firmware to the boards fast. It helps us in production and test procedures.
- **Screen bootloader script:** as we need to upload the bootloader to the _4D Systems_ touch panel we use in the BCN3D Sigma, we use a simple script that loads 8 at a time. What this bootloader does is search the files in the microSD card instead of the internal chip memory.
- **ThermistorLookUpTables:** this folder contains the python generator for the thermistor Look up tables which Marlin is based on.
- **GcodeTests:** it contains pre-made gcodes to test each axis of the printer individually. The gcodes sweep all the speeds. Inside there's a folder called ``stress`` that contains gcodes that stresses each axis with higher speeds and accelerations.   
- **Cura 2 BCN3D Profiles:** this folder contains the basic profiles of the BCN3D Sigma for the Cura 2 Slicing Software.
## To Do

- [ ] Update Firmware uploader for windows.
- [x] Select between multiple `.hex` firmwares in /Files folder.
- [x] Explain how to use 4D Systems bootloader script.
