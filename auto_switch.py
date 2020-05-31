import control_web as cw
import connect_app as ca 
from http.server import HTTPServer
import serial

#TODO
port = '/dev/cu.HC-05-SPPDev-1'
IP = '127.0.0.1'

STATE = [False, False, False]

def buttonClick(driver, signal):
    driver = cw.button_click(driver, signal)
    STATE[signal - 1] != STATE[signal - 1]
    return driver

def arduinoSignal(driver, signal):
    for i in range(3):
        if signal ^ STATE[i]:
            driver = buttonClick(driver, i + 1)

if __name__ == '__main__':
    #TODO
    # ESP32
    driver = cw.connect_to_page('http://www.google.com')
    arduino = serial.Serial(port, 9600, timeout=.1)

    # virtual web
    server_address_httpd = (IP, 8080)
    httpd = HTTPServer(server_address_httpd, ca.RequestHandler_httpd)
    httpd.serve_forever()

    buttonSignal = ca.MyRequest

    while True:
        data = arduino.readline()[:-2].decode('utf-8')

        prev = ca.COUNT
        if data == 'i': ca.COUNT += 1
        elif data == 'o': ca.COUNT -= 1

        buttonSignal = 3

        if buttonSignal:
            driver = buttonClick(driver, buttonSignal)
        elif prev == 1 and ca.COUNT == 0:
            arduinoSignal(0)
        elif prev == 0 and ca.COUNT == 1:
            arduinoSignal(1)
