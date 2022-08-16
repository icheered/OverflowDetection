# main.py
import time
import machine

time.sleep(3)
print("Starting!")

waterpin = machine.ADC(machine.Pin(36))
batterypin = machine.ADC(machine.Pin(35, machine.Pin.IN, machine.Pin.PULL_DOWN))
batterypin.atten(machine.ADC.ATTN_11DB)


def make_sound(timeOn):
    beeper = machine.PWM(machine.Pin(12, machine.Pin.OUT), freq=1000, duty=512)
    time.sleep(timeOn)
    beeper.deinit()

batteryArray = []
def isBatteryEmpty():
    battery = batterypin.read()

    # KEEP TRACK OF MULTIPLE VALUES AND TRIGGER IF MANY IN DESCENDING ORDER ARE FOUND
    # if len(batteryArray) < 5:
    #     batteryArray.append(battery)
    #     return
    
    
    # batteryArray[0:-1] = batteryArray[1:]
    # batteryArray[len(batteryArray)-1] = battery
    # print(batteryArray)
    if battery < 2000:
        return True
    

    # if battery > 5000:
    #     return False

    # # Check if numbers are all decreasing
    # for i in range(0, len(batteryArray) - 1):
    #     if batteryArray[i] >= batteryArray[i + 1]:
    #         return False
    
    # print("Battery empty!")
    # return True



make_sound(0.1)
time.sleep(0.1)
make_sound(0.1)

counter = 0
timeSleeping = 1
while 1:
    time.sleep(timeSleeping)
    if isBatteryEmpty():
        print("Battery empty!")
        make_sound(5)

    level = 0
    for i in range(5):
        level += 0.2 * waterpin.read()
    if level < 3000:
        timeSleeping = 1
        for i in range(5):
            make_sound(0.1)
            time.sleep(0.1)
    else:
        timeSleeping = 30
    batterylevel = batterypin.read()
    print(f"Loop: {counter}, Waterlevel: {level}, Battery: {batterylevel}")
    counter += 1
    