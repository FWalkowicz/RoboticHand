import machine
import utime

ADXL345_I2C_ADDR = 0x53

ADXL345_REG_X = 0x32
ADXL345_REG_Y = 0x34
ADXL345_REG_Z = 0x36

i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1))

i2c.writeto_mem(ADXL345_I2C_ADDR, 0x2D, bytes([0]))  # Wyłączenie czujnika
i2c.writeto_mem(ADXL345_I2C_ADDR, 0x31, bytes([0]))  # Ustawienie pomiaru w trybie normalnym
i2c.writeto_mem(ADXL345_I2C_ADDR, 0x2D, bytes([8]))  # Włączenie czujnika

while True:
    data_x = i2c.readfrom_mem(ADXL345_I2C_ADDR, ADXL345_REG_X, 2)
    data_y = i2c.readfrom_mem(ADXL345_I2C_ADDR, ADXL345_REG_Y, 2)
    data_z = i2c.readfrom_mem(ADXL345_I2C_ADDR, ADXL345_REG_Z, 2)
    
    acceleration_x = (data_x[1] << 8) | data_x[0]
    acceleration_y = (data_y[1] << 8) | data_y[0]
    acceleration_z = (data_z[1] << 8) | data_z[0]
    
    print("Przyspieszenie X: {} | Y: {} | Z: {}".format(acceleration_x, acceleration_y, acceleration_z))
    
    utime.sleep(10)
