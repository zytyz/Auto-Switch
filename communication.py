import serial
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-sp', '--serial_port', default="/dev/cu.usbmodem142201", help="Serial Port Name")
args = parser.parse_args()

arduino = serial.Serial(args.serial_port, 9600, timeout=.1)
while True:
    bytesOnBuffer = arduino.in_waiting
    # print("Bytes available: {}".format(bytesOnBuffer))

    # if bytesOnBuffer > 0:
    data = arduino.read(2)
    print(data)

    """
    data = arduino.readline()[:-2].decode("utf-8")  # the last bit gets rid of the new-line chars
    if data:
        print(data)"""
