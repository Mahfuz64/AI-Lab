class IDDFS:
    def __init__(self, maze, start, target):
        self.maze = maze
        self.start = start
        self.target = target
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    def depth_limited_search(self, node, depth, visited, path):
        if node == self.target:
            path.append(node)
            return True
        
        if depth == 0:
            return False
        
        x, y = node
        visited.add(node)
        path.append(node)
        
        for dx, dy in self.directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols and self.maze[nx][ny] == 0 and (nx, ny) not in visited:
                if self.depth_limited_search((nx, ny), depth - 1, visited, path):
                    return True
        
        path.pop()
        return False
    
    def iddfs(self, max_depth=50):
        for depth in range(max_depth):
            visited = set()
            path = []
            if self.depth_limited_search(self.start, depth, visited, path):
                print(f"Path found at depth {depth} using IDDFS")
                print("Traversal Order:", path)
                return
        print(f"Path not found at max depth {max_depth} using IDDFS")

def main():
    rows, cols = map(int, input().split())
    maze = [list(map(int, input().split())) for _ in range(rows)]
    sx, sy = map(int, input().split()[1:])
    tx, ty = map(int, input().split()[1:])
    
    solver = IDDFS(maze, (sx, sy), (tx, ty))
    solver.iddfs()

if __name__ == "__main__":
    main()
