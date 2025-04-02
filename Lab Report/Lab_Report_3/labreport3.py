def is_safe(graph, vertex, color_assignment, c):
    for neighbor in graph[vertex]:
        if color_assignment[neighbor] == c:
            return False
    return True

def graph_coloring_backtracking(graph, num_vertices, num_colors, vertex=0, color_assignment=None):
    if color_assignment is None:
        color_assignment = [-1] * num_vertices
    
    if vertex == num_vertices:
        return True, color_assignment
    
    for c in range(1, num_colors + 1):
        if is_safe(graph, vertex, color_assignment, c):
            color_assignment[vertex] = c
            if graph_coloring_backtracking(graph, num_vertices, num_colors, vertex + 1, color_assignment)[0]:
                return True, color_assignment
            color_assignment[vertex] = -1
    
    return False, color_assignment

def read_input_file(filename):
    with open(filename, "r") as file:
        n, m, k = map(int, file.readline().split())
        graph = {i: [] for i in range(n)}
        
        for _ in range(m):
            u, v = map(int, file.readline().split())
            graph[u].append(v)
            graph[v].append(u)
    
    return graph, n, k

def main():
    filename = "input.txt" 
    graph, num_vertices, num_colors = read_input_file(filename)
    success, color_assignment = graph_coloring_backtracking(graph, num_vertices, num_colors)
    
    if success:
        print(f"Coloring Possible with {num_colors} Colors")
        print(f"Color Assignment: {color_assignment}")
    else:
        print(f"Coloring Not Possible with {num_colors} Colors")

if __name__ == "__main__":
    main()
