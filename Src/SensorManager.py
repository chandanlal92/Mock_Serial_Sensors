# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 22:14:22 2025

@author: Admin
"""

from datetime import datetime
from Sensor import Sensor

"""SensorManager manages multiple Sensor instances and generates combined data readings.
   Methods:
   - add_sensors(sensor): Adds a Sensor instance to the manager.
   - generate_all_data(): Generates a formatted string of all sensor data readings.
"""
class SensorManager:
    def __init__(self):
        self.sensors = []

    def add_sensors(self, sensor: Sensor):
        self.sensors.append(sensor)

    def generate_all_data(self):
        """Combining all Sensors into one formatted line."""
        timestamp = datetime.now().isoformat()
        readings = [sensor.generate_data() for sensor in self.sensors]
        return f"{timestamp}," + ",".join(readings) + " \n"

