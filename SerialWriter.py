# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 20:34:16 2025

@author: Admin
"""

import asyncio
import serial_asyncio
from SensorManager import SensorManager

"""SerialWriter handles sending sensor data over a serial port at regular intervals.
   Parameters:
   - port: Serial port to write to.
    - manager: SensorManager instance to generate sensor data.
    - baudrate: Communication speed (default 115200).
    - interval: Time interval between data sends (default 1.0 seconds).
    Methods:    
    - start(stop_event): Asynchronous method to start sending data until stop_event is set.
"""
class SerialWriter():
    def __init__(self,port:str,manager:SensorManager,baudrate: int=115200,interval: float=1.0):
        self.port=port
        self.baudrate=baudrate
        self.interval=interval
        self.manager=manager
        self.writer=None
    
    async def start(self,stop_event:asyncio.Event):
        _, self.writer = await serial_asyncio.open_serial_connection(url=self.port, baudrate=self.baudrate)
        print(f"Started writing to {self.port}...\n")
        try:
            while not stop_event.is_set():
                data_line=self.manager.generate_all_data()
                msg = f"Message,{data_line}\n"
                self.writer.write(msg.encode())
                await self.writer.drain()
                print(f"Sent,{msg.strip()}")
                
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            pass
        finally:
            print("Closing serial writer...")
            self.writer.close()
            await self.writer.wait_closed()
            print("Serial writer closed.")