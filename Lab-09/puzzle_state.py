"""
8-Puzzle State Representation Class
Handles the state of the puzzle and basic operations
"""

from typing import Tuple, List
from copy import deepcopy


class PuzzleState:
    """Represents a state of the 8-puzzle and operations on it"""
    
    GOAL_STATE = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    
    def __init__(self, initial_state: List[List[int]], parent=None, move: str = "Start"):
        """
        Initialize a puzzle state
        
        Args:
            initial_state: 3x3 list representing puzzle configuration
            parent: Parent state (for path reconstruction)
            move: The move that led to this state
        """
        self.state = deepcopy(initial_state)
        self.parent = parent
        self.move = move
        self.g_cost = 0 if parent is None else parent.g_cost + 1  # Cost from start
        self.h_cost = self._calculate_heuristic()  # Heuristic cost to goal
        self.f_cost = self.g_cost + self.h_cost  # Total evaluation cost
        
    def _calculate_heuristic(self) -> int:
        """
        Calculate Manhattan Distance heuristic
        Sum of distances of each tile from its goal position
        
        Returns:
            int: Manhattan distance heuristic value
        """
        heuristic = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != 0:  # 0 is the empty tile
                    goal_pos = self._find_goal_position(self.state[i][j])
                    heuristic += abs(i - goal_pos[0]) + abs(j - goal_pos[1])
        return heuristic
    
    @staticmethod
    def _find_goal_position(value: int) -> Tuple[int, int]:
        """Find the goal position of a given value"""
        for i in range(3):
            for j in range(3):
                if PuzzleState.GOAL_STATE[i][j] == value:
                    return (i, j)
        return (-1, -1)
    
    def _find_empty_tile(self) -> Tuple[int, int]:
        """Find position of empty tile (0) in current state"""
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return (i, j)
        return (-1, -1)
    
    def is_goal(self) -> bool:
        """Check if current state is the goal state"""
        return self.state == self.GOAL_STATE
    
    def get_valid_moves(self) -> List[Tuple[int, int, str]]:
        """
        Get all valid moves from current state
        
        Returns:
            List of (new_i, new_j, direction_name) tuples
        """
        empty_i, empty_j = self._find_empty_tile()
        valid_moves = []
        
        # Define possible moves: Up, Down, Left, Right
        directions = [
            (-1, 0, "UP"),     # Move up (empty tile moves up)
            (1, 0, "DOWN"),    # Move down
            (0, -1, "LEFT"),   # Move left
            (0, 1, "RIGHT")    # Move right
        ]
        
        for di, dj, direction in directions:
            new_i, new_j = empty_i + di, empty_j + dj
            
            # Check if new position is within bounds
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                valid_moves.append((new_i, new_j, direction))
        
        return valid_moves
    
    def generate_successors(self) -> List['PuzzleState']:
        """
        Generate all successor states from current state
        
        Returns:
            List of successor PuzzleState objects
        """
        successors = []
        empty_i, empty_j = self._find_empty_tile()
        
        for new_i, new_j, direction in self.get_valid_moves():
            # Create new state by swapping empty tile with adjacent tile
            new_state = deepcopy(self.state)
            new_state[empty_i][empty_j], new_state[new_i][new_j] = \
                new_state[new_i][new_j], new_state[empty_i][empty_j]
            
            # Create successor state
            successor = PuzzleState(new_state, parent=self, move=direction)
            successors.append(successor)
        
        return successors
    
    def __hash__(self) -> int:
        """Make state hashable for set operations"""
        return hash(tuple(tuple(row) for row in self.state))
    
    def __eq__(self, other) -> bool:
        """Check equality of two states"""
        if not isinstance(other, PuzzleState):
            return False
        return self.state == other.state
    
    def __lt__(self, other) -> bool:
        """
        Less than comparison for priority queue
        (For Python's heapq, smaller f_cost has higher priority)
        """
        if self.f_cost != other.f_cost:
            return self.f_cost < other.f_cost
        return self.h_cost < other.h_cost
    
    def __repr__(self) -> str:
        """String representation of state"""
        result = "\n"
        for row in self.state:
            result += str(row) + "\n"
        return result
    
    def get_path(self) -> List['PuzzleState']:
        """
        Reconstruct path from initial state to current state
        
        Returns:
            List of states from start to current
        """
        path = []
        current = self
        while current is not None:
            path.append(current)
            current = current.parent
        return path[::-1]  # Reverse to get start -> goal order
