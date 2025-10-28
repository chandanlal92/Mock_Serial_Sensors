# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 23:15:20 2025

@author: Admin
"""
import asyncio
from Sensor import Sensor
from SensorManager import SensorManager
from SerialWriter import SerialWriter
from SerialReader import SerialReader
from KeyPressHandler import keyPressHandler
import yaml

with open("../Config/SensorConfig.yaml", 'r') as config_file:
    config = yaml.safe_load(config_file)

READ_PORT=config["Serial"]["ReadPort"]
WRITE_PORT=config["Serial"]["WritePort"]
BAUDRATE=config["Serial"]["BaudRate"]
INTERVAL=config["Serial"]["Interval"]

"""SerialApp orchestrates the SerialReader and SerialWriter components along with sensor management.
   Parameters:
   - read_port: Serial port for reading data.
   - write_port: Serial port for writing data.
   Methods:
   - run(): Asynchronous method to run the application until a stop event is triggered.
"""
class SerialApp:   
    def __init__(self,read_port:str,write_port:str):
        self.stop_event=asyncio.Event()
        # Sensor_Setup
        self.sensor_manager=SensorManager()
        for sensor_cfg in config["Sensors"]:
            sensor = Sensor(
                name=sensor_cfg["Name"],
                min_val=float(sensor_cfg["Min"]),
                max_val=float(sensor_cfg["Max"]),
                unit=sensor_cfg["Unit"]
            )
            self.sensor_manager.add_sensors(sensor)
        # Components
        self.reader=SerialReader(port=read_port,baudrate=BAUDRATE)
        self.writer=SerialWriter(port=write_port,manager=self.sensor_manager,
                                 baudrate=BAUDRATE, interval=INTERVAL)  
        self.keypress=keyPressHandler(self.stop_event)       

    async def run(self):
        tasks=[
            asyncio.create_task(self.reader.start(self.stop_event)),
            asyncio.create_task(self.writer.start(self.stop_event)),
            asyncio.create_task(self.keypress.monitor())
            ]
        await self.stop_event.wait()

        print("\n [System] Stop signal received. Cancelling tasks...")
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks,return_exceptions=True)
        print("[System] Shutdown complete")

if __name__=="__main__":
    app=SerialApp(read_port=READ_PORT,write_port=WRITE_PORT)
    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        print("[System] Interrupted Manually")