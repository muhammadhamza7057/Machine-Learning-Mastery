"""
Task-02: DFS and BFS Implementation
====================================
This task implements Depth-First Search (DFS) and Breadth-First Search (BFS)
to find any valid path from source node S to goal node G.

Note: For DFS and BFS, we IGNORE the weights on edges.
      We only care about finding if a path exists, not the optimal path.

Data Structures Used:
- DFS uses a Stack (implemented using a list with append/pop)
- BFS uses a Queue (implemented using collections.deque or list)
"""

from collections import deque

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


def dfs_find_path(graph, start, goal):
    """
    Depth-First Search (DFS) to find a path from start to goal
    
    Algorithm:
    1. Use a stack to keep track of nodes to visit
    2. Use a visited set to avoid revisiting nodes
    3. Keep track of parent nodes to reconstruct the path
    4. Pop a node from stack, explore its neighbors, push unvisited neighbors
    
    Time Complexity: O(V + E) where V = vertices, E = edges
    Space Complexity: O(V) for the stack and visited set
    
    Args:
        graph: Adjacency list representation of the graph
        start: Starting node
        goal: Goal node
        
    Returns:
        A tuple (path, expanded_nodes) where:
        - path: List of nodes from start to goal, or None if no path exists
        - expanded_nodes: Number of nodes expanded during search
    """
    
    visited = set()           # Track visited nodes to avoid cycles
    stack = [start]           # Initialize stack with start node
    parent = {start: None}    # Track parent of each node to reconstruct path
    expanded_count = 0        # Count of nodes expanded
    
    print("\n" + "=" * 60)
    print("DFS (Depth-First Search)")
    print("=" * 60)
    
    while stack:
        # Pop a node from the stack (last in, first out)
        current = stack.pop()
        
        # Check if we've already visited this node
        if current in visited:
            continue
        
        # Mark as visited
        visited.add(current)
        expanded_count += 1
        
        print(f"Visiting: {current}")
        
        # Check if we reached the goal
        if current == goal:
            print(f"✓ Goal '{goal}' found!")
            # Reconstruct path by following parent pointers
            path = []
            node = goal
            while node is not None:
                path.append(node)
                node = parent[node]
            path.reverse()
            return path, expanded_count
        
        # Explore neighbors (add unvisited neighbors to stack)
        # Note: We only extract node name, ignore weight
        neighbors = [neighbor[0] for neighbor in graph.get(current, [])]
        
        for neighbor in neighbors:
            if neighbor not in visited:
                stack.append(neighbor)
                if neighbor not in parent:  # Set parent if not yet set
                    parent[neighbor] = current
    
    print(f"✗ No path found from {start} to {goal}")
    return None, expanded_count


def bfs_find_path(graph, start, goal):
    """
    Breadth-First Search (BFS) to find a path from start to goal
    
    Algorithm:
    1. Use a queue to keep track of nodes to visit
    2. Use a visited set to avoid revisiting nodes
    3. Keep track of parent nodes to reconstruct the path
    4. Dequeue a node, explore its neighbors, enqueue unvisited neighbors
    
    Guarantees: BFS finds the SHORTEST path (in terms of number of edges)
    
    Time Complexity: O(V + E) where V = vertices, E = edges
    Space Complexity: O(V) for the queue and visited set
    
    Args:
        graph: Adjacency list representation of the graph
        start: Starting node
        goal: Goal node
        
    Returns:
        A tuple (path, expanded_nodes) where:
        - path: List of nodes from start to goal, or None if no path exists
        - expanded_nodes: Number of nodes expanded during search
    """
    
    visited = set()           # Track visited nodes
    queue = deque([start])    # Initialize queue with start node
    parent = {start: None}    # Track parent of each node
    visited.add(start)        # Mark start as visited immediately
    expanded_count = 0        # Count of nodes expanded
    
    print("\n" + "=" * 60)
    print("BFS (Breadth-First Search)")
    print("=" * 60)
    
    while queue:
        # Dequeue a node from the front (first in, first out)
        current = queue.popleft()
        expanded_count += 1
        
        print(f"Visiting: {current}")
        
        # Check if we reached the goal
        if current == goal:
            print(f"✓ Goal '{goal}' found!")
            # Reconstruct path by following parent pointers
            path = []
            node = goal
            while node is not None:
                path.append(node)
                node = parent[node]
            path.reverse()
            return path, expanded_count
        
        # Explore neighbors (add unvisited neighbors to queue)
        # Note: We only extract node name, ignore weight
        neighbors = [neighbor[0] for neighbor in graph.get(current, [])]
        
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                parent[neighbor] = current
    
    print(f"✗ No path found from {start} to {goal}")
    return None, expanded_count


# Main execution
if __name__ == "__main__":
    start_node = 'S'
    goal_node = 'G'
    
    print("\nFinding path from", start_node, "to", goal_node)
    print("(Ignoring edge weights - treating all edges as having weight 1)")
    
    # Run DFS
    dfs_path, dfs_expanded = dfs_find_path(graph, start_node, goal_node)
    print(f"Path found: {' -> '.join(dfs_path) if dfs_path else 'None'}")
    print(f"Nodes expanded: {dfs_expanded}")
    
    # Run BFS
    bfs_path, bfs_expanded = bfs_find_path(graph, start_node, goal_node)
    print(f"Path found: {' -> '.join(bfs_path) if bfs_path else 'None'}")
    print(f"Nodes expanded: {bfs_expanded}")
    
    print("\n" + "=" * 60)
    print("Summary:")
    print(f"DFS path length: {len(dfs_path) if dfs_path else 'N/A'}, Nodes expanded: {dfs_expanded}")
    print(f"BFS path length: {len(bfs_path) if bfs_path else 'N/A'}, Nodes expanded: {bfs_expanded}")
    print("=" * 60)
