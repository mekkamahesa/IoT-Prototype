import time
import urequests
import network
from machine import Pin, time_pulse_us

WIFI_SSID = 'ADMIN8'
WIFI_PASS = 'ADMIN8'
UBIDOTS_TOKEN = "BBUS-itVkw0RhfDRPK6GiVnfgbiLsOhdWOn"
DEVICE_LABEL = "smart-trash"
VARIABLE_LABEL = "trash_level"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)
    while not wlan.isconnected():
        print("Menyambungkan WiFi...")
        time.sleep(1)
    print("WiFi Connected:", wlan.ifconfig())

TRIG = Pin(5, Pin.OUT)
ECHO = Pin(18, Pin.IN)

def get_distance():
    TRIG.off()
    time.sleep_us(2)
    TRIG.on()
    time.sleep_us(10)
    TRIG.off()
    duration = time_pulse_us(ECHO, 1, 30000)  # 30ms timeout
    if duration < 0:
        return None
    distance_cm = duration * 0.0343 / 2
    return distance_cm

def send_to_ubidots(level):
    url = f"http://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}/"
    headers = {
        "X-Auth-Token": UBIDOTS_TOKEN,
        "Content-Type": "application/json"
    }
    data = {VARIABLE_LABEL: level}
    try:
        response = urequests.post(url, headers=headers, json=data)
        print("Ubidots Response:", response.text)
        response.close()
    except Exception as e:
        print("Gagal kirim ke Ubidots:", e)

connect_wifi()
TRASH_BIN_HEIGHT = 30  # cm

while True:
    dist = get_distance()
    if dist is None or dist > TRASH_BIN_HEIGHT:
        level = 0
    else:
        level = 100 - (dist / TRASH_BIN_HEIGHT * 100)
        level = max(0, min(100, level))
    print("Level Sampah:", level, "%")
    send_to_ubidots(level)
    time.sleep(15)