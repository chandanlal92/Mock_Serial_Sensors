# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 20:22:53 2025

@author: Admin
"""

import random
from datetime import datetime
import asyncio


"""Sensor simulates a Sensor by producing periodic readings
    
   Parameters:  
    - name: Name of the sensor. 
        - min_val: Minimum value the sensor can produce.
        - max_val: Maximum value the sensor can produce.
        - unit: Unit of measurement for the sensor value (default "units").
    Methods:
        - generate_data(): Generates sensor reading asynchronously.
"""


class Sensor:
    """Simulates a Sensor by producing periodic readings"""
    def __init__(self,name:str,min_val:float,max_val:float,unit:str="units"):
        self.name=name
        self.min_val=min_val
        self.max_val=max_val
        self.unit=unit     

    def generate_data(self):
       """Generates sensor reading asynchronously."""
      
       value=round(random.uniform(self.min_val, self.max_val),2)
       return f"{self.name},{value},{self.unit}"
   
    