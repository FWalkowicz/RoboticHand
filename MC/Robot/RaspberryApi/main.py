from fastapi import FastAPI, HTTPException, status
from typing import Union, List
from pydantic import BaseModel
import smbus2
import time
import json

#create engine model
class Engine(BaseModel):
    engineId: int
    name: Union[str, None] 
    type: Union[int, None] 
    angle: Union[int, None] 
    mode: Union[int, None] 

#initialize engine list and load engine from config file
engineList = []
try:
    with open("config.json", "r") as configFile:
            config = json.load(configFile)
    for item in config:
        newEngine = Engine(**item)
        engineList.append(newEngine)
except:
        print("Invalid config")

#initialize i2c bus
bus_number = 1
device_address = 0x42
i2c_bus = smbus2.SMBus(bus_number)
time.sleep(1)

#initialize app
app = FastAPI()

@app.get("/")
async def root():
    return {"message:" "Hello World"}

@app.put("/init", response_model=List[Engine])
async def init_robot():
    for engine in range(5):
        try:
            i2cRequest = bytearray()
            i2cRequest.append(engine)
            i2cRequest.append(90)
            i2cRequest.append(255)
            i2c_bus.write_i2c_block_data(device_address, 0, i2cRequest)
            i2cRequest.clear()
        except:
            raise HTTPException(status_code=503, detail="I2C device error")
    return engineList

@app.put("/device_address")
async def set_device_address(address: str):
    global device_address
    try:
        device_address = int(address, 16)
    except:
        raise HTTPException(status_code=400, detail="Invalid input, valid format: 0x11")
    return "Device address set to {}".format(hex(device_address))


@app.get("/device_address")
async def get_device_address():
    return hex(device_address)

@app.post("/engines/", response_model=Engine)
async def add_engine(engine: Engine):
    for existing_engine in engineList:
        if existing_engine.engineId == engine.engineId:
            raise HTTPException(status_code=400, detail="Engine with this id already exist")
    engineList.append(engine)
    return engine

@app.get("/engines/", response_model=List[Engine])
async def get_all_engines():
    return engineList

@app.get("/engines/{id}", response_model=Engine)
async def get_engine(id: int):
    for engine in engineList:
        if id == engine.engineId:
            return engine
    raise HTTPException(status_code=404, detail="Engine with this id not exist")

@app.put("/engines/{id}", response_model=Engine)
async def set_mode_angle(id: int, mode_angle: int):
    
    for engine in engineList:
        if id == engine.engineId:   
            if engine.type == 180:
                if mode_angle >= 0 and mode_angle <= 180:
                    try:
                        i2cRequest = bytearray()
                        engine.angle = mode_angle
                        i2cRequest.append(engine.engineId)
                        i2cRequest.append(engine.angle)
                        i2cRequest.append(255)
                        i2c_bus.write_i2c_block_data(device_address, 0, i2cRequest)
                        i2cRequest.clear()
                    except:
                        raise HTTPException(status_code=503, detail="I2C device error")
                    return engine
                else:
                    raise HTTPException(status_code=400, detail="Wrong angle value (0-180)")
            elif engine.type == 360:
                if mode_angle == -1:
                    try:
                        i2cRequest = bytearray()
                        engine.mode = -1
                        i2cRequest.append(engine.engineId)
                        i2cRequest.append(181)
                        i2cRequest.append(255)
                        i2c_bus.write_i2c_block_data(device_address, 0, i2cRequest)
                        i2cRequest.clear()
                    except:
                        raise HTTPException(status_code=503, detail="I2C device error")
                    return engine
                elif mode_angle == 0:
                    try:
                        i2cRequest = bytearray()
                        engine.mode = 0
                        i2cRequest.append(engine.engineId)
                        i2cRequest.append(182)
                        i2cRequest.append(255)
                        i2c_bus.write_i2c_block_data(device_address, 0, i2cRequest)
                        i2cRequest.clear()
                    except:
                        raise HTTPException(status_code=503, detail="I2C device error")
                    return engine
                elif mode_angle == 1:
                    try:
                        i2cRequest = bytearray()
                        engine.mode = 1
                        i2cRequest.append(engine.engineId)
                        i2cRequest.append(183)
                        i2cRequest.append(255)
                        i2c_bus.write_i2c_block_data(device_address, 0, i2cRequest)
                        i2cRequest.clear()
                    except:
                        raise HTTPException(status_code=503, detail="I2C device error")
                    return engine
                else:
                    raise HTTPException(status_code=400, detail="Wrong mode set (-1, 0 ,1)")
            else:
                print(engine.type)
                raise HTTPException(status_code=400, detail="Unsupported servo type")
@app.delete("/engines/{id}", status_code=204)
async def delete_engine(id: int):
    for engine in engineList:
        if id == engine.engineId:
            engineList.remove(engine)
            return None
    raise HTTPException(status_code=404, detail="Engine with this id not exist")
