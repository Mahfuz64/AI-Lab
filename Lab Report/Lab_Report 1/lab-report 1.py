import random

class Node:
    def __init__(self, a, b, z):
        self.x = a
        self.y = b
        self.depth = z

class DFS:
    def __init__(self):
        self.directions = 4
        self.x_move = [1, -1, 0, 0]  
        self.y_move = [0, 0, 1, -1]
        self.found = False
        self.N = 0
        self.source = None
        self.goal = None
        self.goal_level = 999999
        self.path = [] 
        self.topological_order = [] 

    def generate_random_grid(self):
        self.N = random.randint(4, 7)
        graph = [[random.choice([0, 1]) for _ in range(self.N)] for _ in range(self.N)]

    
        while True:
            source_x, source_y = random.randint(0, self.N - 1), random.randint(0, self.N - 1)
            goal_x, goal_y = random.randint(0, self.N - 1), random.randint(0, self.N - 1)
            if (source_x, source_y) != (goal_x, goal_y) and graph[source_x][source_y] == 1 and graph[goal_x][goal_y] == 1:
                break

        self.source = Node(source_x, source_y, 0)
        self.goal = Node(goal_x, goal_y, self.goal_level)
        return graph, (source_x, source_y), (goal_x, goal_y)

    def print_grid(self, graph, source, goal):
        print("\nGrid:")
        for i in range(self.N):
            row = ""
            for j in range(self.N):
                if (i, j) == source:
                    row += "S " 
                elif (i, j) == goal:
                    row += "G " 
                else:
                    row += ("1 " if graph[i][j] == 1 else "0 ")
            print(row)

    def print_direction(self, m, x, y):
        directions = ["Down", "Up", "Right", "Left"]
        print(f"Moving {directions[m]} -> ({x}, {y})")

    def st_dfs(self, graph, u):
        self.topological_order.append((u.x, u.y))
        self.path.append((u.x, u.y))
        
        if u.x == self.goal.x and u.y == self.goal.y:
            self.found = True
            self.goal.depth = u.depth
            return

        graph[u.x][u.y] = 0 

        for j in range(self.directions):
            v_x = u.x + self.x_move[j]
            v_y = u.y + self.y_move[j]

            if 0 <= v_x < self.N and 0 <= v_y < self.N and graph[v_x][v_y] == 1:
                self.print_direction(j, v_x, v_y)
                child = Node(v_x, v_y, u.depth + 1)
                self.st_dfs(graph, child)

                if self.found:
                    return

        self.path.pop() 

    def init(self):
        graph, source, goal = self.generate_random_grid()
        self.print_grid(graph, source, goal)

        print(f"\nSource: {source}\nGoal: {goal}\n")
        self.st_dfs(graph, self.source)

        if self.found:
            print("\nGoal found!")
            print(f"Number of moves required = {self.goal.depth}")
            print(f"DFS Path: {self.path}")
        else:
            print("\nGoal cannot be reached from the starting block.")

        print(f"\nTopological Order of Traversal: {self.topological_order}")

def main():
    d = DFS()
    d.init()

if __name__ == "__main__":
    main()
