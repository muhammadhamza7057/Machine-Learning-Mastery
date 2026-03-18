"""
8-Puzzle A* Solver - Demonstration Example
Shows a complete example solution with detailed output
"""

from puzzle_state import PuzzleState
from astar_solver import AStarSolver
from solution_display import SolutionDisplay


def demo_example_1():
    """Demo 1: Easy puzzle (1 move away from goal)"""
    print("\n" + "="*70)
    print("EXAMPLE 1: EASY PUZZLE (1 Move to Goal)")
    print("="*70)
    
    initial = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 0, 8]
    ]
    
    print("\nInitial Configuration:")
    print("| 1 | 2 | 3 |")
    print("| 4 | 5 | 6 |")
    print("| 7 | 0 | 8 |")
    print("\nGoal Configuration:")
    print("| 1 | 2 | 3 |")
    print("| 4 | 5 | 6 |")
    print("| 7 | 8 | 0 |")
    
    solver = AStarSolver(initial)
    success, path, nodes_explored = solver.solve()
    
    if success:
        display = SolutionDisplay()
        display.print_solution_path(path, show_all_states=True)
        display.print_move_sequence(path)
        display.print_compact_solution(path, nodes_explored)
        
        print(f"\nAnalysis:")
        print(f"- Solution found in {len(path)-1} moves")
        print(f"- Nodes explored: {nodes_explored}")
        print(f"- This puzzle required minimal search due to small depth")


def demo_example_2():
    """Demo 2: Medium puzzle (3-4 moves away from goal)"""
    print("\n" + "="*70)
    print("EXAMPLE 2: MEDIUM PUZZLE (3-4 Moves to Goal)")
    print("="*70)
    
    initial = [
        [1, 2, 3],
        [4, 0, 5],
        [7, 8, 6]
    ]
    
    print("\nInitial Configuration:")
    print("| 1 | 2 | 3 |")
    print("| 4 | 0 | 5 |")
    print("| 7 | 8 | 6 |")
    print("\nGoal Configuration:")
    print("| 1 | 2 | 3 |")
    print("| 4 | 5 | 6 |")
    print("| 7 | 8 | 0 |")
    
    solver = AStarSolver(initial)
    success, path, nodes_explored = solver.solve()
    
    if success:
        display = SolutionDisplay()
        display.print_move_sequence(path)
        display.print_compact_solution(path, nodes_explored)
        
        print(f"\nAnalysis:")
        print(f"- Solution found in {len(path)-1} moves")
        print(f"- Nodes explored: {nodes_explored}")
        print(f"- Cost progression through states:")
        for i, state in enumerate(path[::max(1, len(path)//5)]):
            print(f"  Step {i}: g(n)={state.g_cost}, h(n)={state.h_cost}, f(n)={state.f_cost}")


def demo_example_3():
    """Demo 3: Harder puzzle with more moves"""
    print("\n" + "="*70)
    print("EXAMPLE 3: CHALLENGING PUZZLE (5-6 Moves to Goal)")
    print("="*70)
    
    initial = [
        [4, 1, 2],
        [7, 5, 3],
        [8, 0, 6]
    ]
    
    print("\nInitial Configuration:")
    print("| 4 | 1 | 2 |")
    print("| 7 | 5 | 3 |")
    print("| 8 | 0 | 6 |")
    print("\nGoal Configuration:")
    print("| 1 | 2 | 3 |")
    print("| 4 | 5 | 6 |")
    print("| 7 | 8 | 0 |")
    
    solver = AStarSolver(initial)
    success, path, nodes_explored = solver.solve()
    
    if success:
        display = SolutionDisplay()
        display.print_move_sequence(path)
        display.print_compact_solution(path, nodes_explored)
        display.print_solution_analysis(path, nodes_explored, solver.max_frontier_size)
        
        print(f"\nKey Observations:")
        print(f"- Solution found in {len(path)-1} moves")
        print(f"- Nodes explored: {nodes_explored}")
        print(f"- Maximum frontier size: {solver.max_frontier_size}")
        print(f"- A* avoided exploring suboptimal paths through heuristic guidance")


def print_algorithm_comparison():
    """Print comparison showing why A* is better"""
    print("\n" + "="*70)
    print("ALGORITHM COMPARISON: Why A* is Optimal")
    print("="*70)
    
    print("""
SEARCH ALGORITHM COMPARISON:
────────────────────────────────────────────────────────────────

1. BREADTH-FIRST SEARCH (BFS)
   - Expands states level by level
   - Guarantees shortest path (in unweighted graphs)
   - Inefficient: explores all states at depth d before d+1
   - Nodes explored: Often 1000+ for medium puzzles

2. DEPTH-FIRST SEARCH (DFS)
   - Explores deeply before backtracking
   - Can find solutions quickly if lucky
   - No guarantee of optimality
   - Can waste time on dead-end branches

3. UNIFORM COST SEARCH (UCS)
   - Uses only g(n): actual cost from start
   - Explores states in order of path cost
   - Better than BFS/DFS but still uninformed
   - Nodes explored: Usually 100-500 for medium puzzles

4. A* SEARCH (Our Implementation)
   ✓ Uses f(n) = g(n) + h(n)
   ✓ Informed by heuristic h(n)
   ✓ Optimal with admissible heuristic
   ✓ Guaranteed to find best solution
   ✓ Nodes explored: Usually 10-50 for medium puzzles
   ✓ Most efficient and intelligent approach

MANHATTAN DISTANCE HEURISTIC PROPERTIES:
────────────────────────────────────────────────────────────────
✓ Admissible: Never overestimates actual cost
✓ Consistent: h(n) ≤ cost(n, n') + h(n') for all successors
✓ Effective: Good estimates reduce search space
✓ Simple: O(1) to compute, O(n) for all states
✓ Accurate: Closely approximates actual remaining cost

OPTIMAL DECISION-MAKING IN A*:
────────────────────────────────────────────────────────────────
At each step, A* makes the BEST decision because:

1. It selects the state with minimum f(n) = g(n) + h(n)
2. This balances:
   - Actual progress toward goal (g(n))
   - Remaining estimated effort (h(n))
3. The heuristic guides search toward goal intelligently
4. Unattractive branches (high h(n)) are explored last
5. First goal found is guaranteed optimal
6. No better path could have been missed

PROOF OF OPTIMALITY:
────────────────────────────────────────────────────────────────
If h(n) is admissible (never overestimates):
1. When A* reaches goal, f(goal) = g(goal) + 0 is actual cost
2. Any unexplored state has f(n) ≥ actual goal cost
3. Therefore, goal found is optimal
4. This is guaranteed by the priority queue ordering

EXAMPLE WITH NUMBERS:
────────────────────────────────────────────────────────────────
For a medium puzzle:
- A* might explore: ~30 nodes before finding solution
- BFS would explore: ~300+ nodes at same depth
- DFS might explore: ~500+ nodes before finding goal
- UCS would explore: ~100+ nodes

A* finds the solution 10x faster than uninformed search!
""")


def main():
    """Run all demonstrations"""
    print("\n" + "█"*70)
    print("█ 8-PUZZLE A* SOLVER - DEMONSTRATION EXAMPLES")
    print("█"*70)
    
    # Run examples
    demo_example_1()
    demo_example_2()
    demo_example_3()
    
    # Show algorithm comparison
    print_algorithm_comparison()
    
    print("\n" + "█"*70)
    print("█ DEMONSTRATION COMPLETE")
    print("█"*70)
    print("\nKey Takeaways:")
    print("1. A* finds optimal solutions efficiently")
    print("2. Manhattan Distance guides search effectively")
    print("3. f(n) = g(n) + h(n) ensures smart node selection")
    print("4. Heuristic reduces search space dramatically")
    print("5. First goal found guarantees optimality")
    print("\n")


if __name__ == "__main__":
    main()
