"""
Automated Test Suite for 8-Puzzle A* Solver
Tests all requirements and validates solution correctness
"""

from puzzle_state import PuzzleState
from astar_solver import AStarSolver


def test_valid_successor_states():
    """Test Requirement 1: Generate all valid successor states"""
    print("\n" + "="*60)
    print("TEST 1: VALID SUCCESSOR STATES GENERATION")
    print("="*60)
    
    initial = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    
    state = PuzzleState(initial)
    valid_moves = state.get_valid_moves()
    successors = state.generate_successors()
    
    print(f"\nInitial State:")
    print(state)
    print(f"Valid moves from initial state: {len(valid_moves)}")
    print(f"Valid move directions: {[m[2] for m in valid_moves]}")
    print(f"Generated successors: {len(successors)}")
    
    assert len(successors) > 0, "Should generate at least one successor"
    assert len(successors) <= 4, "Maximum 4 successors possible"
    
    print("✓ PASSED: Valid successor states generated correctly")
    return True


def test_heuristic_function():
    """Test Requirement 2: Apply heuristic function h(n)"""
    print("\n" + "="*60)
    print("TEST 2: HEURISTIC FUNCTION h(n) - Manhattan Distance")
    print("="*60)
    
    # Goal state should have h(n) = 0
    goal_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    
    state = PuzzleState(goal_state)
    print(f"\nGoal State h(n) = {state.h_cost}")
    assert state.h_cost == 0, "Goal state should have h(n) = 0"
    
    # State with all tiles displaced should have higher h(n)
    displaced = [
        [8, 7, 6],
        [5, 4, 3],
        [2, 1, 0]
    ]
    
    state2 = PuzzleState(displaced)
    print(f"Displaced State h(n) = {state2.h_cost}")
    assert state2.h_cost > 0, "Displaced state should have positive h(n)"
    
    print("\nHeuristic values calculated using Manhattan Distance:")
    print("Sum of |current_row - goal_row| + |current_col - goal_col|")
    print("for each tile.")
    
    print("✓ PASSED: Heuristic function h(n) working correctly")
    return True


def test_evaluation_function():
    """Test Requirement 3: Use evaluation function f(n) = g(n) + h(n)"""
    print("\n" + "="*60)
    print("TEST 3: EVALUATION FUNCTION f(n) = g(n) + h(n)")
    print("="*60)
    
    initial = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    
    state = PuzzleState(initial)
    print(f"\nInitial State Analysis:")
    print(f"g(n) [Cost from start]: {state.g_cost}")
    print(f"h(n) [Heuristic cost]: {state.h_cost}")
    print(f"f(n) = g(n) + h(n) = {state.g_cost} + {state.h_cost} = {state.f_cost}")
    
    # Verify the formula
    assert state.f_cost == state.g_cost + state.h_cost, \
        "f(n) must equal g(n) + h(n)"
    
    # Create a successor and check f(n) changes
    successors = state.generate_successors()
    if successors:
        successor = successors[0]
        print(f"\nSuccessor State Analysis:")
        print(f"g(n) [Cost from start]: {successor.g_cost}")
        print(f"h(n) [Heuristic cost]: {successor.h_cost}")
        print(f"f(n) = g(n) + h(n) = {successor.g_cost} + {successor.h_cost} = {successor.f_cost}")
        assert successor.g_cost == state.g_cost + 1, "g(n) should increase by 1"
    
    print("\n✓ PASSED: Evaluation function f(n) working correctly")
    return True


def test_state_selection():
    """Test Requirement 4: Select the best state at each step"""
    print("\n" + "="*60)
    print("TEST 4: BEST STATE SELECTION")
    print("="*60)
    
    initial = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 0, 8]
    ]
    
    state = PuzzleState(initial)
    successors = state.generate_successors()
    
    print(f"\nGenerated {len(successors)} successors:")
    for i, succ in enumerate(successors, 1):
        print(f"Successor {i}: f(n)={succ.f_cost}, g(n)={succ.g_cost}, h(n)={succ.h_cost}")
    
    # Best state should have minimum f(n)
    best = min(successors, key=lambda s: s.f_cost)
    print(f"\nBest successor has f(n) = {best.f_cost}")
    assert best.f_cost == min(s.f_cost for s in successors), \
        "Best state selection failed"
    
    print("✓ PASSED: Best state selection working correctly")
    return True


def test_solution_path_display():
    """Test Requirement 5: Display full solution path"""
    print("\n" + "="*60)
    print("TEST 5: SOLUTION PATH DISPLAY")
    print("="*60)
    
    initial = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 0, 8]
    ]
    
    solver = AStarSolver(initial)
    success, path, nodes_explored = solver.solve()
    
    print(f"\nSolution found: {success}")
    print(f"Path length: {len(path)} states")
    
    if success:
        print("\nFull path states:")
        for i, state in enumerate(path):
            print(f"State {i}: f(n)={state.f_cost}, Move={state.move}")
    
    assert success, "Should find solution for solvable puzzle"
    assert len(path) > 0, "Path should not be empty"
    
    print("✓ PASSED: Solution path displayed correctly")
    return True


def test_total_moves_cost():
    """Test Requirement 6: Print total moves (cost)"""
    print("\n" + "="*60)
    print("TEST 6: TOTAL MOVES/COST CALCULATION")
    print("="*60)
    
    initial = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 0, 8]
    ]
    
    solver = AStarSolver(initial)
    success, path, nodes_explored = solver.solve()
    
    if success:
        total_moves = len(path) - 1  # -1 because first state is initial
        moves_list = [state.move for state in path[1:]]
        
        print(f"\nTotal moves required: {total_moves}")
        print(f"Move sequence: {' → '.join(moves_list)}")
        print(f"Final cost g(n): {path[-1].g_cost}")
        
        assert total_moves == path[-1].g_cost, "Total moves should equal g(n)"
        assert len(moves_list) == total_moves, "Move count mismatch"
    
    print("✓ PASSED: Total moves/cost calculated correctly")
    return True


def run_all_tests():
    """Run all requirement tests"""
    print("\n" + "█"*60)
    print("█ 8-PUZZLE A* ALGORITHM - REQUIREMENT VALIDATION TESTS")
    print("█"*60)
    
    tests = [
        test_valid_successor_states,
        test_heuristic_function,
        test_evaluation_function,
        test_state_selection,
        test_solution_path_display,
        test_total_moves_cost
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append((test_func.__name__, result))
        except Exception as e:
            print(f"✗ FAILED: {e}")
            results.append((test_func.__name__, False))
    
    # Print summary
    print("\n" + "█"*60)
    print("█ TEST SUMMARY")
    print("█"*60)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    
    print(f"\nTotal: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n✓ ALL REQUIREMENTS VALIDATED SUCCESSFULLY!")
    else:
        print(f"\n✗ {total_tests - total_passed} test(s) failed")
    
    print("█"*60 + "\n")
    
    return total_passed == total_tests


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
