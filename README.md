# Auto-Switch

## Introduction
why用外力按開關

## System Architecture
<p align="center">
   <img src="./images/architecture.png" alt="image" width="750"/>
   </br>
   System Architecture
</p>

The image above shows our system architecture. Our system consists of different parts which are described in details as follows:
1. **Laser** and **Laser Detector**
   * Two pairs of lasers and laser sensors are placed in front of the door. The lasers are *constantly on* and aim at the corresponding sensor.
   * The laser sensors are connected to an arduino board that is connected to Raspberry Pi via *serial* port.
   * Together with the laser sensors, the arduino board is able to send a message to Raspberry Pi if a person *enters or exits the room*. (Details are described below)
2. **ESP32** and **Servos**
   * ESP32 board is microcontroll processing unit with integrated Wi-Fi and bluetooth connectivity.
   * The light switches of the room are *externally pressed by a number of servos*.
   * The servos are powered and controlled by ESP32.
   * ESP32 turns on/off the light switches following the commands from *Raspberry Pi via Wi-Fi connections*.
3. **Raspberry Pi**
   * Raspberry acts at the control conter of the system.
   * Based on the information from the arduino board, it records the number of people currently in the room.
   * If someone enters an orginally empty room, it *automatically* sends a message to ESP32 and turns on the lights.
   * Contrastly, when the last person left the room, it *automatically* sends a message to ESP32 and turns off the lights.
4. **App**
   * Although the lights are controlled automatically, e.g. Lights are on when someone is in the room while lights are off when the room is empty, one still might want to *control the lights manually*.
   * We designed an app to meet this need.
   * The app is based on Android and communicates with Raspberry Pi *via Wi-Fi connection* as well.


### When a person enters the room...
<p align="center">
   <img src="./images/enter_room.png" alt="image" width="750"/>
   </br>
   The laser detector
</p>

## Implementation
#### Light switches are pressed with external servos
* The servos are controlled by ESP32 through WiFi connections
* We 3d-printed a case for three light switches. A light switch is controlled by two servos, one of which presses the switch on while the other presses the switch off.
<p align="center">
   <img src="./images/servo_case_ESP32.png" alt="image" width="750"/>
   </br>
   Servo Case for the switches
</p>

#### The 2 laser sensors determine whether a person has entered
* Two sensors are placed in front of the door. Laser light is constantly on.
* When a person enters the room
* The number of people in the room is recorded. If eveyone has left the room


## Setting Up 
#### Set up the ESP32 Server
1. Connect the ESP32 to a pc and upload ```switch/switch.ino``` via Arduino IDE
   * Make sure to change the network credentials in ```switch/switch.ino```.
   * When uploading the code, the BOOT button on ESP32 should be pressed.
2. After pressing the EN button, open the Serial Monitor to know the **webpage URL**.

#### Set up the Laser and Sensor Module
1. Upload ```tmp.ino``` to the Arduino Board

#### Setting up Raspberry Pi
1. Connect Rpi to the same network ESP32 is connected to.
2. Connect the Arduino Board to Rpi with a usb cable.
   * Check the **port** the Arduino Board is using
3. Check the **IP address** of Rpi
4. Run the follwing command in terminal
```python
python auto_switch.py <port name> <IP address> <webpage URL>
```

#### Downloading the app (Optional: Allows manual control)
1. Download the app via command line
```
wget https://github.com/zytyz/Auto-Switch/releases/download/v0/AutoSwitch.apk
```
2. Run the .apk file on a Android Device

## Running
The switches are automatically controlled as people enter or exit the room. All switches are turned on when there are people remaining in the room, while all switches are turned off when everyone has exited.

The switches can also be manually controlled via the app. We can also check or reset the current number of people in the room as well.
#### App Interface
There are three parts of the app interface:
1. Setting IP address of Rpi
2. Controlling the Switches
3. Check the number of people remaining in the room
<p align="center">
   <img src="./images/app_screen.png" alt="image" width="250"/>
   </br>
   App Interface
</p>


## Diffuculties and Solution
#### ESP32 Setup

1. Wrong Servo Library
   - An error occurred when trying to compile the code for ESP32.
    ```
      WARNING: library Servo claims to run on (avr, sam, samd, nrf52, stm32f4) architecture(s) and may be incompatible with your current board which runs on (esp32) architecture(s).
      In file included from C:\Users\My PC\Desktop\switch\switch\switch.ino:8:0:

      D:\Program\Arduino\libraries\Servo\src/Servo.h:73:2: error: #error "This library only supports boards with an AVR, SAM, SAMD, NRF52 or STM32F4 processor."

      #error "This library only supports boards with an AVR, SAM, SAMD, NRF52 or STM32F4 processor."

      ^

      exit status 1
      開發板 DOIT ESP32 DEVKIT V1 編譯錯誤。
    ```
   - We solved this problem by installing the ESP32_Arduino_Servo_Library
      - [github](https://github.com/RoboticsBrno/ServoESP32): uncompress the directory
      - [Import a library](https://www.arduino.cc/en/guide/libraries): make sure "ServoESP32" is in the library

2. Brownout detector was triggered (Shown in Serial Monitor)
   * When a button was pressed or the ESP32 sets up connection, an error "Brownout detector was triggered" might occur.
   * This results from a problem of the voltage supply of ESP32.
   * Solution ([reference](https://www.reddit.com/r/esp32/comments/brt87e/brownout_detector_was_triggered_when_activating/))
      * Change a usb cable
      * Do not power from a pc

#### Raspberry Pi Setup
1. Driver
   - Unable to install **Chrome** on RPi. Therefore, the original *ChromeDriver* won’t work.
   - Not able to find *Chromium Driver* for **Debian 10 armv7l**.
   - With the help of [樹莓派 Raspberry Pi 使用 Python + Selenium 控制 Chromium 瀏覽器](https://blog.gtwang.org/iot/raspberry-pi/raspberry-pi-install-chromium-chrome-driver/), finally a suitable driver for our system.
2. EXPORT PATH
   - For the code to work properly, `/usr/lib/chromium-browser/chromedriver` needs to be export to the `PATH`.
   - However, during the process, I’ve accidentally overwrite the original `PATH` which cause most of the block most of the commands.
   - Eventually, `echo "[original PATH]" >> ~/.bashrc` to enable all those commands and then add `chromedriver` to the `PATH`

## Precautions
1. Choose the right Board in the Arduino IDE
   * for ESP32, choose "DOIT ESP32 DEVKIT V1"
   * for Arduino UNO, choose "Arduino UNO"
2. When connecting to Rpi remotely, make sure to connect to the Raspberry Pi with X11 forwarding enabled.
```
ssh -X pi@192.xx.x.xx
```
3. (continue) Instead of opening a browser, add few codes to bypass the problem.
```python=
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome('chromedriver', chrome_options=options)
```
