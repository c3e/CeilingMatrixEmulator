# CeilingMatrixEmulator

This python script, tries to emulate the hardware of the ceiling pixel lamp, 
by creating a virtual serial port for the input and renders the output into a pygame window.
You can use it to test for example animations and games on your local machine, without the use of the actual hardware.

If you start the script, you should see a print message with the current virtual serial port path.
- ('Hey use this serial port:', '/dev/pts/7')

Create a symlink, so other application (like glediator) can see and use it.
- sudo ln -s /dev/pts/7 /dev/ttyUSB99
