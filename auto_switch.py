import control_web as cw
import serial

port = '/dev/cu.HC-05-SPPDev-1'

if __name__ == '__main__':
    driver = cw.connect_to_page('http://www.google.com')
    arduino = serial.Serial(port, 9600, timeout=.1)

    while True:
        data = arduino.readline()[:-2].decode('utf-8')
        if data:
            print (data)
