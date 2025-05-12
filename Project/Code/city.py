CELL_SIZE = 24
GRID_WIDTH = 32
GRID_HEIGHT = 16

def generate_road_map():
    road_map = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    verticals = [i for i in range(1, GRID_WIDTH-1, 3)]
    horizontals = [i for i in range(1, GRID_HEIGHT-1, 3)]
    for col in verticals:
        for row in range(GRID_HEIGHT):
            road_map[row][col] = 1
    for row in horizontals:
        for col in range(GRID_WIDTH):
            road_map[row][col] = 1
    return road_map

def get_road_cells(road_map):
    return [(r, c) for r in range(len(road_map)) for c in range(len(road_map[0])) if road_map[r][c] == 1]

def get_intersections(road_map):
    intersections = []
    for r in range(1, len(road_map)-1):
        for c in range(1, len(road_map[0])-1):
            if road_map[r][c] == 1:  # Only consider road cells
                # Count road neighbors (4-directional)
                neighbors = 0
                for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                    if 0 <= r+dr < len(road_map) and 0 <= c+dc < len(road_map[0]):
                        neighbors += road_map[r+dr][c+dc]
                
                # Consider it an intersection if ≥ 3 connecting roads
                if neighbors >= 3:
                    intersections.append((r, c))
    return intersections

def grid_to_pixel(row, col):
    return col * CELL_SIZE, row * CELL_SIZE
