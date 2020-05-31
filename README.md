# Auto-Switch
## How To Run
### Set up the ESP32 Server
### Raspberry Pi
1. Driver
   - Unable to install **Chrome** on RPi. Therefore, the original *ChromeDriver* won’t work.
   - Not able to find *Chromium Driver* for **Debian 10 armv7l**.
   - With the help of [樹莓派 Raspberry Pi 使用 Python + Selenium 控制 Chromium 瀏覽器](https://blog.gtwang.org/iot/raspberry-pi/raspberry-pi-install-chromium-chrome-driver/), finally a suitable driver for our system.
2. EXPORT PATH
   - For the code to work properly, `/usr/lib/chromium-browser/chromedriver` needs to be export to the `PATH`.
   - However, during the process, I’ve accidentally overwrite the original `PATH` which cause most of the block most of the commands.
   - Eventually, `echo "[original PATH]" >> ~/.bashrc` to enable all those commands and then add `chromedriver` to the `PATH`
## Compile Problem
### Wrong Servo Library
```

WARNING: library Servo claims to run on (avr, sam, samd, nrf52, stm32f4) architecture(s) and may be incompatible with your current board which runs on (esp32) architecture(s).
In file included from C:\Users\My PC\Desktop\switch\switch\switch.ino:8:0:

D:\Program\Arduino\libraries\Servo\src/Servo.h:73:2: error: #error "This library only supports boards with an AVR, SAM, SAMD, NRF52 or STM32F4 processor."

 #error "This library only supports boards with an AVR, SAM, SAMD, NRF52 or STM32F4 processor."

  ^

exit status 1
開發板 DOIT ESP32 DEVKIT V1 編譯錯誤。

```
* Installing the ESP32_Arduino_Servo_Library
	* [github](https://github.com/RoboticsBrno/ServoESP32): uncompress the directory
	* [Import a library](https://www.arduino.cc/en/guide/libraries): make sure "ServoESP32" is in the library

### Brownout detector was triggered (Shown in Serial Monitor)
* [link](https://www.reddit.com/r/esp32/comments/brt87e/brownout_detector_was_triggered_when_activating/)
	* Problem with hardware on voltage supply
	* Change a usb cable or don't power from a pc

### Choose the right Board
* for ESP32, choose "DOIT ESP32 DEVKIT V1"