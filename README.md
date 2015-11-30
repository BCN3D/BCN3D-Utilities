### BCN3D Software Utilities

This repository serves as container for all the script files we use indoors for production or even for testing.
We update this repo quite often and sometimes is difficult to keep up with documentation but we'll do our best.


## Folders

In this repo you will find the following folders:

- **Firmware updater Cura:** this folder has the basic phyton code for Cura that looks for new releases of our BCN3D Sigma Firmware and let's you upgrade the version of the 3D printer.
- **Firmware uploader scripts:** it contains the scripts for windows and UNIX systems to upload the latest firmware to the boards fast. It helps us in production and test procedures.
- **Screen bootloader script:** as we need to upload the bootloader to the _4D Systems_ touch panel we use in the BCN3D Sigma, we use a simple script that loads 8 at a time. What this bootloader does is search the files in the microSD card instead of the internal chip memory.

## To Do

- [ ] Update Firmware uploader for windows.
- [ ] Update the `main.py` file.
- [x] Select between multiple `.hex` firmwares in /Files folder.
- [ ] Explain how to use 4D Systems bootloader script.
