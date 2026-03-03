"""
Task-03: A* Algorithm Implementation
====================================
This task implements the A* (A-Star) algorithm to find the minimum-cost path
from source node S to goal node G using edge weights and a heuristic function.

A* Formula: f(n) = g(n) + h(n)
where:
    - g(n) = actual cost from start to node n
    - h(n) = heuristic estimate of cost from node n to goal
    - f(n) = estimated total cost through node n

Heuristics:
A heuristic must be admissible (never overestimate actual distance).
This example uses predefined heuristic values based on node layout.

Data Structure Used:
- Priority Queue (implemented using heapq module)
"""

import heapq

# Graph definition (same as Task-01)
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

# Define heuristic values for each node
# These represent estimated distances to goal node 'G'
# Based on the graph layout, here are reasonable heuristic values
heuristic_values = {
    'S':       6,    # S is far from G, estimated cost to reach G is 6
    'B_top':   5,    # B_top needs at least 5 to reach C, then 3 to G
    'B_bottom': 4,   # B_bottom can go through C(1) to reach closer to G
    'C':       3,    # C can reach G directly with cost 3
    'G':       0,    # G is the goal, heuristic is 0
    'E':       8,    # E is far from goal
    'F':       3     # F is close to G, can reach with cost 3
}


def heuristic(node, goal='G'):
    """
    Heuristic function that estimates the cost from a node to the goal.
    
    This uses predefined heuristic values that are admissible
    (they never overestimate the actual cost).
    
    Args:
        node: Current node
        goal: Goal node (default 'G')
        
    Returns:
        Estimated cost from node to goal
    """
    return heuristic_values.get(node, float('inf'))


def a_star_find_path(graph, start, goal):
    """
    A* algorithm to find the minimum-cost path from start to goal.
    
    Algorithm:
    1. Use a priority queue ordered by f(n) = g(n) + h(n)
    2. g(n) = actual cost from start to current node
    3. h(n) = heuristic estimate of cost from current to goal
    4. Always expand the most promising node (lowest f value)
    5. Track parent nodes to reconstruct the path
    
    Optimality: A* finds the OPTIMAL path if heuristic is admissible
    (heuristic never overestimates actual distance)
    
    Time Complexity: Depends on heuristic quality, but O(b^d) in worst case
    Space Complexity: O(V) for storage
    
    Args:
        graph: Adjacency list representation of the graph
        start: Starting node
        goal: Goal node
        
    Returns:
        A tuple (path, total_cost, expanded_nodes) where:
        - path: List of nodes from start to goal, or None if no path exists
        - total_cost: Total cost of the path
        - expanded_nodes: Number of nodes expanded during search
    """
    
    # Priority queue stores tuples: (f_value, counter, node, g_value)
    # counter ensures FIFO for nodes with same f_value
    open_set = []
    heapq.heappush(open_set, (0, 0, start, 0))  # (f, counter, node, g)
    
    visited = set()           # Track nodes we've fully explored
    g_values = {start: 0}     # Actual cost from start to each node
    parent = {start: None}    # Track parent node for path reconstruction
    expanded_count = 0        # Count of nodes expanded
    counter = 1               # For maintaining order in priority queue
    
    print("\n" + "=" * 70)
    print("A* (A-Star) Algorithm")
    print("=" * 70)
    print(f"Start: {start}, Goal: {goal}")
    print(f"\nHeuristicValues (h values):")
    for node in heuristic_values:
        print(f"  h({node}) = {heuristic_values[node]}")
    
    while open_set:
        # Get node with minimum f value from priority queue
        f_value, _, current, g_current = heapq.heappop(open_set)
        
        # Skip if we've already fully explored this node
        if current in visited:
            continue
        
        # Mark as visited (fully explored)
        visited.add(current)
        expanded_count += 1
        
        # Calculate actual values for display
        h_current = heuristic(current)
        
        print(f"\nExpanding: {current}")
        print(f"  g({current}) = {g_current} (actual cost from start)")
        print(f"  h({current}) = {h_current} (heuristic estimate)")
        print(f"  f({current}) = {g_current} + {h_current} = {f_value}")
        
        # Check if we reached the goal
        if current == goal:
            print(f"\n✓ Goal '{goal}' found!")
            
            # Reconstruct path
            path = []
            node = goal
            while node is not None:
                path.append(node)
                node = parent[node]
            path.reverse()
            
            return path, g_current, expanded_count
        
        # Explore neighbors
        neighbors = graph.get(current, [])
        
        for neighbor_node, edge_weight in neighbors:
            if neighbor_node in visited:
                continue  # Skip already fully explored nodes
            
            # Calculate cost to reach this neighbor
            new_g = g_current + edge_weight
            
            # Only process if this is a better path than previously found
            if neighbor_node not in g_values or new_g < g_values[neighbor_node]:
                g_values[neighbor_node] = new_g
                h_neighbor = heuristic(neighbor_node)
                f_neighbor = new_g + h_neighbor
                
                # Add to priority queue
                heapq.heappush(open_set, (f_neighbor, counter, neighbor_node, new_g))
                counter += 1
                
                # Update parent
                parent[neighbor_node] = current
                
                print(f"  → Added to queue: {neighbor_node} with f-value {f_neighbor}")
    
    print(f"\n✗ No path found from {start} to {goal}")
    return None, float('inf'), expanded_count


# Main execution
if __name__ == "__main__":
    start_node = 'S'
    goal_node = 'G'
    
    print("\nFinding MINIMUM-COST path from", start_node, "to", goal_node)
    print("(Using edge weights and heuristic function)")
    
    # Run A*
    a_star_path, a_star_cost, a_star_expanded = a_star_find_path(graph, start_node, goal_node)
    
    print("\n" + "=" * 70)
    if a_star_path:
        print(f"Path found: {' -> '.join(a_star_path)}")
        print(f"Total path cost: {a_star_cost}")
    else:
        print(f"No path found from {start_node} to {goal_node}")
    
    print(f"Nodes expanded: {a_star_expanded}")
    print("=" * 70)
