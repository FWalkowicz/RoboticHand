from machine import Pin
from utime import sleep

pin = Pin("LED", Pin.OUT)
pin.value(0)
i=0
print("SOS signal...")
while True:
#S
    while i<3:
        pin.value(1)
        sleep(0.25)
        pin.value(0)
        sleep(0.25)
        i=i+1
    sleep(0.75)
    i=0
#O
    while i<3:
        pin.value(1)
        sleep(1)
        pin.value(0)
        sleep(0.25)
        i=i+1
    sleep(0.75)
    i=0
#S
    while i<3:
        pin.value(1)
        sleep(0.25)
        pin.value(0)
        sleep(0.25)
        i=i+1
    sleep(0.75)
    i=0
    sleep(3)
    