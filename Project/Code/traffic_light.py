import pygame
from city import grid_to_pixel
import numpy as np
from vehicle_types import VehicleType

GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
CELL_SIZE = 40

class TrafficLight:
    def __init__(self, row, col, interval=3000):
        self.row = row
        self.col = col
        self.interval = interval
        self.is_green = True
        self.timer = 0
        self.car_count = 0
        self.emergency_count = 0
        self.last_switch = 0
        self.min_green_time = 2000
        self.max_green_time = 8000  
        self.yellow_time = 500
        self.is_yellow = False
        self.phase = 0 
        self.coordinated = False
        self.coordination_group = None
        self.congestion_threshold = 3 
        self.adaptive_timing = True

    def update(self, dt, cars):
        self.timer += dt
        self.update_car_count(cars)
        
        if self.emergency_count > 0:
            self._handle_emergency()
            return

        if self.is_yellow:
            if self.timer >= self.yellow_time:
                self.is_yellow = False
                self.is_green = not self.is_green
                self.timer = 0
            return

        if self.adaptive_timing:
            self._adaptive_timing(cars)
        else:
            if self.timer >= self.min_green_time:
                if self.should_switch(cars):
                    self._initiate_switch()
                elif self.timer >= self.max_green_time:
                    self._initiate_switch()

    def _adaptive_timing(self, cars):
        current_direction_cars = self._get_current_direction_cars(cars)
        perpendicular_cars = self._get_perpendicular_cars(cars)
        
        current_density = len(current_direction_cars)
        perpendicular_density = len(perpendicular_cars)
        
        if self.is_green:
            if current_density == 0 and perpendicular_density >= self.congestion_threshold:
                self._initiate_switch()
            elif self.timer >= self.min_green_time:
                if current_density < perpendicular_density and self.timer >= self.min_green_time * 1.5:
                    self._initiate_switch()
                elif self.timer >= self.max_green_time:
                    self._initiate_switch()
        else:
            if perpendicular_density == 0 and current_density >= self.congestion_threshold:
                self._initiate_switch()
            elif self.timer >= self.min_green_time:
                if perpendicular_density < current_density and self.timer >= self.min_green_time * 1.5:
                    self._initiate_switch()
                elif self.timer >= self.max_green_time:
                    self._initiate_switch()

    def _get_current_direction_cars(self, cars):
        current_direction_cars = []
        for car in cars:
            if self._is_current_direction_approach(car):
                current_direction_cars.append(car)
        return current_direction_cars

    def _is_current_direction_approach(self, car):
        if car.index >= len(car.path) - 1:
            return False
        
        current_pos = car.path[car.index]
        next_pos = car.path[car.index + 1]
        
        if self.phase == 0: 
            return abs(next_pos[0] - self.row) >= abs(next_pos[1] - self.col)
        else: 
            return abs(next_pos[0] - self.row) <= abs(next_pos[1] - self.col)

    def should_switch(self, cars):
        current_direction_cars = self._get_current_direction_cars(cars)
        perpendicular_cars = self._get_perpendicular_cars(cars)
        
        return len(perpendicular_cars) > len(current_direction_cars)

    def _initiate_switch(self):
        self.is_yellow = True
        self.timer = 0
        if self.coordinated:
            self._notify_coordination_group()

    def _handle_emergency(self):
        if not self.is_green:
            self.is_green = True
            self.timer = 0
            self.is_yellow = False

    def update_car_count(self, cars):
        self.car_count = 0
        self.emergency_count = 0
        for car in cars:
            if self.is_car_approaching(car):
                self.car_count += 1
                if car.properties.type == VehicleType.EMERGENCY:
                    self.emergency_count += 1

    def is_car_approaching(self, car):
        if car.index >= len(car.path) - 1:
            return False
        
        current_pos = car.path[car.index]
        next_pos = car.path[car.index + 1]
        
        dist = abs(current_pos[0] - self.row) + abs(current_pos[1] - self.col)
        return dist <= 3

    def _check_perpendicular_traffic(self, cars):
        perpendicular_cars = 0
        for car in self._get_perpendicular_cars(cars):
            if self.is_car_approaching(car):
                perpendicular_cars += 1
        return perpendicular_cars > self.car_count * 1.5

    def _get_perpendicular_cars(self, cars):
        perpendicular_cars = []
        for car in cars:
            if self._is_perpendicular_approach(car):
                perpendicular_cars.append(car)
        return perpendicular_cars

    def _is_perpendicular_approach(self, car):
        if car.index >= len(car.path) - 1:
            return False
        
        current_pos = car.path[car.index]
        next_pos = car.path[car.index + 1]
        
        if self.phase == 0: 
            return abs(next_pos[0] - self.row) < abs(next_pos[1] - self.col)
        else: 
            return abs(next_pos[0] - self.row) > abs(next_pos[1] - self.col)

    def set_coordination_group(self, group):
        self.coordinated = True
        self.coordination_group = group

    def _notify_coordination_group(self):
        if self.coordination_group:
            self.coordination_group.notify_light_change(self)

    def draw(self, screen):
        x, y = grid_to_pixel(self.row, self.col)
        
        if self.is_yellow:
            color = YELLOW
        else:
            color = GREEN if self.is_green else RED
            
        pygame.draw.circle(screen, color, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 6)
        
        font = pygame.font.Font(None, 20)
        text = font.render(str(self.car_count), True, (0, 0, 0))
        screen.blit(text, (x + CELL_SIZE // 2 - 5, y + CELL_SIZE // 2 + 10))
        
        if self.is_yellow:
            time_left = int((self.yellow_time - self.timer) / 1000)
        else:
            if self.is_green:
                time_left = int((self.max_green_time - self.timer) / 1000)
            else:
                time_left = int((self.max_green_time - self.timer) / 1000)
        time_text = font.render(f"{max(time_left,0)}s", True, (0, 0, 0))
        screen.blit(time_text, (x + CELL_SIZE // 2 - 10, y + CELL_SIZE // 2 - 25))
        
        if self.emergency_count > 0:
            pygame.draw.circle(screen, (255, 0, 0), (x + CELL_SIZE // 2, y + CELL_SIZE // 2 - 15), 3)

class TrafficLightGroup:
    def __init__(self):
        self.lights = []
        self.phase = 0
        self.timer = 0
        self.interval = 5000

    def add_light(self, light):
        self.lights.append(light)
        light.set_coordination_group(self)

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.interval:
            self.phase = 1 - self.phase
            self.timer = 0
            for light in self.lights:
                light.phase = self.phase

    def notify_light_change(self, light):
        for other_light in self.lights:
            if other_light != light:
                other_light.phase = light.phase
                other_light.timer = 0
