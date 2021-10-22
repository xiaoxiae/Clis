# Turntable
A custom turntable powered by Arduino Uno.

## Requirements
- 1x Arduino Uno
- 1x A4988-based motor driver
- 1x bipolar stepper motor with a NEMA 17 interface
	- note: the length of mine is ~64mm (including the shaft), which is likely not standard; if you wish to use a different-sized NEMA 17 motor, either send me an email and I'll add the adjusted body to the `parts/` directory, or do it yourself (the model was created using Fusion 360 and the `parts/` folder contains the source file)
- 1x power supply for the motor
- 6x 608 bearings

## Construction
1. print all parts of the printer (found in the `parts/` folder)
	- `Mid.stl` is mostly to keep the wires from interfering with the bearings and is optional
2. add bearings and the motor
3. wire and power everything properly
	- Arduino expects the following mapping of pins to the A4988 sensor:
		- `2` -> `DIR`
		- `3` -> `STEP`
		- `4` -> `ENABLE`
4. load the code to the Arduino (found in the `code/` folder)

After this, the Arduino can be controlled as seen in the `code/code.ino` script. Essentially, it listens on the serial channel for the next string that it converts to an integer and uses it as the turning angle. After the turning is done, it responds back with the same number it received (again as a string) and repeats.
