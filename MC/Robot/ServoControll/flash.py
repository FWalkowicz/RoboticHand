from servo import ServoCluster, servo2040, Servo,Calibration
from i2cSlave import i2c_slave
from time import sleep

s_i2c = i2c_slave(0,sda=20,scl=21,slaveAddress=0x42)
s0 = Servo(servo2040.SERVO_1)
s1 = Servo(servo2040.SERVO_2)
s2 = Servo(servo2040.SERVO_3)
clusterPins = list(range(servo2040.SERVO_4, servo2040.SERVO_5+1))
cluster = ServoCluster(0, 0, clusterPins)
s0.enable()
s1.enable()
s2.enable()
cluster.enable_all()
sleep(1)
dataArr = []
data = 0
#s0.to_min()
while True:
    while data!=255:
        data = s_i2c.get()
        dataArr.append(data)
    if len(dataArr)>0:
       # print(dataArr)
        data=0
        if dataArr[2]==181:
            cluster.to_min(dataArr[1])
        elif dataArr[2]==182:
            cluster.to_mid(dataArr[1])
        elif dataArr[2]==183:
            cluster.to_max(dataArr[1])
        else:
            if dataArr[1] == 3:
                cluster.to_percent(0, dataArr[2]/180, load=False)
                cluster.to_percent(1, 1 - dataArr[2]/180, load=False)
            elif dataArr[1] == 0:
                s0.to_percent(dataArr[2]/180)
            elif dataArr[1] == 1:
                s1.to_percent(dataArr[2]/180)
            elif dataArr[1] == 2:
                s2.to_percent(dataArr[2]/180)
        dataArr.clear()