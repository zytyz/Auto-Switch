import control_web as cw
import connect_app as ca 
from http.server import HTTPServer
import serial

#TODO
port = '/dev/cu.usbmodem14101'
IP = '127.0.0.1'

STATE = [False, False, False]

def buttonClick(driver, signal):
    driver = cw.button_click(driver, signal)
    STATE[signal - 1] != STATE[signal - 1]
    return driver

def arduinoSignal(driver, signal):
    for i in range(3):
        if signal ^ STATE[i]:
            print ('click', i)
            driver = buttonClick(driver, i + 1)
    return driver

if __name__ == '__main__':
    #TODO
    # ESP32
    driver = cw.connect_to_page()
    arduino = serial.Serial(port, 9600)
    print ('Arduino')

    # virtual web
    server_address_httpd = (IP, 8080)
    httpd = HTTPServer(server_address_httpd, ca.RequestHandler_httpd)
    print ('before serve_forever')
    # httpd.serve_forever()

    print ('START......')
    while True:
        data = arduino.readline()[:-2].decode('utf-8')

        prev = ca.COUNT
        if data == 'i': ca.COUNT += 1
        elif data == 'o': ca.COUNT -= 1

        print (data)
        print (ca.COUNT)

        buttonSignal = ca.MyRequest

        if buttonSignal:
            driver = buttonClick(driver, buttonSignal)
        elif prev == 1 and ca.COUNT == 0:
            driver = arduinoSignal(driver, 0)
            print ('nobody')
        elif prev == 0 and ca.COUNT == 1:
            driver = arduinoSignal(driver, 1)
            print ('one person')
