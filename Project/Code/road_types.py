from enum import Enum
import random

class RoadType(Enum):
    HIGHWAY = 1
    MAIN_ROAD = 2
    LOCAL_STREET = 3
    BUS_LANE = 4

class RoadProperties:
    def __init__(self, road_type):
        self.type = road_type
        self.set_properties()

    def set_properties(self):
        if self.type == RoadType.HIGHWAY:
            self.speed_limit = 3
            self.lanes = 2
            self.color = (40, 40, 40) 
            self.allow_emergency = True
            self.allow_trucks = True
            self.allow_buses = True
        elif self.type == RoadType.MAIN_ROAD:
            self.speed_limit = 2
            self.lanes = 1
            self.color = (60, 60, 60) 
            self.allow_emergency = True
            self.allow_trucks = True
            self.allow_buses = True
        elif self.type == RoadType.LOCAL_STREET:
            self.speed_limit = 1
            self.lanes = 1
            self.color = (80, 80, 80)  
            self.allow_emergency = True
            self.allow_trucks = False
            self.allow_buses = False
        elif self.type == RoadType.BUS_LANE:
            self.speed_limit = 1.5
            self.lanes = 1
            self.color = (0, 0, 128) 
            self.allow_emergency = True
            self.allow_trucks = False
            self.allow_buses = True

class CityLayout:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.intersections = []
        self.bus_stops = []
        self.emergency_stations = []

    def generate_layout(self):
        self._generate_highways()
        self._generate_main_roads()
        self._generate_local_streets()
        self._generate_bus_lanes()
        self._generate_intersections()
        self._generate_bus_stops()
        self._generate_emergency_stations()

    def _generate_highways(self):
        for row in [3, 11]:
            for col in range(self.width):
                self.grid[row][col] = RoadProperties(RoadType.HIGHWAY)
        
        for col in [4, 12]:
            for row in range(self.height):
                self.grid[row][col] = RoadProperties(RoadType.HIGHWAY)

    def _generate_main_roads(self):
        for row in [7]:
            for col in range(self.width):
                if self.grid[row][col] is None:
                    self.grid[row][col] = RoadProperties(RoadType.MAIN_ROAD)

    def _generate_local_streets(self):
        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row][col] is None:
                    self.grid[row][col] = RoadProperties(RoadType.LOCAL_STREET)

    def _generate_bus_lanes(self):
        for row in [7]:
            for col in range(self.width):
                if random.random() < 0.3: 
                    self.grid[row][col] = RoadProperties(RoadType.BUS_LANE)

    def _generate_intersections(self):
        for row in range(1, self.height-1):
            for col in range(1, self.width-1):
                if (self.grid[row][col] is not None and
                    self.grid[row-1][col] is not None and
                    self.grid[row+1][col] is not None and
                    self.grid[row][col-1] is not None and
                    self.grid[row][col+1] is not None):
                    self.intersections.append((row, col))

    def _generate_bus_stops(self):
        for row in range(self.height):
            for col in range(self.width):
                if (self.grid[row][col] is not None and
                    self.grid[row][col].type == RoadType.BUS_LANE and
                    random.random() < 0.2): 
                    self.bus_stops.append((row, col))

    def _generate_emergency_stations(self):
        for _ in range(3):  
            row = random.randint(0, self.height-1)
            col = random.randint(0, self.width-1)
            if self.grid[row][col] is not None:
                self.emergency_stations.append((row, col))

    def get_road_type(self, row, col):
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.grid[row][col]
        return None

    def is_valid_position(self, row, col):
        return (0 <= row < self.height and 
                0 <= col < self.width and 
                self.grid[row][col] is not None) 