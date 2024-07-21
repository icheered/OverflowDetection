# main.py
import gc

import machine
import network
import urequests
import utime as time

# Constants
SSID = "name"
PASSWORD = "password"
WATER_PIN = 36
BATTERY_PIN = 35
BEEPER_PIN = 12
URL = "http://192.168.5.131/cm?cmnd=Power"


# Setup ADC
def setup_adc(pin_number, attenuation):
    adc_pin = machine.ADC(
        machine.Pin(pin_number, machine.Pin.IN, machine.Pin.PULL_DOWN)
    )
    adc_pin.atten(attenuation)
    return adc_pin


waterpin = setup_adc(WATER_PIN, machine.ADC.ATTN_11DB)
batterypin = setup_adc(BATTERY_PIN, machine.ADC.ATTN_11DB)


# Beeper setup
def make_sound(time_on):
    beeper = machine.PWM(machine.Pin(BEEPER_PIN, machine.Pin.OUT), freq=1000, duty=512)
    time.sleep(time_on)
    beeper.deinit()


def make_repeated_sound(time_on, time_off, times):
    for i in range(times):
        make_sound(time_on)
        time.sleep(time_off)


# WiFi connection
def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    print("Connecting to WiFi", end="")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(1)
    print("\nConnected to WiFi")
    config = wlan.ifconfig()
    print("Network config:", config)
    # Log the RSSI (signal strength)
    rssi = wlan.status("rssi")
    print(f"WiFi signal strength: {rssi} dBm")


# Smart switch control
def smart_switch_available(url, retry_count=3):
    wlan = network.WLAN(network.STA_IF)  # Get the network interface
    for attempt in range(retry_count):
        try:
            response = urequests.get(url)
            status_code = response.status_code
            response.close()
            if status_code == 200:
                return True
            else:
                print(f"Attempt {attempt + 1} failed with status code: {status_code}")
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            print(f"Current network config: {wlan.ifconfig()}")
            rssi = wlan.status("rssi")
            print(f"Current WiFi signal strength: {rssi} dBm")
            if attempt < retry_count - 1:
                print("Retrying...")
                time.sleep(2)  # wait 2 seconds before retrying
            else:
                print("Failed after several attempts.")
    return False


def set_airco_state(url, state):
    try:
        urequests.get(f"{url}%20{state}")
        print(f"Airco state set to {state}")
    except Exception as e:
        print(f"Error setting Airco state: {e}")


# Sensor readings
def read_average_adc(adc_pin, samples=5):
    total = sum(adc_pin.read() for _ in range(samples))
    return total / samples


# Main loop
connect_to_wifi(SSID, PASSWORD)

if not smart_switch_available(URL):
    print("Airco smart switch not available")
    make_repeated_sound(3, 1, 3)
    exit(1)

set_airco_state(URL, "On")
make_repeated_sound(0.1, 0.1, 2)

count = 0
while True:
    count += 1
    print(f"Count: {count}")
    gc.collect()
    if not smart_switch_available(URL):
        print("Airco smart switch not available")
        make_sound(5)
        continue

    battery_level = read_average_adc(batterypin)
    water_level = read_average_adc(waterpin)
    print(f"Water level: {water_level}, Battery level: {battery_level}")

    if battery_level < 2000:
        print("Battery empty!")
        make_repeated_sound(1, 1, 5)
        set_airco_state(URL, "Off")
    elif water_level < 3000:
        print("Water detected!")
        set_airco_state(URL, "Off")
    else:
        set_airco_state(URL, "On")

    time.sleep(3)
