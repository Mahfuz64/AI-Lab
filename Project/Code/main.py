import pygame
import sys
import random
from collections import deque
from city import generate_road_map, get_road_cells, get_intersections, grid_to_pixel, CELL_SIZE, GRID_WIDTH, GRID_HEIGHT
from traffic_light import TrafficLight, TrafficLightGroup
from car import Car
from vehicle_types import VehicleType
import heapq
import numpy as np
from collections import defaultdict
from sklearn.cluster import KMeans

pygame.init()
SIDE_PANEL_WIDTH = 220
screen = pygame.display.set_mode((CELL_SIZE * GRID_WIDTH + SIDE_PANEL_WIDTH, CELL_SIZE * GRID_HEIGHT))
pygame.display.set_caption("Smart City Traffic System")

WHITE = (255, 255, 255)
BG_COLOR = (200, 200, 200)
DASHBOARD_COLOR = (240, 240, 240)
TEXT_COLOR = (0, 0, 0)

road_map = generate_road_map()
intersections = get_intersections(road_map)
road_cells = get_road_cells(road_map)

INTERSECTION_COLORS = [
    (0, 0, 200), (200, 0, 0), (0, 150, 0), (200, 100, 0), (150, 0, 150), (0, 150, 150)
]
def color_intersections(intersections):
    adj = {pt: [] for pt in intersections}
    for (r, c) in intersections:
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nbr = (r+dr, c+dc)
            if nbr in adj:
                adj[(r, c)].append(nbr)
    colors = {}
    for node in intersections:
        used = {colors[nbr] for nbr in adj[node] if nbr in colors}
        for i, color in enumerate(INTERSECTION_COLORS):
            if i not in used:
                colors[node] = i
                break
    return colors

intersection_colors = color_intersections(intersections)

is_valid_position = lambda r, c: 0 <= r < GRID_HEIGHT and 0 <= c < GRID_WIDTH and road_map[r][c] == 1

random.seed(42)
bus_stops = random.sample(intersections, min(8, len(intersections)))
emergency_stations = random.sample([pt for pt in intersections if pt not in bus_stops], min(3, len(intersections)-len(bus_stops)))

traffic_light_groups = []
color_groups = defaultdict(list)
for intersection, color in intersection_colors.items():
    color_groups[color].append(intersection)

for color, intersections in color_groups.items():
    group = TrafficLightGroup()
    for row, col in intersections:
        light = TrafficLight(row, col)
        group.add_light(light)
    traffic_light_groups.append(group)

cars = []
MAX_CARS = 60
SPAWN_INTERVAL = 500

class Dashboard:
    def __init__(self):
        self.completed = 0
        self.total = 0
        self.avg_wait = 0
    def update(self, cars, completed_cars):
        self.completed += len(completed_cars)
        self.total = self.completed + len(cars)
        waits = [car.wait_time for car in cars if hasattr(car, 'wait_time')]
        self.avg_wait = sum(waits) / len(waits) if waits else 0
    def draw(self, screen):
        font = pygame.font.Font(None, 24)
        x = CELL_SIZE * GRID_WIDTH + 10
        y = 10
        screen.blit(font.render(f"Dashboard", True, (0,0,0)), (x, y))
        y += 30
        screen.blit(font.render(f"Cars: {self.total}", True, (0,0,0)), (x, y))
        y += 25
        screen.blit(font.render(f"Completed: {self.completed}", True, (0,0,0)), (x, y))
        y += 25
        screen.blit(font.render(f"Avg Wait: {self.avg_wait:.1f}s", True, (0,0,0)), (x, y))

dashboard = Dashboard()

class IntersectionPanel:
    def __init__(self, intersections, traffic_lights):
        self.intersections = intersections
        self.traffic_lights = traffic_lights
    def update(self, intersections, traffic_lights):
        self.intersections = intersections
        self.traffic_lights = traffic_lights
    def draw(self, screen):
        font = pygame.font.Font(None, 20)
        x = CELL_SIZE * GRID_WIDTH + 10
        y = 140
        screen.blit(font.render("Intersections", True, (0,0,0)), (x, y))
        y += 20
        for light in self.traffic_lights[:6]:
            status = "G" if light.is_green else "R"
            screen.blit(font.render(f"({light.row},{light.col}): {status} {light.car_count}", True, (0,0,0)), (x, y))
            y += 18

all_traffic_lights = [light for group in traffic_light_groups for light in group.lights]
intersection_panel = IntersectionPanel(intersections, all_traffic_lights)

font_btn = pygame.font.Font(None, 24)

class RouteInfoPanel:
    def __init__(self, font):
        self.length = 0
        self.congestion = 0
        self.avg_congestion = 0
    def update(self, path, traffic_lights, car_counts=None):
        self.length = len(path) if path else 0
        if path and car_counts:
            self.congestion = sum(car_counts.get(cell, 0) for cell in path)
            self.avg_congestion = self.congestion / self.length if self.length else 0
        else:
            self.congestion = 0
            self.avg_congestion = 0
    def draw(self, screen, x, y):
        font = pygame.font.Font(None, 20)
        screen.blit(font.render("Route Info", True, (0,0,0)), (x, y))
        y += 20
        screen.blit(font.render(f"Length: {self.length}", True, (0,0,0)), (x, y))
        y += 18
        screen.blit(font.render(f"Congestion: {self.congestion}", True, (0,0,0)), (x, y))
        y += 18
        screen.blit(font.render(f"Avg Congestion: {self.avg_congestion:.2f}", True, (0,0,0)), (x, y))

route_info_panel = RouteInfoPanel(font_btn)

class MiniMapPanel:
    def __init__(self):
        pass
    def update(self, *args, **kwargs):
        pass
    def draw(self, screen, intersections, path, intersection_clusters, cluster_colors):
        x0 = CELL_SIZE * GRID_WIDTH + 10
        y0 = 320
        w = 120
        h = 60
        pygame.draw.rect(screen, (220,220,220), (x0, y0, w, h))
        scale_x = w / GRID_WIDTH
        scale_y = h / GRID_HEIGHT
        for (r, c) in intersections:
            pygame.draw.rect(screen, (80,80,80), (x0 + c*scale_x, y0 + r*scale_y, scale_x, scale_y))
        for (r, c) in path:
            pygame.draw.rect(screen, (255,255,0), (x0 + c*scale_x, y0 + r*scale_y, scale_x, scale_y))

mini_map_panel = MiniMapPanel()

def iterative_deepening_search(start, goal, road_map, traffic_analyzer, max_depth=50):
    def depth_limited_search(node, goal, depth, visited, path):
        node = tuple(node)  
        if depth == 0:
            return None
        if node == goal:
            return path
        
        visited.add(node)
        row, col = node
        
        neighbors = []
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < len(road_map) and 
                0 <= new_col < len(road_map[0]) and 
                road_map[new_row][new_col] == 1 and 
                (new_row, new_col) not in visited):
                traffic_cost = traffic_analyzer.get_traffic_level((new_row, new_col))
                neighbors.append(((new_row, new_col), traffic_cost))
        
        neighbors.sort(key=lambda x: x[1])
        
        for new_node, _ in neighbors:
            result = depth_limited_search(new_node, goal, depth - 1, visited, path + [new_node])
            if result is not None:
                return result
        
        visited.remove(node)
        return None
    
    for depth in range(1, max_depth + 1):
        result = depth_limited_search(start, goal, depth, set(), [start])
        if result is not None:
            return result
    
    return None

def find_route(start, goal, road_map, traffic_analyzer):
    return iterative_deepening_search(start, goal, road_map, traffic_analyzer)

def get_alternative_routes(start, end, is_valid_position, num_routes=3):
    routes = []
    for _ in range(num_routes):
        path = find_route(start, end, road_map, traffic_analyzer)
        if not path:
            break
        if path not in routes:
            routes.append(path)
        random.shuffle(intersections)
    return routes

def spawn_vehicle():
    if len(cars) >= MAX_CARS or not intersections:
        return None
    vehicle_type = random.choices(
        [VehicleType.CAR, VehicleType.BUS, VehicleType.EMERGENCY, VehicleType.TRUCK, VehicleType.MOTORCYCLE],
        weights=[0.7, 0.1, 0.05, 0.1, 0.05]
    )[0]
    if vehicle_type == VehicleType.BUS and bus_stops:
        start = random.choice(bus_stops)
    elif vehicle_type == VehicleType.EMERGENCY and emergency_stations:
        start = random.choice(emergency_stations)
    else:
        start = random.choice(intersections)
    end = random.choice(intersections)
    while end == start:
        end = random.choice(intersections)
    path = find_route(start, end, road_map, traffic_analyzer)
    if path:
        return Car(path, vehicle_type, None)
    return None

clock = pygame.time.Clock()
last_spawn = pygame.time.get_ticks()
running = True

selected_start = None
selected_end = None
suggested_paths = []
current_path_index = 0

class UIButton:
    def __init__(self, rect, text, font, color=(180,180,255), text_color=(0,0,0)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (100,100,200), self.rect, 2)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

clear_btn = UIButton((CELL_SIZE * GRID_WIDTH + 220, 20, 120, 36), "Clear Route", font_btn)
mode_btn = UIButton((CELL_SIZE * GRID_WIDTH + 220, 60, 120, 36), "Mode: IDS", font_btn)

def draw_legend(screen):
    font = pygame.font.Font(None, 18)
    x = CELL_SIZE * GRID_WIDTH + 10
    y = 400
    screen.blit(font.render("Legend:", True, (0,0,0)), (x, y))
    y += 18
    pygame.draw.rect(screen, (80,80,80), (x, y, 18, 18))
    screen.blit(font.render("= Free", True, (0,0,0)), (x+24, y))
    y += 20
    pygame.draw.rect(screen, (200,200,80), (x, y, 18, 18))
    screen.blit(font.render("= Light", True, (0,0,0)), (x+24, y))
    y += 20
    pygame.draw.rect(screen, (255,140,0), (x, y, 18, 18))
    screen.blit(font.render("= Medium", True, (0,0,0)), (x+24, y))
    y += 20
    pygame.draw.rect(screen, (220,0,0), (x, y, 18, 18))
    screen.blit(font.render("= Heavy", True, (0,0,0)), (x+24, y))

class TrafficAnalyzer:
    def __init__(self, n_clusters=3):
        self.n_clusters = n_clusters
        self.cluster_centers = []
        self.traffic_density = {}
        
    def update_traffic_density(self, intersections, vehicles):
        for intersection in intersections:
            nearby_vehicles = sum(
                1 for v in vehicles
                if 0 <= v.index < len(v.path)
                and abs(v.path[v.index][0] - intersection[0]) <= 2
                and abs(v.path[v.index][1] - intersection[1]) <= 2
            )
            self.traffic_density[intersection] = nearby_vehicles
        
        if len(intersections) >= self.n_clusters:
            self._custom_kmeans(intersections)
            
    def _custom_kmeans(self, intersections):
        if not self.cluster_centers:
            self.cluster_centers = random.sample(intersections, self.n_clusters)
        
        for _ in range(10):
            clusters = {center: [] for center in self.cluster_centers}
            for point in intersections:
                if point not in self.traffic_density:
                    continue
                closest = min(self.cluster_centers,
                            key=lambda center: abs(center[0]-point[0]) + abs(center[1]-point[1]))
                clusters[closest].append(point)
            
            new_centers = []
            for center, points in clusters.items():
                if points:
                    total_weight = sum(self.traffic_density.get(p, 0) for p in points)
                    if total_weight > 0:
                        mean_row = sum(p[0]*self.traffic_density.get(p, 0) for p in points)/total_weight
                        mean_col = sum(p[1]*self.traffic_density.get(p, 0) for p in points)/total_weight
                        new_center = min(points,
                                       key=lambda p: abs(p[0]-mean_row) + abs(p[1]-mean_col))
                        new_centers.append(new_center)
                    else:
                        new_centers.append(center)
                else:
                    new_centers.append(center)
            
           
            if set(new_centers) == set(self.cluster_centers):
                break
                
            self.cluster_centers = new_centers
    
    def get_traffic_level(self, intersection):
        if intersection not in self.traffic_density:
            return 0
        
       
        if not self.cluster_centers:
            return self.traffic_density[intersection]
        
        closest = min(self.cluster_centers,
                    key=lambda center: abs(center[0]-intersection[0]) + abs(center[1]-intersection[1]))
        
      
        cluster_density = sum(self.traffic_density.get(p, 0) 
                            for p in self.traffic_density 
                            if min(self.cluster_centers,
                                 key=lambda c: abs(c[0]-p[0]) + abs(c[1]-p[1])) == closest)
        
        avg_cluster_density = cluster_density / len([p for p in self.traffic_density 
                                                   if min(self.cluster_centers,
                                                        key=lambda c: abs(c[0]-p[0]) + abs(c[1]-p[1])) == closest]) if cluster_density else 0
        
        return int(self.traffic_density[intersection] * (avg_cluster_density / 10 if avg_cluster_density > 10 else 1))

traffic_analyzer = TrafficAnalyzer()

while running:
    dt = clock.tick(60)
    screen.fill(BG_COLOR)

    car_counts = defaultdict(int)
    for car in cars:
        if 0 <= car.index < len(car.path):
            cell = car.path[car.index]
            car_counts[cell] += 1

    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            road = road_map[row][col]
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if (row, col) in intersections:
                color = INTERSECTION_COLORS[intersection_colors[(row, col)] % len(INTERSECTION_COLORS)]
            elif road == 1:
                color = (80, 80, 80) 
            else:
                color = (255, 255, 255) 
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (180, 180, 180), rect, 1)

    for group in traffic_light_groups:
        for light in group.lights:
            x, y = grid_to_pixel(light.row, light.col)
            color = (0, 200, 0) if light.is_green else (200, 0, 0)
            pygame.draw.circle(screen, color, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2)
            font = pygame.font.Font(None, 18)
            if light.is_yellow:
                time_left = int((light.yellow_time - light.timer) / 1000)
            else:
                time_left = int((light.max_green_time - light.timer) / 1000)
            time_text = font.render(f"{max(time_left,0)}s", True, (0, 0, 0))
            screen.blit(time_text, (x + CELL_SIZE // 2 - 10, y + CELL_SIZE // 2 - CELL_SIZE // 2 - 12))

    if not intersections or not any(group.lights for group in traffic_light_groups):
        font = pygame.font.Font(None, 24)
        x = CELL_SIZE * GRID_WIDTH + 10
        y = 60
        screen.blit(font.render("No intersections or traffic lights!", True, (200,0,0)), (x, y))

    for group in traffic_light_groups:
        group.update(dt)
        for light in group.lights:
            light.update(dt, cars)
            light.draw(screen)

    if pygame.time.get_ticks() - last_spawn > SPAWN_INTERVAL:
        vehicle = spawn_vehicle()
        if vehicle:
            cars.append(vehicle)
            last_spawn = pygame.time.get_ticks()

    cars_to_remove = []
    all_traffic_lights = [light for group in traffic_light_groups for light in group.lights]
    for car in cars:
        car.move(all_traffic_lights, cars)
        car.draw(screen)
        if car.index >= len(car.path) - 1:
            cars_to_remove.append(car)
    
    dashboard.update(cars, cars_to_remove)
    
    for car in cars_to_remove:
        cars.remove(car)

    intersection_panel.update(intersections, all_traffic_lights)

    route_congestions = []
    best_route_index = 0
    if suggested_paths:
        for path in suggested_paths:
            if path:
                avg_cong = sum(car_counts.get(cell, 0) for cell in path) / len(path)
                route_congestions.append(avg_cong)
            else:
                route_congestions.append(float('inf'))
        if route_congestions:
            best_route_index = route_congestions.index(min(route_congestions))

    if suggested_paths:
        for idx, current_path in enumerate(suggested_paths):
            color = (0, 255, 0) if idx == best_route_index else (255, 255, 0)
            for (r, c) in current_path:
                rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, color, rect, 4)

    if selected_start:
        rect = pygame.Rect(selected_start[1] * CELL_SIZE, selected_start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (0, 255, 0), rect, 4)
    if selected_end:
        rect = pygame.Rect(selected_end[1] * CELL_SIZE, selected_end[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (0, 0, 255), rect, 4)

    dashboard.draw(screen)
    intersection_panel.draw(screen)
    clear_btn.draw(screen)
    mode_btn.draw(screen)
    if suggested_paths and 0 <= best_route_index < len(suggested_paths):
        route_info_panel.update(suggested_paths[best_route_index], all_traffic_lights, car_counts)
    else:
        route_info_panel.update([], all_traffic_lights, car_counts)
    route_info_panel.draw(screen, CELL_SIZE * GRID_WIDTH + 220, 110)
    mini_map_panel.draw(screen, intersections, suggested_paths[current_path_index] if suggested_paths else [], [], [])

    mode_font = pygame.font.Font(None, 28)
    mode_text = mode_font.render(f"Mode: IDS", True, (0, 0, 0))
    pygame.draw.rect(screen, (255,255,255), (CELL_SIZE * GRID_WIDTH + 220, 160, 140, 36))
    screen.blit(mode_text, (CELL_SIZE * GRID_WIDTH + 230, 170))

    draw_legend(screen)

    traffic_analyzer.update_traffic_density(intersections, cars)

    for group in traffic_light_groups:
        for light in group.lights:
            traffic_level = traffic_analyzer.get_traffic_level((light.row, light.col))
            light.max_green_time = 5000 + (traffic_level * 1000)  # More time for higher traffic

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if clear_btn.is_clicked((mx, my)):
                selected_start = None
                selected_end = None
                suggested_paths = []
                current_path_index = 0
            elif mode_btn.is_clicked((mx, my)):
                if suggested_paths:
                    current_path_index = (current_path_index + 1) % len(suggested_paths)
                    route_info_panel.update(suggested_paths[current_path_index], all_traffic_lights, car_counts)
            elif mx < CELL_SIZE * GRID_WIDTH and my < CELL_SIZE * GRID_HEIGHT:
                col = mx // CELL_SIZE
                row = my // CELL_SIZE
                if (row, col) in intersections and is_valid_position(row, col):
                    if not selected_start:
                        selected_start = (row, col)
                    elif not selected_end and (row, col) != selected_start:
                        selected_end = (row, col)
                        suggested_paths = get_alternative_routes(selected_start, selected_end, is_valid_position)
                        current_path_index = 0
                        if suggested_paths:
                            route_info_panel.update(suggested_paths[current_path_index], all_traffic_lights, car_counts)
                    else:
                        selected_start = (row, col)
                        selected_end = None
                        suggested_paths = []
                        current_path_index = 0

pygame.quit()
sys.exit()
