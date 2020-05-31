import control_web as cw
import serial

if __name__ == '__main__':
    driver = cw.connect_to_page('http://www.google.com')
