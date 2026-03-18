"""
8-PUZZLE PROBLEM SOLVER USING A* ALGORITHM
============================================

This program implements a goal-based intelligent agent that solves the 8-puzzle
problem using the A* search algorithm. It demonstrates:

1. State space generation - Creating valid successor states
2. Heuristic evaluation - Using Manhattan Distance h(n)
3. Cost evaluation - Using f(n) = g(n) + h(n)
4. Optimal path selection - Selecting best states at each step
5. Solution path display - Showing complete sequence of moves
6. Analysis - Demonstrating optimal decision-making

Author: AI Agent
Subject: Artificial Intelligence Lab
Topic: Goal-Based Intelligent Agents
"""

from typing import List
from puzzle_state import PuzzleState
from astar_solver import AStarSolver
from solution_display import SolutionDisplay


def create_custom_puzzle() -> List[List[int]]:
    """
    Create a custom puzzle configuration
    Returns: 3x3 list representing the puzzle
    """
    print("\n" + "=" * 60)
    print("8-PUZZLE SOLVER - A* Algorithm")
    print("=" * 60)
    
    print("\nGoal Configuration:")
    print("| 1 | 2 | 3 |")
    print("| 4 | 5 | 6 |")
    print("| 7 | 8 | 0 |")
    print("(0 represents empty space)")
    
    print("\nEnter initial puzzle configuration (or use predefined):")
    print("Choose option:")
    print("1. Use easy puzzle")
    print("2. Use medium puzzle")
    print("3. Use hard puzzle")
    print("4. Enter custom puzzle")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    puzzles = {
        "1": [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]  # Already solved
        ],
        "2": [
            [1, 2, 3],
            [4, 5, 6],
            [7, 0, 8]  # One move away
        ],
        "3": [
            [1, 2, 3],
            [4, 5, 6],
            [0, 7, 8]  # Two moves away
        ],
        "4": [
            [1, 2, 3],
            [4, 0, 5],
            [7, 8, 6]  # Multiple moves
        ]
    }
    
    if choice in puzzles:
        initial = puzzles[choice]
        print("\nSelected puzzle:")
        print_state(initial)
        return initial
    else:
        # Default to medium difficulty
        print("\nUsing default medium puzzle...")
        initial = puzzles["2"]
        print_state(initial)
        return initial


def print_state(state: List[List[int]]):
    """Print a puzzle state in readable format"""
    for row in state:
        print("| " + " | ".join(str(x) if x != 0 else " " for x in row) + " |")


def main():
    """Main program execution"""
    
    try:
        # Get initial puzzle configuration
        initial_state = create_custom_puzzle()
        
        # Create and run A* solver
        print("\n" + "=" * 60)
        print("Running A* Algorithm...")
        print("=" * 60)
        print("\nSearching for optimal solution...")
        
        solver = AStarSolver(initial_state)
        success, path, nodes_explored = solver.solve()
        
        # Display results
        if success:
            print(f"\n✓ Solution found!")
            print(f"  Exploring states using priority queue based on f(n) = g(n) + h(n)")
            
            solution_info = solver.get_solution_info()
            
            # Display the full solution path
            display = SolutionDisplay()
            
            # Show all states with costs
            print("\n" + "=" * 60)
            print("DETAILED SOLUTION PATH WITH COST ANALYSIS")
            print("=" * 60)
            display.print_solution_path(path, show_all_states=True)
            
            # Show move sequence
            display.print_move_sequence(path)
            
            # Show comprehensive analysis
            display.print_solution_analysis(
                path, 
                nodes_explored,
                solver.max_frontier_size
            )
            
            # Show compact report
            display.print_compact_solution(path, nodes_explored)
            
            # Final summary
            print("\n" + "=" * 60)
            print("SOLUTION SUMMARY")
            print("=" * 60)
            print(f"\nTotal Moves Required: {solution_info['total_moves']}")
            print(f"Nodes Explored: {solution_info['nodes_explored']}")
            print(f"Solution Path Length: {solution_info['solution_length']}")
            print(f"Max Frontier Size: {solution_info['max_frontier_size']}")
            print("\nThis solution is OPTIMAL because:")
            print("• A* expands nodes in order of f(n) = g(n) + h(n)")
            print("• Manhattan Distance heuristic is admissible")
            print("• First goal found guarantees minimum cost")
            print("=" * 60 + "\n")
            
        else:
            print("\n✗ No solution found!")
            print(f"Nodes explored: {nodes_explored}")
            print("The puzzle configuration may be unsolvable.")
    
    except Exception as e:
        print(f"\nError occurred: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
