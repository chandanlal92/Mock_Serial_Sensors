# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 22:14:12 2025

@author: Admin
"""

import asyncio
import serial_asyncio
import aiofiles
from datetime import datetime

class SerialReader:
    def __init__(self,port:str,baudrate:int=9600,log_file:str="serial_output.txt"):
        self.port=port
        self.baudrate=baudrate
        self.log_file=log_file
        self.writer=None
        self.reader=None

    async def start(self,stop_event:asyncio.Event):
        self.reader,self.writer=await serial_asyncio.open_serial_connection(url=self.port, baudrate=self.baudrate)
        async with aiofiles.open(self.log_file,'a')as f:
            try:
                while not stop_event.is_set():
                    line=await self.reader.readline()
                    if line:
                        text=line.decode('utf-8', errors='ignore').strip()
                        timestamp=datetime.now().isoformat()
                        print(f"[Reader] Received:{text} at {timestamp}")
                        await f.write(text+"\n")
                        await f.flush()
            except asyncio.CancelledError:
                pass
            finally:
                print("[Reader] Closing Serial port...")
                self.writer.close()
                await self.writer.wait_closed()
                print("[Reader] Serial port closed.")