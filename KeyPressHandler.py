# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 22:15:21 2025

@author: Admin
"""

import msvcrt
import asyncio

"""KeyPressHandler monitors key presses to control the simulator.
   Parameters:
    - stop_event: An asyncio.Event to signal stopping the simulator.
   Methods:
    - monitor(): Asynchronous method to monitor key presses and set stop_event when 'q' is pressed or Ctrl+C is detected.
"""
class keyPressHandler:
    def __init__(self, stop_event: asyncio.Event):
        self.stop_event=stop_event
        
    async def monitor(self):
        """Monitors key press to stop the simulator"""
        print("Print q or ctrl+c to stop to stop the simulation")
        try:
            while not self.stop_event.is_set():
                await asyncio.sleep(0.1)
                if msvcrt.kbhit():
                    key=msvcrt.getch().decode().lower()
                    if key== 'q':
                        print("Simulator is stopped by key press...\n")
                        self.stop_event.set()             
        except KeyboardInterrupt:
            self.stop_event.set()
        finally:
            print("KeyPressHandler stopped.")