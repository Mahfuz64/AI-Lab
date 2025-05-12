import pygame
from city import grid_to_pixel, CELL_SIZE
from vehicle_types import VehicleType, VehicleProperties
import random
import math

DEFAULT_SPEEDS = {
    VehicleType.CAR: 2.0,
    VehicleType.BUS: 1.5,
    VehicleType.EMERGENCY: 2.5,
    VehicleType.TRUCK: 1.2,
    VehicleType.MOTORCYCLE: 2.2
}
DEFAULT_LANES = 1

class Car:
    def __init__(self, path, vehicle_type, _unused=None):
        self.path = path
        self.index = 0
        self.x, self.y = grid_to_pixel(*self.path[0])
        self.properties = VehicleProperties(vehicle_type)
        self.current_speed = 0
        self.target_speed = DEFAULT_SPEEDS.get(vehicle_type, 2.0)
        self.wait_time = 0
        self.is_waiting = False
        self.current_lane = 0
        self.lane_change_timer = 0
        self.bus_stop_wait_time = 0
        self.is_at_bus_stop = False
        self.emergency_mode = False

    def move(self, traffic_lights, cars):
        if self.index >= len(self.path) - 1:
            return

        next_cell = self.path[self.index + 1]

    
        if self.properties.type == VehicleType.EMERGENCY:
            self._handle_emergency_behavior(cars)

      
        if self.properties.type == VehicleType.BUS:
            self._handle_bus_behavior()

       
        if self.should_stop_for_red(next_cell, traffic_lights):
            self.is_waiting = True
            self.wait_time += 1
            self._decelerate()
            return

        self.is_waiting = False

        if DEFAULT_LANES > 1:
            self._handle_lane_changing(cars)

        self._adjust_speed()

        target_x, target_y = grid_to_pixel(*next_cell)
        dx = target_x - self.x
        dy = target_y - self.y
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist < self.current_speed:
            self.index += 1
            self.x, self.y = target_x, target_y
        else:
            self.x += self.current_speed * (dx / dist)
            self.y += self.current_speed * (dy / dist)

    def _handle_emergency_behavior(self, cars):
        self.emergency_mode = True
        for car in cars:
            if car != self and self._is_nearby(car, 3):
                car._yield_to_emergency()

    def _handle_bus_behavior(self):
        pass

    def _handle_lane_changing(self, cars):
        self.lane_change_timer -= 1
        if self.lane_change_timer <= 0:
            if self._can_change_lane(cars):
                self.current_lane = 1 - self.current_lane
            self.lane_change_timer = 60

    def _can_change_lane(self, cars):
        for car in cars:
            if car != self and self._is_nearby(car, 2):
                return False
        return True

    def _adjust_speed(self):
        target_speed = self.target_speed
        if self.current_speed < target_speed:
            self.current_speed = min(self.current_speed + self.properties.acceleration, target_speed)
        elif self.current_speed > target_speed:
            self.current_speed = max(self.current_speed - self.properties.deceleration, target_speed)

    def _decelerate(self):
        self.current_speed = max(0, self.current_speed - self.properties.deceleration)

    def _yield_to_emergency(self):
        self.current_speed = max(0, self.current_speed - self.properties.deceleration * 2)

    def _is_nearby(self, other_car, distance):
        return (abs(self.x - other_car.x) < CELL_SIZE * distance and 
                abs(self.y - other_car.y) < CELL_SIZE * distance)

    def should_stop_for_red(self, cell, traffic_lights):
        for light in traffic_lights:
            if (light.row, light.col) == cell and not light.is_green:
                if self.properties.type == VehicleType.EMERGENCY:
                    return False
                return True
        return False

    def draw(self, screen):
        size = CELL_SIZE * self.properties.size
        pygame.draw.rect(screen, (128, 0, 32), 
                        (self.x + (CELL_SIZE - size)/2, 
                         self.y + (CELL_SIZE - size)/2, 
                         size, size))
        
        if self.is_waiting:
            pygame.draw.circle(screen, (255, 255, 0), 
                             (int(self.x + CELL_SIZE - 10), int(self.y + 10)), 3)
        
        if self.properties.type == VehicleType.EMERGENCY and self.emergency_mode:
            self._draw_emergency_lights(screen)
        
        if self.properties.type == VehicleType.BUS and self.is_at_bus_stop:
            pygame.draw.circle(screen, (0, 0, 255), 
                             (int(self.x + 10), int(self.y + 10)), 3)

    def _draw_emergency_lights(self, screen):
        if pygame.time.get_ticks() % 500 < 250:  # Flash every 500ms
            pygame.draw.circle(screen, (255, 0, 0), 
                             (int(self.x + 5), int(self.y + 5)), 3)
            pygame.draw.circle(screen, (0, 0, 255), 
                             (int(self.x + CELL_SIZE - 5), int(self.y + 5)), 3)
