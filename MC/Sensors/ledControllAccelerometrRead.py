import network
import socket
import time

from machine import Pin, I2C
from imu import MPU6050

def accelerometer_measurement():
    ax=imu.accel.x * g_to_m #acceleration converted to m/s2
    ay=imu.accel.y * g_to_m
    az=imu.accel.z * g_to_m
    gx=imu.gyro.x
    gy=imu.gyro.y
    gz=imu.gyro.z
    tem=imu.temperature
    return [ax, ay, az, gx, gy, gz, tem]

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)
g_to_m = 9.80665
pax = 0
pay = 0
paz = 0
pgx = 0
pgy = 0
pgz = 0
a_sensitivity=0
g_sensitivity=0

led = Pin("LED", Pin.OUT)
led.value(0)
stateis="LED is OFF"
led_status=False
ssid = 'COMORE_WIFI'
password = '!Q2w3e4r'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

html = """<!DOCTYPE html>
<html>
    <head> <title>Pico W</title> </head>
    <body> <h1>Pico W</h1>
        <h2>LED</h2>
        <form action="/light/on">
            <input type="submit" value="LED ON" />
        </form>
        <form action="/light/off">
            <input type="submit" value="LED OFF" />
        </form>
        <p>%s</p>
        <h2>Accelerometr</h2>
        <form action="/accelerometr/refresh">
            <input type="submit" value="REFRESH TABLE" />
        </form>
        <table border>
        <tr>
            <th>ax</th>
            <th>ay</th>
            <th>az</th>
            <th>gx</th>
            <th>gy</th>
            <th>gz</th>
            <th>tmp</th>
        </tr>
        <tr>
            %s
        </tr>
        </table>
        <form action="/reset/accelerometr">
            <input type="submit" value="RESET ACCELEROMETR" />
        </form>
        <h3>Set Acceleromert Sensitivity (%s)</h3>
        <form action="/accelerometr/sensitivity/0">
            <input type="submit" value="0" />
        </form>
        <form action="/accelerometr/sensitivity/1">
            <input type="submit" value="1" />
        </form>
        <form action="/accelerometr/sensitivity/2">
            <input type="submit" value="2" />
        </form>
        <form action="/accelerometr/sensitivity/3">
            <input type="submit" value="3" />
        </form>
        <h3>Set Gyroscope Sensitivity (%s)</h3>
        <form action="/gyroscope/sensitivity/0">
            <input type="submit" value="0" />
        </form>
        <form action="/gyroscope/sensitivity/1">
            <input type="submit" value="1" />
        </form>
        <form action="/gyroscope/sensitivity/2">
            <input type="submit" value="2" />
        </form>
        <form action="/gyroscope/sensitivity/3">
            <input type="submit" value="3" />
        </form>
    </body>
</html>
"""

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print(request)

        request = str(request)
        led_on = request.find('/light/on')
        led_off = request.find('/light/off')
        table_refresh = request.find('/accelerometr/refresh')
        reset_accelerometr = request.find('/reset/accelerometr')
        accelerometer_sensitivity = request.find('/accelerometr/sensitivity')
        gyroscope_sensitivity = request.find('/gyroscope/sensitivity')
        print( 'led on = ' + str(led_on))
        print( 'led off = ' + str(led_off))

        

        if led_on == 6:
            print("led on")
            led.value(1)
            stateis = "LED is ON"
            led_status = True

        if led_off == 6:
            print("led off")
            led.value(0)
            stateis = "LED is OFF"
            led_status = True

        if table_refresh == 6:
            ax, ay, az, gx, gy, gz, tem = accelerometer_measurement()
            mpu6050 = str("<td>"+str(round(ax+pax,2))+"</td><td>"+str(round(ay+pay,2))+"</td><td>"+str(round(az+paz,2))+"</td><td>"+str(round(gx+pgx,2))+"</td><td>"+str(round(gy+pgy,2))+"</td><td>"+str(round(gz+pgz,2))+"</td><td>"+str(round(tem,2))+"</td>")


        if reset_accelerometr == 6:
            print("reset accelerometr")
            ax, ay, az, gx, gy, gz, tem = accelerometer_measurement()
            pax = -ax
            pay = -ay
            paz = -az
            pgx = -gx
            pgy = -gy
            pgz = -gz
        
        if accelerometer_sensitivity == 6:
            if request.find('/accelerometr/sensitivity/0')!=-1:
                a_sensitivity=0
            elif request.find('/accelerometr/sensitivity/1')!=-1:
                a_sensitivity=1
            elif request.find('/accelerometr/sensitivity/2')!=-1:
                a_sensitivity=2
            elif request.find('/accelerometr/sensitivity/3')!=-1:
                a_sensitivity=3
            imu.accel_range = a_sensitivity
            print("Accelerometr Sensivty set ", a_sensitivity)
        if gyroscope_sensitivity == 6:
            if request.find('/gyroscope/sensitivity/0')!=-1:
                g_sensitivity=0
            elif request.find('/gyroscope/sensitivity/1')!=-1:
                g_sensitivity=1
            elif request.find('/gyroscope/sensitivity/2')!=-1:
                g_sensitivity=2
            elif request.find('/gyroscope/sensitivity/3')!=-1:
                g_sensitivity=3
            imu.accel_range = g_sensitivity
            print("Accelerometr Sensivty set ", g_sensitivity)
        ax, ay, az, gx, gy, gz, tem = accelerometer_measurement()  
        mpu6050 = str("<td>"+str(round(ax+pax,2))+"</td><td>"+str(round(ay+pay,2))+"</td><td>"+str(round(az+paz,2))+"</td><td>"+str(round(gx+pgx,2))+"</td><td>"+str(round(gy+pgy,2))+"</td><td>"+str(round(gz+pgz,2))+"</td><td>"+str(round(tem,2))+"</td>")

        response = html % (stateis, mpu6050, a_sensitivity, g_sensitivity)

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')