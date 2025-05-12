from enum import Enum
import pygame

class VehicleType(Enum):
    CAR = 1
    BUS = 2
    EMERGENCY = 3
    TRUCK = 4
    MOTORCYCLE = 5

class VehicleProperties:
    def __init__(self, vehicle_type):
        self.type = vehicle_type
        self.set_properties()

    def set_properties(self):
        if self.type == VehicleType.CAR:
            self.speed = 2
            self.size = 0.8
            self.color = (255, 0, 0)  
            self.priority = 1
            self.acceleration = 0.1
            self.deceleration = 0.2
        elif self.type == VehicleType.BUS:
            self.speed = 1.5
            self.size = 1.0
            self.color = (0, 0, 255) 
            self.priority = 2
            self.acceleration = 0.05
            self.deceleration = 0.1
        elif self.type == VehicleType.EMERGENCY:
            self.speed = 3
            self.size = 0.9
            self.color = (255, 255, 0) 
            self.priority = 3
            self.acceleration = 0.2
            self.deceleration = 0.3
        elif self.type == VehicleType.TRUCK:
            self.speed = 1.2
            self.size = 1.2
            self.color = (128, 128, 128) 
            self.priority = 1
            self.acceleration = 0.03
            self.deceleration = 0.08
        elif self.type == VehicleType.MOTORCYCLE:
            self.speed = 2.5
            self.size = 0.6
            self.color = (0, 255, 0) 
            self.priority = 1
            self.acceleration = 0.15
            self.deceleration = 0.25

    def get_light_color(self):
        if self.type == VehicleType.EMERGENCY:
            return (255, 0, 0) 
        return self.color 