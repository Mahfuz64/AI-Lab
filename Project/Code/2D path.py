import pygame
import sys
import random

pygame.init()


CELL_SIZE = 40
GRID_WIDTH = 15
GRID_HEIGHT = 15
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart City: Car Spawn Simulation")

WHITE = (255, 255, 255)
ROAD_COLOR = (80, 80, 80)
BG_COLOR = (230, 230, 230)
CAR_COLORS = [(255, 0, 0), (0, 200, 0), (0, 0, 255), (255, 165, 0), (200, 0, 200)]


road_map = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]


for row in range(GRID_HEIGHT):
    for col in [2, 6, 10, 13]:
        road_map[row][col] = 1


for row in [3, 7, 11]:
    for col in range(GRID_WIDTH):
        road_map[row][col] = 1

# Convert grid to pixel
def grid_to_pixel(row, col):
    return col * CELL_SIZE, row * CELL_SIZE

# Car class
class Car:
    def __init__(self, path, color):
        self.path = path
        self.index = 0
        self.x, self.y = grid_to_pixel(*self.path[0])
        self.speed = 2
        self.color = color

    def move(self):
        if self.index < len(self.path) - 1:
            next_row, next_col = self.path[self.index + 1]
            next_x, next_y = grid_to_pixel(next_row, next_col)

            dx = next_x - self.x
            dy = next_y - self.y

            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist < self.speed:
                self.index += 1
                self.x, self.y = next_x, next_y
            else:
                self.x += self.speed * (dx / dist)
                self.y += self.speed * (dy / dist)

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x + 5, self.y + 5, CELL_SIZE - 10, CELL_SIZE - 10))

# Get all road cells
def get_road_cells():
    return [(r, c) for r in range(GRID_HEIGHT) for c in range(GRID_WIDTH) if road_map[r][c] == 1]

# Check if straight line path is valid
def get_straight_path(start, end):
    r1, c1 = start
    r2, c2 = end

    path = []
    if r1 == r2:
        step = 1 if c2 > c1 else -1
        for c in range(c1, c2 + step, step):
            if road_map[r1][c] != 1:
                return []
            path.append((r1, c))
    elif c1 == c2:
        step = 1 if r2 > r1 else -1
        for r in range(r1, r2 + step, step):
            if road_map[r][c1] != 1:
                return []
            path.append((r, c1))
    return path

# Car list and spawn timer
cars = []
SPAWN_INTERVAL = 2000  # in ms
last_spawn_time = pygame.time.get_ticks()

# Clock
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BG_COLOR)

    # Draw map
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if road_map[row][col] == 1:
                pygame.draw.rect(screen, ROAD_COLOR, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)

    # Spawn new car
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time > SPAWN_INTERVAL:
        road_cells = get_road_cells()
        spawn = random.choice(road_cells)
        dest = random.choice(road_cells)
        while dest == spawn:
            dest = random.choice(road_cells)

        path = get_straight_path(spawn, dest)
        if path:
            color = random.choice(CAR_COLORS)
            cars.append(Car(path, color))
            last_spawn_time = current_time

    # Update and draw cars
    for car in cars:
        car.move()
        car.draw()

    pygame.display.flip()
    clock.tick(60)

    # Quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()
