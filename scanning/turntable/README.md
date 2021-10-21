# Turntable
A custom turntable powered by Arduino Uno.

## Requirements
- 1x Arduino Uno
- 1x A4988 motor driver
- 1x bipolar stepper motor with a NEMA 17 interface
	- note: the length of mine is 54mm (including the shaft), which is likely not standard; if you wish to use a different-sized NEMA 17 motor, send me an email and I'll add the adjusted body to the `parts/` directory (or, if you have Fusion 360, you can also do it yourself)
- 1x power supply for the motor
- 6x 608 bearings

## Construction
1. print the parts of the printer (found in the `parts/` folder)
	- it also contains `Turntable.f3d`, which is a Fusion 360 file that I used to generate the STLs
2. add bearings and the motor
3. wire and power everything properly
4. load code to the Arduino (found in the `code/` folder)

After this, the Arduino can be controlled as seen in the `code/code.ino` script. Essentially, it listens on the serial channel for a number between 0 and 255, which determines the turning angle. After the turning is done, it responds back with the same number it received and listens again.
