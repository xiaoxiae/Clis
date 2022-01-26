# Turntable
A custom turntable powered by Arduino Uno.

Some numbers of the components vary, depending on how powerful you want the turntable to be. The minimum is 1 (obviously), the maximum being 3.

## Requirements
- 1x Arduino Uno
- 1x-3x A4988-based motor drivers
- 1x-3x bipolar stepper motors with a NEMA 17 interface
	- note: the length of mine is ~64mm (including the shaft), which is likely not standard; if you wish to use a different-sized NEMA 17 motor, either send me an email and I'll add the adjusted body to the `parts/` directory, or do it yourself (the model was created using Fusion 360 and the `parts/` folder contains the source file)
- 4x-12x M3 screws (motor mounts to motors), thread length 0.5cm
- 2x-6x M3 screws (motor mounts to body), thread length 1cm
- 2x-6x M3 nuts (motor mounts to body)
- 1x power supply for the motor(s)
- (1 + 6)x 608 bearings

## Construction
1. print parts of the printer (found in the `parts/` folder):
	- 1x body
	- 1x top
	- 1x-3x motor mount
2. add the bearings
3. wire and power everything properly
	- I used a small breadboard to make this step as easy as possible
	- Arduino expects the following mapping of pins to the A4988 sensor(s):
		- `2` -> `DIR`
		- `3` -> `STEP`
		- `4` -> `ENABLE`
	- don't forget to **tune the controllers:** https://ardufocus.com/howto/a4988-motor-current-tuning/
4. load the code to the Arduino (found in the `code/` folder)

After this, the Arduino can be controlled as seen in the `code/code.ino` script: it listens on the serial channel for the next string that it then converts to an integer and uses it as the turning angle. After the turning is done, it responds back with the same number it received (again as a string) and again starts to listen.
