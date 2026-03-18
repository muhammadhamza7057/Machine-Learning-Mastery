"""
A* Algorithm Implementation for the 8-Puzzle Problem
Implements the A* search algorithm with f(n) = g(n) + h(n)
"""

import heapq
from typing import Tuple, List, Set
from puzzle_state import PuzzleState


class AStarSolver:
    """A* algorithm solver for the 8-puzzle problem"""
    
    def __init__(self, initial_state: List[List[int]]):
        """
        Initialize the A* solver
        
        Args:
            initial_state: The initial configuration of the puzzle (3x3 list)
        """
        self.initial_state = initial_state
        self.open_set = []  # Priority queue for frontier nodes
        self.closed_set: Set[PuzzleState] = set()  # Visited nodes
        self.goal_state = None
        self.nodes_explored = 0
        self.max_frontier_size = 0
        
    def solve(self) -> Tuple[bool, List[PuzzleState], int]:
        """
        Solve the 8-puzzle using A* algorithm
        
        Algorithm:
        1. Add initial state to open set
        2. While open set is not empty:
           a. Get state with minimum f(n) from open set
           b. If goal state, return solution
           c. Generate successors
           d. For each successor not in closed set:
              - Add to open set with f(n) cost
              e. Add current to closed set
        3. If open set empty and no goal found, no solution
        
        Returns:
            Tuple of (success, path_to_goal, nodes_explored)
        """
        # Initialize
        initial = PuzzleState(self.initial_state)
        heapq.heappush(self.open_set, (initial.f_cost, initial))
        
        while self.open_set:
            # Track maximum frontier size
            self.max_frontier_size = max(self.max_frontier_size, len(self.open_set))
            
            # Get state with minimum f(n) from priority queue
            _, current_state = heapq.heappop(self.open_set)
            
            # Check if goal state reached
            if current_state.is_goal():
                self.goal_state = current_state
                return True, current_state.get_path(), self.nodes_explored
            
            # Add to closed set (visited)
            self.closed_set.add(current_state)
            self.nodes_explored += 1
            
            # Generate and evaluate successor states
            for successor in current_state.generate_successors():
                # Skip if already visited
                if successor in self.closed_set:
                    continue
                
                # Check if successor already in open set with higher cost
                # and update if necessary
                in_open = False
                for i, (f_cost, state) in enumerate(self.open_set):
                    if state == successor:
                        in_open = True
                        # If we found a better path, update it
                        if successor.f_cost < f_cost:
                            self.open_set[i] = (successor.f_cost, successor)
                            heapq.heapify(self.open_set)
                        break
                
                # Add to open set if not already there
                if not in_open:
                    heapq.heappush(self.open_set, (successor.f_cost, successor))
        
        # No solution found
        return False, [], self.nodes_explored
    
    def get_solution_info(self) -> dict:
        """
        Get detailed information about the solution
        
        Returns:
            Dictionary with solution metrics
        """
        if self.goal_state is None:
            return {
                "is_solved": False,
                "total_moves": 0,
                "nodes_explored": self.nodes_explored,
                "max_frontier_size": self.max_frontier_size
            }
        
        path = self.goal_state.get_path()
        return {
            "is_solved": True,
            "total_moves": len(path) - 1,  # -1 because start state has 0 moves
            "final_g_cost": self.goal_state.g_cost,
            "nodes_explored": self.nodes_explored,
            "max_frontier_size": self.max_frontier_size,
            "solution_length": len(path)
        }
