# Overflow Detector
This is the code for a simple microcontroller with a moisture sensor and a buzzer that alerts the user when the moisture sensor detects water. This is used for detecting overflow from an airco water reservoir to avoid spills.

## Installation
Having flashed the micropython firmware to the ESP32 you can upload the code:
```bash
ampy --port /dev/ttyUSB0 --baud 115200 put main.py
```

To see the output:
```bash
screen /dev/ttyUSB0 115200
```
