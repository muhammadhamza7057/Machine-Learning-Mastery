import abc
from typing import List
from collections import deque
import numpy as np


class Graph(abc.ABC):
    """
    Base (abstract) Graph class.
    """

    def __init__(self, num_vertices: int, directed: bool = False) -> None:
        """
        Parameters:
            num_vertices (int): number of vertices in the graph
            directed (bool): True for directed graph, False for undirected
        """
        self.num_vertices = num_vertices
        self.directed = directed

    @abc.abstractmethod
    def add_edge(self, v1: int, v2: int, weight: int = 1) -> None:
        """Connects two vertices and assigns weight to the edge."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_adjacent_vertices(self, v: int) -> List[int]:
        """Returns list of neighboring vertices."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_indegree(self, v: int) -> int:
        """Returns indegree of vertex v."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_edge_weight(self, v1: int, v2: int) -> float:
        """Returns weight of edge between v1 and v2."""
        raise NotImplementedError

    @abc.abstractmethod
    def display(self) -> None:
        """Prints the whole graph."""
        raise NotImplementedError


class AdjacencyMatrixGraph(Graph):
    """
    Graph implementation using an adjacency matrix.
    """

    def __init__(self, num_vertices: int, directed: bool = False) -> None:
        super().__init__(num_vertices, directed)
        self.matrix = np.zeros((num_vertices, num_vertices))

    def add_edge(self, v1: int, v2: int, weight: int = 1) -> None:
        """Connects two vertices."""
        if v1 >= self.num_vertices or v2 >= self.num_vertices or v1 < 0 or v2 < 0:
            raise ValueError(f"Vertices {v1} and {v2} are out of bounds")
        if weight < 1:
            raise ValueError("An edge cannot have weight < 1")

        self.matrix[v1][v2] = weight
        if not self.directed:
            self.matrix[v2][v1] = weight

    def get_adjacent_vertices(self, v: int) -> List[int]:
        if v < 0 or v >= self.num_vertices:
            raise ValueError(f"Cannot access vertex {v}")

        adjacent_vertices: List[int] = []
        for i in range(self.num_vertices):
            if self.matrix[v][i] > 0:
                adjacent_vertices.append(i)
        return adjacent_vertices

    def get_indegree(self, v: int) -> int:
        """Returns indegree of vertex v."""
        if v < 0 or v >= self.num_vertices:
            raise ValueError(f"Cannot access vertex {v}")

        indegree = 0
        for i in range(self.num_vertices):
            if self.matrix[i][v] > 0:
                indegree += 1
        return indegree

    def get_edge_weight(self, v1: int, v2: int) -> float:
        """Returns weight of edge between two vertices."""
        return self.matrix[v1][v2]

    def display(self) -> None:
        """Prints the whole graph."""
        for i in range(self.num_vertices):
            for v in self.get_adjacent_vertices(i):
                print(i, "-->", v)


# ===========================
# BFS & DFS Implementations
# ===========================

def bfs(graph: Graph, start_vertex: int):
    """BFS traversal of the graph starting from start_vertex."""
    visited = []
    queue = deque([start_vertex])

    visited.append(start_vertex)

    while queue:
        node = queue.popleft()
        print(node, end=" ")

        for neighbor in graph.get_adjacent_vertices(node):
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)

    return visited


def dfs(graph: Graph, start_vertex: int, visited=None):
    """DFS traversal of the graph starting from start_vertex."""
    if visited is None:
        visited = []

    visited.append(start_vertex)
    print(start_vertex, end=" ")

    for neighbor in graph.get_adjacent_vertices(start_vertex):
        if neighbor not in visited:
            dfs(graph, neighbor, visited)

    return visited


# ===========================
# Example Usage
# ===========================
if __name__ == "__main__":
    g = AdjacencyMatrixGraph(6, directed=False)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 4)
    g.add_edge(3, 5)
    g.add_edge(4, 5)

    print("Graph edges:")
    g.display()

    print("\nBFS starting from vertex 0:")
    bfs(g, 0)

    print("\n\nDFS starting from vertex 0:")
    dfs(g, 0)
    print()