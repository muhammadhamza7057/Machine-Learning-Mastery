"""
Task-01: Graph Representation using Adjacency List
=====================================================
This task represents the directed, weighted graph from the exercise
using an adjacency list in Python.

Graph Structure:
- Nodes: S, B (top), B (bottom), C, G, E, F
- The graph is directed with weighted edges

Nodes mapping:
S -> Source node (starting point)
B_top -> First B node (top path)
B_bottom -> Second B node (bottom path)
C -> C node
G -> Goal/destination node
E -> E node
F -> F node
"""

# Define the graph as an adjacency list
# Each node maps to a list of (destination, weight) tuples
# This represents all directed edges in the weighted graph

graph = {
    'S': [
        ('B_top', 2),      # S -> B(top) with weight 2
        ('B_bottom', 4)    # S -> B(bottom) with weight 4
    ],
    
    'B_top': [
        ('C', 5),          # B(top) -> C with weight 5
        ('G', 5)           # B(top) -> G with weight 5 (direct path)
    ],
    
    'B_bottom': [
        ('C', 1),          # B(bottom) -> C with weight 1
        ('F', 1)           # B(bottom) -> F with weight 1
    ],
    
    'C': [
        ('G', 3),          # C -> G with weight 3
        ('F', 2)           # C -> F with weight 2
    ],
    
    'E': [
        ('B_bottom', 4)    # E -> B(bottom) with weight 4
    ],
    
    'F': [
        ('G', 3)           # F -> G with weight 3
    ],
    
    'G': []                # Goal node has no outgoing edges
}

# Print the adjacency list representation
def print_graph():
    """
    Function to print the graph in a readable format
    """
    print("=" * 60)
    print("Graph Representation (Adjacency List)")
    print("=" * 60)
    
    for node, edges in graph.items():
        print(f"\nNode: {node}")
        if edges:
            for destination, weight in edges:
                print(f"  └─> {destination} (weight: {weight})")
        else:
            print(f"  └─> No outgoing edges")
    
    print("\n" + "=" * 60)

# Main execution
if __name__ == "__main__":
    print_graph()
    
    # You can also access the graph programmatically
    print("\nQuick Access Examples:")
    print(f"Neighbors of S: {graph['S']}")
    print(f"Neighbors of C: {graph['C']}")
    print(f"Weight of edge S -> B_top: {graph['S'][0][1]}")
