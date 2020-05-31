import control_web as cw
import connect_app as ca
from http.server import HTTPServer
import serial
import threading
import sys

# TODO
# port = '/dev/cu.usbmodem14101' # mhsu
try:
    port = sys.argv[1]
    IP = sys.argv[2]
except:
    port = "/dev/cu.usbmodem143201"  # zyt
    IP = '192.168.0.102'

STATE = [False, False, False]


def executeAppRequest(appRequest):
    """
    :param appRequest(str): the string sent from the connected app
    :return:
    """
    global driver
    print("Executing App Request...")
    if "Button" in appRequest:
        buttonIdx = int(appRequest.split('_')[1])
        buttonClick(driver, signal=buttonIdx)
        print("Clicked Button {}".format(buttonIdx))
    elif appRequest == "Update_Status":
        print("Status Updated")
    elif "Reset_Num_to_" in appRequest:
        num = int(appRequest.split('_')[-1])
        ca.COUNT = num
        print("Number Reset")


def buttonClick(driver, signal):
    """
    Click the Button on the Webpage and change state
    :param driver:
    :param signal:
    :return:
    """
    global STATE
    driver = cw.button_click(driver, signal)
    STATE[signal - 1] = False if STATE[signal - 1] else True
    return driver


def allButtonClick(driver, signal):
    """
    Click all Button once
    :param driver:
    :param signal:
    :return:
    """
    for i in range(3):
        if signal ^ STATE[i]:
            print('click', i)
            driver = buttonClick(driver, i + 1)
    return driver


def run_server():
    global httpd
    print("Start Server")
    httpd.serve_forever()


def arduino_listen():
    global driver, arduino
    print('Listening to Arduino...')
    while True:
        print("hihihi")
        # print(ca.newRequest)
        bytesOnBuffer = arduino.in_waiting
        print("Bytes available: {}".format(bytesOnBuffer))

        if bytesOnBuffer > 0:
            data = arduino.readline()[:-2].decode('utf-8')
            print(data)
        else:
            data = ''

        prev = ca.COUNT
        if data == 'i':
            ca.COUNT += 1
            print("Arduino i")
        elif data == 'o':
            ca.COUNT -= 1
            print("Arduino o")

        if ca.newRequest:
            appRequest = ca.MyRequest
            print(appRequest)
            ca.newRequest = False
            executeAppRequest(appRequest)
            # driver = buttonClick(driver, buttonSignal)
        elif prev == 1 and ca.COUNT == 0:
            driver = allButtonClick(driver, 0)
            print('nobody')
        elif prev == 0 and ca.COUNT == 1:
            driver = allButtonClick(driver, 1)
            print('one person')


if __name__ == '__main__':
    # TODO
    # ESP32

    server_address_httpd = (IP, 8080)
    httpd = HTTPServer(server_address_httpd, ca.RequestHandler_httpd)

    driver = cw.connect_to_page()
    arduino = serial.Serial(port, 9600)

    threads = []
    thread_server = threading.Thread(target=run_server)
    threads.append(thread_server)
    thread_arduino = threading.Thread(target=arduino_listen)
    threads.append(thread_arduino)
    # thread.daemon = True
    for t in threads:
        t.start()
