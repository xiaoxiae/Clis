import serial
from time import sleep

ser = serial.Serial(
    "/dev/ttyACM0",
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)

if not ser.isOpen():
    ser.open()

# give Arduino some time to connect
# important, *don't change this*
sleep(2)

def turn_by(angle: int):
    """Turn the turntable by an angle."""

    ser.flushInput()
    ser.flushOutput()

    print(angle)

    ser.write(str(angle).encode())

    while True:
        data = ser.readline().decode().strip()

        if data == str(angle):
            break
        else:
            sys.exit(1)

turn_by(90)
