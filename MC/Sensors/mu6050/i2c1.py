from imu import MPU6050
import time
from machine import Pin, I2C

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)
g_to_m = 9.80665
print("ax        ay        az        gx        gy        gz        temp")
while True:
    #acceleration default unit g
    #gyro default unit deg/s
    #temp in C
    ax=round(imu.accel.x * g_to_m - 7.1, 2) #acceleration converted to m/s2
    ay=round(imu.accel.y * g_to_m - 1.4, 2)
    az=round(imu.accel.z * g_to_m - 7.7, 2)
    gx=round(imu.gyro.x - 12.5, 2)
    gy=round(imu.gyro.y + 9, 2)
    gz=round(imu.gyro.z - 1, 2)
    tem=round(imu.temperature,2)  
    print(ax,"    ",ay,"    ",az,"    ",gx,"    ",gy,"    ",gz,"    ",tem,"        ",end="\r")
    time.sleep(0.2)