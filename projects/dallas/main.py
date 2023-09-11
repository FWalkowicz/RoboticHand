from time import sleep, sleep_ms, localtime
from ujson import loads, dumps
from urequests import post, put
from machine import Pin, reset
from network import WLAN, STA_IF
from onewire import OneWire
from ds18x20 import DS18X20
from socket import socket
from errno import ECONNABORTED

# config
file = open("config.json")
cfg = file.read()
config = loads(cfg)

database = str(config["IP"])
ssid = str(config["SSID"])
password = str(config["PASSWORD"])
name = str(config["DEVICE_NAME"])
type = str(config["DEVICE_TYPE"])
id = str(config["DEVICE_ID"])

# GPIO
pico_led = Pin("LED")

ds_pin = Pin(0)
ds_sensor = DS18X20(OneWire(ds_pin))

# database
update_url = f"https://{database}/devices/{id}"
register_url = f"https://{database}/devices/register"
url = f"https://{database}/temperature"
print(f"connecting to database @ https://{database}")

headers = {
    "Content-type": "application/json",  # type: ignore
    "Accept": "application/json",  # type: ignore
}


def register(register_url, update_url, data, headers):
    print(register_info)
    for _ in range(5):
        try:
            register = post(
                url=register_url, data=data, headers=headers
            )  # send register request
            print("Data sent successfully!")
            if (
                "Registered device" in register.content
            ):  # if already registered send update data
                put(url=update_url, data=data, headers=headers)
                print("Updated successfully!")
            return True
        except OSError as e:
            if e.args[0] == ECONNABORTED:
                print("Connection aborted. Retrying in 5 seconds...")
                sleep(5)
            else:
                print("An error occurred:", e)
                return False
    return False


# wifi
def connect():
    wlan = WLAN(STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print("Waiting for connection...")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}")
    return ip


def open_socket(ip):
    address = (ip, 80)
    connection = socket()
    connection.bind(address)
    connection.listen(1)
    return connection


try:
    ip = connect()
    connection = open_socket(ip)
except KeyboardInterrupt:
    reset()

# register
register_info = dumps(
    {
        "deviceId": id,  # type: ignore
        "name": name,  #  type: ignore
        "deviceType": type,  #  type: ignore
    }
)
register(register_url, update_url, register_info, headers)

# main
file = open("log.csv", "w")
roms = ds_sensor.scan()
print("Found DS devices: ", roms)

while True:
    ds_sensor.convert_temp()
    sleep_ms(750)

    for rom in roms:
        utc_time = localtime()
        utc_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.{:03d}Z".format(
            utc_time[0],
            utc_time[1],
            utc_time[2],
            utc_time[3],
            utc_time[4],
            utc_time[5],
            utc_time[7],
        )
        log_timestamp = "{:02d}:{:02d}:{:02d}".format(
            utc_time[3],
            utc_time[4],
            utc_time[5],
        )

        readings = dumps(
            {
                "temperature": round(ds_sensor.read_temp(rom), 1),  # type: ignore
                "deviceId": id,  # type: ignore
                "name": name,  #  type: ignore
                "deviceType": type,  #  type: ignore
                "timestampUTC": utc_timestamp,  # type: ignore
            }
        )

        print(readings)
        file.write(str(round(ds_sensor.read_temp(rom), 1)) + " " + log_timestamp + ", ")
        file.flush()
        pico_led.value(1)
        sleep(1)
        pico_led.value(0)
        try:
            send = post(url=url, data=readings, headers=headers)
            print(send.content)
        except OSError as e:
            if e.args[0] == ECONNABORTED:
                print("Connection aborted. Retrying in 15 min...")
            else:
                print("An error occurred:", e)
    sleep(15)
