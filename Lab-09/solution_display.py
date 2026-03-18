"""
Display and Visualization Module for 8-Puzzle Solution
Shows the step-by-step solution path and analysis
"""

from typing import List
from puzzle_state import PuzzleState


class SolutionDisplay:
    """Display and format the solution path"""
    
    @staticmethod
    def print_puzzle_state(state: PuzzleState, step: int = 0, show_costs: bool = True):
        """
        Print a single puzzle state in a readable format
        
        Args:
            state: PuzzleState to display
            step: Step number in solution path
            show_costs: Whether to show g(n), h(n), f(n) costs
        """
        print(f"\n{'='*40}")
        if step > 0:
            print(f"Step: {step} | Move: {state.move}")
        else:
            print(f"INITIAL STATE")
        print(f"{'='*40}")
        
        # Print the puzzle state
        for row in state.state:
            print("| ", end="")
            for cell in row:
                if cell == 0:
                    print(" ", end=" | ")
                else:
                    print(cell, end=" | ")
            print()
        
        # Print costs
        if show_costs:
            print(f"-" * 40)
            print(f"g(n) [Cost from start]: {state.g_cost}")
            print(f"h(n) [Heuristic cost]: {state.h_cost}")
            print(f"f(n) = g(n) + h(n):   {state.g_cost} + {state.h_cost} = {state.f_cost}")
            print(f"-" * 40)
    
    @staticmethod
    def print_solution_path(path: List[PuzzleState], show_all_states: bool = True):
        """
        Print the complete solution path
        
        Args:
            path: List of states from start to goal
            show_all_states: Whether to show all intermediate states
        """
        print("\n" + "=" * 60)
        print("8-PUZZLE SOLUTION PATH")
        print("=" * 60)
        
        if show_all_states:
            for step, state in enumerate(path):
                SolutionDisplay.print_puzzle_state(state, step)
        else:
            # Only show initial and goal states
            print("\nINITIAL STATE:")
            SolutionDisplay.print_puzzle_state(path[0], 0, show_costs=False)
            
            print("\n" + "-" * 40)
            print("GOAL STATE REACHED!")
            print("-" * 40)
            SolutionDisplay.print_puzzle_state(path[-1], len(path)-1, show_costs=False)
    
    @staticmethod
    def print_move_sequence(path: List[PuzzleState]):
        """Print just the sequence of moves"""
        print("\n" + "=" * 60)
        print("MOVE SEQUENCE")
        print("=" * 60)
        
        moves = [state.move for state in path[1:]]  # Skip initial state
        
        print("\nSequence of moves:")
        for i, move in enumerate(moves, 1):
            print(f"{i:2}. {move}")
        
        print(f"\nTotal moves: {len(moves)}")
    
    @staticmethod
    def print_solution_analysis(path: List[PuzzleState], 
                               nodes_explored: int,
                               max_frontier_size: int):
        """
        Print detailed analysis of the solution
        
        Args:
            path: Solution path
            nodes_explored: Total nodes explored by A*
            max_frontier_size: Maximum frontier size during search
        """
        print("\n" + "=" * 60)
        print("SOLUTION ANALYSIS & ALGORITHM METRICS")
        print("=" * 60)
        
        print(f"\n1. SOLUTION METRICS:")
        print(f"   Total moves (cost): {len(path) - 1}")
        print(f"   Solution length: {len(path)} states")
        print(f"   Final g(n): {path[-1].g_cost}")
        print(f"   Final h(n): {path[-1].h_cost}")
        print(f"   Final f(n): {path[-1].f_cost}")
        
        print(f"\n2. ALGORITHM EFFICIENCY:")
        print(f"   Nodes explored: {nodes_explored}")
        print(f"   Maximum frontier size: {max_frontier_size}")
        print(f"   Branching factor: {4}")  # 8-puzzle has at most 4 moves
        
        print(f"\n3. HEURISTIC ANALYSIS:")
        initial_h = path[0].h_cost
        final_h = path[-1].h_cost
        print(f"   Initial h(n): {initial_h}")
        print(f"   Final h(n): {final_h}")
        print(f"   h(n) reduction: {initial_h - final_h}")
        print(f"   Average h(n) per step: {initial_h / (len(path) - 1) if len(path) > 1 else 0:.2f}")
        
        print(f"\n4. OPTIMALITY EXPLANATION:")
        print(f"   The A* algorithm guarantees optimal solution because:")
        print(f"   - It explores nodes in order of f(n) = g(n) + h(n)")
        print(f"   - Manhattan Distance is admissible (never overestimates)")
        print(f"   - The first goal state found is guaranteed to be optimal")
        print(f"   - Total cost: {len(path) - 1} moves")
        
        print(f"\n5. DECISION-MAKING PROCESS:")
        print(f"   At each step, A* selected the state with minimum f(n),")
        print(f"   balancing actual cost g(n) with estimated remaining cost h(n).")
        print(f"   This ensures the best path is explored first, leading to")
        print(f"   optimal decision-making and minimum cost solution.")
        
        print("\n" + "=" * 60)
    
    @staticmethod
    def print_compact_solution(path: List[PuzzleState], nodes_explored: int):
        """Print a compact version of the solution"""
        print("\n" + "█" * 60)
        print("█ 8-PUZZLE A* SOLUTION REPORT")
        print("█" * 60)
        
        moves = [state.move for state in path[1:]]
        
        print(f"\n✓ SOLUTION FOUND!")
        print(f"  Total Moves: {len(moves)}")
        print(f"  Nodes Explored: {nodes_explored}")
        
        print(f"\n→ Move Sequence:")
        print(f"  {' → '.join(moves)}")
        
        print(f"\n• States Progression:")
        print(f"  Initial state → (optimized path) → Goal state")
        print(f"  Total states in path: {len(path)}")
        
        print("\n" + "█" * 60)
