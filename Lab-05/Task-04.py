"""
Task-04: Results and Path Printing for All Algorithms
======================================================
This task integrates DFS, BFS, and A* algorithms and displays
their results in a clear, organized format.

This file imports the implementations from the previous tasks
and presents the results in a unified manner.
"""

import sys
from collections import deque
import heapq

# Graph definition
graph = {
    'S': [
        ('B_top', 2),
        ('B_bottom', 4)
    ],
    'B_top': [
        ('C', 5),
        ('G', 5)
    ],
    'B_bottom': [
        ('C', 1),
        ('F', 1)
    ],
    'C': [
        ('G', 3),
        ('F', 2)
    ],
    'E': [
        ('B_bottom', 4)
    ],
    'F': [
        ('G', 3)
    ],
    'G': []
}

# Heuristic values for A*
heuristic_values = {
    'S':       6,
    'B_top':   5,
    'B_bottom': 4,
    'C':       3,
    'G':       0,
    'E':       8,
    'F':       3
}


def dfs_find_path(graph, start, goal, verbose=False):
    """DFS implementation - returns path and expanded nodes"""
    visited = set()
    stack = [start]
    parent = {start: None}
    expanded_count = 0
    
    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        expanded_count += 1
        
        if verbose:
            print(f"  Visiting: {current}")
        
        if current == goal:
            path = []
            node = goal
            while node is not None:
                path.append(node)
                node = parent[node]
            path.reverse()
            return path, expanded_count
        
        neighbors = [neighbor[0] for neighbor in graph.get(current, [])]
        for neighbor in neighbors:
            if neighbor not in visited:
                stack.append(neighbor)
                if neighbor not in parent:
                    parent[neighbor] = current
    
    return None, expanded_count


def bfs_find_path(graph, start, goal, verbose=False):
    """BFS implementation - returns path and expanded nodes"""
    visited = set()
    queue = deque([start])
    parent = {start: None}
    visited.add(start)
    expanded_count = 0
    
    while queue:
        current = queue.popleft()
        expanded_count += 1
        
        if verbose:
            print(f"  Visiting: {current}")
        
        if current == goal:
            path = []
            node = goal
            while node is not None:
                path.append(node)
                node = parent[node]
            path.reverse()
            return path, expanded_count
        
        neighbors = [neighbor[0] for neighbor in graph.get(current, [])]
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                parent[neighbor] = current
    
    return None, expanded_count


def heuristic(node):
    """Heuristic function for A*"""
    return heuristic_values.get(node, float('inf'))


def a_star_find_path(graph, start, goal, verbose=False):
    """A* implementation - returns path, cost, and expanded nodes"""
    open_set = []
    heapq.heappush(open_set, (0, 0, start, 0))
    
    visited = set()
    g_values = {start: 0}
    parent = {start: None}
    expanded_count = 0
    counter = 1
    
    while open_set:
        f_value, _, current, g_current = heapq.heappop(open_set)
        
        if current in visited:
            continue
        visited.add(current)
        expanded_count += 1
        
        if verbose:
            h_current = heuristic(current)
            print(f"  Visiting: {current} (g={g_current}, h={h_current}, f={f_value})")
        
        if current == goal:
            path = []
            node = goal
            while node is not None:
                path.append(node)
                node = parent[node]
            path.reverse()
            return path, g_current, expanded_count
        
        neighbors = graph.get(current, [])
        for neighbor_node, edge_weight in neighbors:
            if neighbor_node in visited:
                continue
            
            new_g = g_current + edge_weight
            
            if neighbor_node not in g_values or new_g < g_values[neighbor_node]:
                g_values[neighbor_node] = new_g
                h_neighbor = heuristic(neighbor_node)
                f_neighbor = new_g + h_neighbor
                heapq.heappush(open_set, (f_neighbor, counter, neighbor_node, new_g))
                counter += 1
                parent[neighbor_node] = current
    
    return None, float('inf'), expanded_count


def calculate_path_cost(path, graph):
    """
    Calculate the total cost of a path by summing edge weights.
    
    Args:
        path: List of nodes representing the path
        graph: Adjacency list representation
        
    Returns:
        Total cost of the path
    """
    if not path or len(path) == 1:
        return 0
    
    total_cost = 0
    for i in range(len(path) - 1):
        current = path[i]
        next_node = path[i + 1]
        
        # Find the weight of the edge from current to next_node
        neighbors = graph.get(current, [])
        for neighbor, weight in neighbors:
            if neighbor == next_node:
                total_cost += weight
                break
    
    return total_cost


def print_results(start, goal):
    """
    Run all three algorithms and display comprehensive results.
    
    This function demonstrates each algorithm side-by-side
    and shows detailed metrics for comparison.
    """
    
    print("\n" + "=" * 80)
    print(f"ALGORITHM EXECUTION AND RESULTS")
    print(f"Finding path from '{start}' to '{goal}'")
    print("=" * 80)
    
    # Run DFS
    print("\n" + "-" * 80)
    print("1. DEPTH-FIRST SEARCH (DFS)")
    print("-" * 80)
    print("Status: Ignoring edge weights (treats all edges as cost 1)")
    dfs_path, dfs_expanded = dfs_find_path(graph, start, goal, verbose=False)
    dfs_cost = calculate_path_cost(dfs_path, graph) if dfs_path else None
    
    if dfs_path:
        print(f"✓ Path Found: {' → '.join(dfs_path)}")
        print(f"  Path Length (edges): {len(dfs_path) - 1}")
        print(f"  Actual Path Cost: {dfs_cost}")
        print(f"  Nodes Expanded: {dfs_expanded}")
    else:
        print(f"✗ No path found")
    
    # Run BFS
    print("\n" + "-" * 80)
    print("2. BREADTH-FIRST SEARCH (BFS)")
    print("-" * 80)
    print("Status: Ignoring edge weights (treats all edges as cost 1)")
    bfs_path, bfs_expanded = bfs_find_path(graph, start, goal, verbose=False)
    bfs_cost = calculate_path_cost(bfs_path, graph) if bfs_path else None
    
    if bfs_path:
        print(f"✓ Path Found: {' → '.join(bfs_path)}")
        print(f"  Path Length (edges): {len(bfs_path) - 1}")
        print(f"  Actual Path Cost: {bfs_cost}")
        print(f"  Nodes Expanded: {bfs_expanded}")
    else:
        print(f"✗ No path found")
    
    # Run A*
    print("\n" + "-" * 80)
    print("3. A* ALGORITHM")
    print("-" * 80)
    print("Status: Using edge weights and heuristic function")
    a_star_path, a_star_cost, a_star_expanded = a_star_find_path(graph, start, goal, verbose=False)
    
    if a_star_path:
        print(f"✓ Path Found: {' → '.join(a_star_path)}")
        print(f"  Path Length (edges): {len(a_star_path) - 1}")
        print(f"  Optimal Path Cost: {a_star_cost}")
        print(f"  Nodes Expanded: {a_star_expanded}")
    else:
        print(f"✗ No path found")
    
    # Comparison Summary
    print("\n" + "=" * 80)
    print("COMPARATIVE SUMMARY TABLE")
    print("=" * 80)
    print(f"{'Algorithm':<15} {'Path Found':<12} {'Path Length':<14} {'Cost':<12} {'Nodes Exp.':<12}")
    print("-" * 80)
    
    if dfs_path:
        print(f"{'DFS':<15} {'Yes':<12} {len(dfs_path)-1:<14} {dfs_cost:<12} {dfs_expanded:<12}")
    else:
        print(f"{'DFS':<15} {'No':<12} {'-':<14} {'-':<12} {dfs_expanded:<12}")
    
    if bfs_path:
        print(f"{'BFS':<15} {'Yes':<12} {len(bfs_path)-1:<14} {bfs_cost:<12} {bfs_expanded:<12}")
    else:
        print(f"{'BFS':<15} {'No':<12} {'-':<14} {'-':<12} {bfs_expanded:<12}")
    
    if a_star_path:
        print(f"{'A*':<15} {'Yes':<12} {len(a_star_path)-1:<14} {a_star_cost:<12} {a_star_expanded:<12}")
    else:
        print(f"{'A*':<15} {'No':<12} {'-':<14} {'-':<12} {a_star_expanded:<12}")
    
    print("=" * 80)
    
    # Additional Insights
    print("\nKEY INSIGHTS:")
    print("-" * 80)
    
    if a_star_path and a_star_cost:
        if dfs_path and dfs_cost:
            print(f"DFS vs A*: DFS path cost is {dfs_cost}, A* optimal cost is {a_star_cost}")
            print(f"          A* is {'BETTER' if a_star_cost < dfs_cost else 'WORSE' if a_star_cost > dfs_cost else 'SAME'}")
        
        if bfs_path and bfs_cost:
            print(f"BFS vs A*: BFS path cost is {bfs_cost}, A* optimal cost is {a_star_cost}")
            print(f"          A* is {'BETTER' if a_star_cost < bfs_cost else 'WORSE' if a_star_cost > bfs_cost else 'SAME'}")
    
    print("=" * 80 + "\n")


# Main execution
if __name__ == "__main__":
    start_node = 'S'
    goal_node = 'G'
    
    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + " " * 20 + "GRAPH ALGORITHM ANALYSIS AND RESULTS" + " " * 22 + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    
    print_results(start_node, goal_node)
