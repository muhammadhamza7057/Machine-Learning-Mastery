"""
Task-05: Detailed Comparison of DFS vs BFS vs A*
=================================================
This task provides a comprehensive comparison of three graph traversal algorithms:
DFS (Depth-First Search), BFS (Breadth-First Search), and A* (A-Star).

The comparison analyzes:
1. Data structures used
2. Completeness (can it always find a solution?)
3. Optimality (does it find the best solution?)
4. Time Complexity
5. Space Complexity
6. Real-world applications

This is a detailed analysis document with examples from the given graph.
"""

print("\n" + "█" * 90)
print("█" + " " * 88 + "█")
print("█" + " " * 15 + "COMPREHENSIVE COMPARISON: DFS vs BFS vs A*" + " " * 31 + "█")
print("█" + " " * 88 + "█")
print("█" * 90)


# ============================================================================
# 1. DATA STRUCTURES USED
# ============================================================================

print("\n" + "=" * 90)
print("1. DATA STRUCTURES USED")
print("=" * 90)

print("""
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ DFS (Depth-First Search)                                                            │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ Primary Data Structure: STACK (Last-In-First-Out / LIFO)                           │
│                                                                                     │
│ Implementation: Can be implemented using:                                          │
│   • List with append() and pop() operations in Python                             │
│   • Recursion (call stack is implicit)                                            │
│                                                                                     │
│ How it works:                                                                       │
│   1. Push the start node onto the stack                                            │
│   2. While stack is not empty:                                                     │
│      - Pop the node from top of stack                                              │
│      - If not visited, mark as visited                                             │
│      - Push all unvisited neighbors onto the stack                                 │
│   3. The stack naturally explores deep paths first                                 │
│                                                                                     │
│ Example with our graph (S to G):                                                   │
│   Stack: [S]                                                                        │
│   → Pop S, push neighbors: [B_bottom, B_top]                                       │
│   → Pop B_top, push neighbors: [G, C]                                              │
│   → Pop C, found or push neighbors...                                              │
│   → Pop G, GOAL REACHED!                                                            │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│ BFS (Breadth-First Search)                                                          │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ Primary Data Structure: QUEUE (First-In-First-Out / FIFO)                          │
│                                                                                     │
│ Implementation: Can be implemented using:                                          │
│   • collections.deque for O(1) append and popleft operations                       │
│   • List with append() and pop(0), but less efficient                              │
│                                                                                     │
│ How it works:                                                                       │
│   1. Enqueue the start node                                                        │
│   2. While queue is not empty:                                                     │
│      - Dequeue a node from front                                                   │
│      - If not visited, mark as visited                                             │
│      - Enqueue all unvisited neighbors                                             │
│   3. The queue naturally explores level by level (breadth-wise)                    │
│                                                                                     │
│ Example with our graph (S to G):                                                   │
│   Queue: [S]                                                                        │
│   → Dequeue S, enqueue neighbors: [B_bottom, B_top]                                │
│   → Dequeue B_bottom, enqueue neighbors: [C, F]                                    │
│   → Dequeue B_top, enqueue neighbors: [C, G]                                       │
│   → Dequeue C, C already visited, skip new ones...                                 │
│   → Dequeue F, enqueue neighbors: [G]                                              │
│   → Dequeue G, GOAL REACHED!                                                        │
│   Note: Explores all nodes at distance 1 before distance 2, etc.                   │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│ A* (A-Star Algorithm)                                                               │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ Primary Data Structure: PRIORITY QUEUE                                             │
│                                                                                     │
│ Implementation: Can be implemented using:                                          │
│   • heapq module (min-heap) in Python                                              │
│   • Maintains heap order for efficient extraction of minimum element               │
│                                                                                     │
│ How it works:                                                                       │
│   1. Initialize with start node: f(start) = g(start) + h(start)                    │
│   2. While priority queue is not empty:                                            │
│      - Extract node with minimum f value                                           │
│      - If this is goal, FOUND!                                                     │
│      - For each neighbor, calculate: f = g + edge_cost + h(neighbor)               │
│      - Add to priority queue if f is better                                        │
│   3. Always expands the most promising node first                                  │
│                                                                                     │
│ Components:                                                                         │
│   • g(n): Actual cost from start to node n                                         │
│   • h(n): Heuristic estimate from node n to goal                                   │
│   • f(n): Total estimated cost = g(n) + h(n)                                       │
│                                                                                     │
│ Example with our graph (S to G):                                                   │
│   f(S) = 0 + 6 = 6                                                                  │
│   → Expand S (lowest f), add: B_top(f=7), B_bottom(f=8)                            │
│   → Expand B_top (f=7), add: C(f=8), G(f=10)                                       │
│   → Expand C (f=8), check G(f=8)...                                                │
│   → Might expand G if it's lowest, GOAL REACHED!                                   │
│   Note: Always chose the node with lowest f value                                  │
└─────────────────────────────────────────────────────────────────────────────────────┘
""")


# ============================================================================
# 2. COMPLETENESS
# ============================================================================

print("\n" + "=" * 90)
print("2. COMPLETENESS (Can it always find a solution if one exists?)")
print("=" * 90)

print("""
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ DFS (Depth-First Search)                                                            │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ Completeness: YES - BUT ONLY if graph has finite depth                             │
│                                                                                     │
│ Conditions:                                                                         │
│   ✓ COMPLETE if: The graph is acyclic OR we track visited nodes                   │
│   ✗ INCOMPLETE if: Infinite depth in acyclic graph (unlikely in practice)          │
│                                                                                     │
│ Why: DFS explores deeply first, so if a path exists but is very deep,             │
│      DFS might explore unproductive branches first before finding it               │
│                                                                                     │
│ Example with our graph:                                                            │
│   We have visited set, so DFS will eventually find path S → B_top → G              │
│   guaranteed (if one exists)                                                       │
│                                                                                     │
│ Guarantee: IF path exists AND we use visited set, DFS finds it                     │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│ BFS (Breadth-First Search)                                                          │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ Completeness: YES - Always complete                                                │
│                                                                                     │
│ Why: BFS explores level by level (by distance from start)                          │
│      If a path exists, BFS will find it at some depth level                        │
│      It cannot miss a path because it systematically explores all nodes            │
│      at distance d before exploring nodes at distance d+1                          │
│                                                                                     │
│ Guarantee: BFS ALWAYS finds a solution if one exists                               │
│            Moreover, it finds the SHORTEST path (in terms of edge count)           │
│                                                                                     │
│ Example with our graph:                                                            │
│   Level 0: [S]                                                                      │
│   Level 1: [B_top, B_bottom]                                                       │
│   Level 2: [C, G, F]    ← G found at level 2!                                      │
│   Guaranteed to find path with minimum number of edges                             │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│ A* (A-Star Algorithm)                                                               │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ Completeness: YES - If admissible heuristic is used                                │
│                                                                                     │
│ Conditions:                                                                         │
│   ✓ COMPLETE if: h(n) ≤ actual_cost(n to goal) for ALL nodes                     │
│                   (Admissible heuristic)                                           │
│   ✗ INCOMPLETE if: h(n) overestimates some distances                              │
│                                                                                     │
│ Why: With admissible heuristic, A* never prunes the path to goal                   │
│      The actual cost will eventually be lower than h-estimates for goal path      │
│                                                                                     │
│ Example with our graph:                                                            │
│   h values: S=6, B_top=5, B_bottom=4, C=3, F=3, G=0 (all admissible!)             │
│   These NEVER overestimate, so A* will find path: S → ... → G guaranteed           │
│                                                                                     │
│ Guarantee: A* finds solution if admissible heuristic used (which it is here)      │
└─────────────────────────────────────────────────────────────────────────────────────┘
""")


# ============================================================================
# 3. OPTIMALITY
# ============================================================================

print("\n" + "=" * 90)
print("3. OPTIMALITY (Does it find the minimum-cost solution?)")
print("=" * 90)

print("""
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ DFS (Depth-First Search)                                                            │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ Optimality: NO - DFS does not guarantee minimum-cost path                          │
│                                                                                     │
│ Why: DFS explores in arbitrary order (depth-first) and returns first path found    │
│      This path may not be the cheapest one                                         │
│                                                                                     │
│ Example with our graph:                                                            │
│   DFS might find: S → B_top → C → G (cost: 2+5+3 = 10)                            │
│   But optimal:     S → B_bottom → C → G (cost: 4+1+3 = 8)                          │
│   DFS returns first path found, not the cheapest!                                  │
│                                                                                     │
│ When to use despite non-optimality:                                                │
│   • Only care about finding ANY path                                               │
│   • Need to explore all possibilities anyway                                       │
│   • Memory-constrained (DFS uses less memory)                                      │
│                                                                                     │
│ Guarantee: NO guarantee of optimal solution                                        │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│ BFS (Breadth-First Search)                                                          │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ Optimality: YES - IF all edge costs are equal (uniform cost)                       │
│             NO - If edge costs differ                                              │
│                                                                                     │
│ Why: BFS finds path with minimum NUMBER OF EDGES, but not minimum COST            │
│      if edges have different weights                                               │
│                                                                                     │
│ Example with our graph:                                                            │
│   BFS finds:  S → B_bottom → C → G (3 edges, cost=8)  ← Minimum edges!            │
│   But also:   S → B_top → G (2 edges, cost=7)  ← Fewer edges but higher cost!     │
│                                                                                     │
│   If we ignore weights (all edges = cost 1):                                       │
│   BFS is OPTIMAL because it minimizes edge count                                   │
│                                                                                     │
│   If we consider weights:                                                          │
│   BFS is NOT optimal (S→B_top→G = 7 is cheaper than S→B_bottom→C→G = 8)          │
│                                                                                     │
│ When to use:                                                                        │
│   • Unweighted graphs (or all edges have same weight)                              │
│   • Need shortest path by edge count, not cost                                     │
│   • Simpler than A* and faster for unweighted graphs                               │
│                                                                                     │
│ Guarantee: OPTIMAL for unweighted graphs only                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│ A* (A-Star Algorithm)                                                               │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ Optimality: YES - IF admissible heuristic is used                                  │
│                                                                                     │
│ Mathematical Proof:                                                                 │
│   If h(n) ≤ actual_cost(n to goal), then A* always finds optimal path              │
│   A* expands nodes with lowest f(n) = g(n) + h(n)                                  │
│   When goal is selected for expansion, g(goal) is guaranteed to be optimal        │
│                                                                                     │
│ Why: A* combines:                                                                   │
│   g(n) = actual cost reaching n (exact, from start)                                │
│   h(n) = heuristic estimate remaining (admissible, won't overestimate)             │
│   This guarantees optimality!                                                      │
│                                                                                     │
│ Example with our graph:                                                            │
│   Our heuristics are admissible (never overestimate):                              │
│     h(S)=6, h(B_top)=5, h(B_bottom)=4, h(C)=3, h(F)=3, h(G)=0                     │
│                                                                                     │
│   A* finds: S → B_bottom → C → G (cost = 4+1+3 = 8) - OPTIMAL!                    │
│   (Better than S → B_top → G which costs 2+5 = 7... wait that's cheaper!)         │
│   So A* would actually find: S → B_top → G (cost = 7) - TRUE OPTIMAL!             │
│                                                                                     │
│ Guarantee: ALWAYS finds optimal solution with admissible heuristic                 │
└─────────────────────────────────────────────────────────────────────────────────────┘
""")


# ============================================================================
# 4. TIME COMPLEXITY
# ============================================================================

print("\n" + "=" * 90)
print("4. TIME COMPLEXITY")
print("=" * 90)

print("""
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ DFS (Depth-First Search)                                                            │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ Time Complexity: O(V + E)                                                          │
│   where V = number of vertices, E = number of edges                                │
│                                                                                     │
│ Explanation:                                                                        │
│   • Each vertex is visited at most once (due to visited set)                       │
│   • Each edge is examined at most once                                             │
│   • Visiting one vertex: O(1)                                                      │
│   • Examining all edges: O(E)                                                      │
│   • Total: O(V) + O(E) = O(V + E)                                                  │
│                                                                                     │
│ With our graph (6 nodes, 8 edges):                                                 │
│   Time = O(6 + 8) = O(14) = VERY FAST                                             │
│                                                                                     │
│ Best Case:   O(1) if goal is first neighbor explored                               │
│ Worst Case:  O(V + E) if goal is last or not found                                │
│ Average:     Depends on goal location and exploration order                        │
│                                                                                     │
│ Note: DFS is very efficient - once we visit a vertex, we never revisit it          │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│ BFS (Breadth-First Search)                                                          │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ Time Complexity: O(V + E)                                                          │
│   where V = number of vertices, E = number of edges                                │
│                                                                                     │
│ Explanation:                                                                        │
│   • Same as DFS - each vertex visited once, each edge examined once                │
│   • Queue operations (enqueue/dequeue) are O(1) with deque                         │
│   • Total: O(V) vertices + O(E) edges = O(V + E)                                   │
│                                                                                     │
│ With our graph:                                                                     │
│   Time = O(6 + 8) = O(14) = VERY FAST                                             │
│                                                                                     │
│ Best Case:   O(1) if goal is first neighbor                                        │
│             O(V) if goal is at depth of tree width                                │
│ Worst Case:  O(V + E) if goal not found or at end                                 │
│ Average:     Generally linear like DFS                                             │
│                                                                                     │
│ IMPORTANT: Unlike DFS, BFS guarantees shortest path in unweighted graphs           │
│            But it might visit more nodes to ensure this                            │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│ A* (A-Star Algorithm)                                                               │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ Time Complexity: O(b^d) in worst case                                              │
│   where b = branching factor, d = depth to goal                                    │
│                                                                                     │
│   BUT with good heuristic: Much better than worst case!                            │
│                                                                                     │
│ Explanation:                                                                        │
│   • Without heuristic (h=0, becomes Dijkstra): O(E log V) with binary heap         │
│   • With perfect heuristic: O(V) - goes straight to goal                          │
│   • With good heuristic: O(E' + V' log V') where E', V' << E, V                   │
│                                                                                     │
│ With our graph and our heuristics:                                                 │
│   Good heuristics mean we don't explore unnecessary nodes                          │
│   Time: Much better than O(b^d), closer to O(V + E)                               │
│   Actual: Visits fewer nodes than BFS but with heap overhead                      │
│                                                                                     │
│ Best Case:   O(h(n) evaluations) if heuristic is perfect                           │
│ Worst Case:  O(b^d) = exponential (bad heuristic)                                  │
│ Average:     Depends heavily on heuristic quality!                                 │
│                                                                                     │
│ Heap Operations:                                                                    │
│   • Each insert/extract: O(log V)                                                  │
│   • Total V operations: O(V log V)                                                 │
│   • Plus edge operations and heuristic evaluations                                 │
│                                                                                     │
│ KEY INSIGHT: A* is slower than DFS/BFS per operation (due to heap),                │
│              but expands FEWER nodes when given good heuristic                     │
│              This often makes A* faster in practice                                │
└─────────────────────────────────────────────────────────────────────────────────────┘
""")


# ============================================================================
# 5. SPACE COMPLEXITY
# ============================================================================

print("\n" + "=" * 90)
print("5. SPACE COMPLEXITY")
print("=" * 90)

print("""
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ DFS (Depth-First Search)                                                            │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ Space Complexity: O(h) or O(V)                                                     │
│   h = height of tree/graph                                                         │
│   V = number of vertices                                                           │
│                                                                                     │
│ Breakdown:                                                                          │
│   Stack storage: O(h) in best case (linear path), O(V) in worst case              │
│   Visited set: O(V)                                                                │
│   Parent tracking: O(V)                                                            │
│   Total: O(V) worst case                                                           │
│                                                                                     │
│ With our graph:                                                                     │
│   Stack could have at most V nodes                                                 │
│   Visited set: 6 nodes                                                             │
│   Parent map: 6 nodes                                                              │
│   Total: O(6) = MINIMAL MEMORY                                                     │
│                                                                                     │
│ Advantage of DFS:                                                                   │
│   ✓ Uses LESS MEMORY than BFS in many cases                                       │
│   ✓ Stack only needs space for current path depth                                  │
│   ✓ Good for memory-constrained systems                                            │
│                                                                                     │
│ Stack grows along deepest path, not breadth                                        │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│ BFS (Breadth-First Search)                                                          │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ Space Complexity: O(w) or O(V)                                                     │
│   w = maximum width (branching) of tree                                            │
│   V = number of vertices                                                           │
│                                                                                     │
│ Breakdown:                                                                          │
│   Queue storage: O(w) at deepest level (could be O(V))                             │
│   Visited set: O(V)                                                                │
│   Parent tracking: O(V)                                                            │
│   Total: O(V) in general case                                                      │
│                                                                                     │
│ With our graph:                                                                     │
│   Queue at deepest level: max neighbors at one level                               │
│   Visited set: 6 nodes                                                             │
│   Parent map: 6 nodes                                                              │
│   Total: O(6) = MODERATE MEMORY                                                    │
│                                                                                     │
│ Problem with BFS:                                                                   │
│   ✗ Uses MORE MEMORY than DFS                                                     │
│   ✗ Queue expands with breadth of graph                                            │
│   ✗ In wide graphs, can use significant memory                                     │
│                                                                                     │
│ Queue holds all neighbors at current level (width-based growth)                    │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│ A* (A-Star Algorithm)                                                               │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ Space Complexity: O(V)                                                             │
│   Generally same as BFS but can be optimized                                       │
│                                                                                     │
│ Breakdown:                                                                          │
│   Open set (priority queue): O(V) worst case                                       │
│   Closed set (explored): O(V)                                                      │
│   g-values tracking: O(V)                                                          │
│   Parent tracking: O(V)                                                            │
│   Total: O(V)                                                                      │
│                                                                                     │
│ With our graph:                                                                     │
│   Open set: could hold up to 6 nodes                                               │
│   Closed set: 6 nodes                                                              │
│   g-values: 6 nodes                                                                │
│   Parent: 6 nodes                                                                  │
│   Total: O(6) = MODERATE TO HIGH MEMORY                                            │
│                                                                                     │
│ Trade-off Analysis:                                                                │
│   ✗ Uses MORE memory than DFS                                                     │
│   ≈ Similar to BFS                                                                 │
│   ✓ But finds goal faster, so shorter span overall                                │
│   ✓ With good heuristic, many nodes never even added to open set                  │
│                                                                                     │
│ Priority queue (heap) has overhead but doesn't significantly increase space        │
└─────────────────────────────────────────────────────────────────────────────────────┘
""")


# ============================================================================
# 6. COMPARISON TABLE
# ============================================================================

print("\n" + "=" * 90)
print("6. COMPREHENSIVE COMPARISON TABLE")
print("=" * 90)

print("""
┌──────────────────┬────────────────────┬────────────────────┬────────────────────┐
│ CRITERION        │ DFS                │ BFS                │ A*                 │
├──────────────────┼────────────────────┼────────────────────┼────────────────────┤
│ Data Structure   │ Stack (LIFO)       │ Queue (FIFO)       │ Priority Queue     │
│                  │                    │                    │ (min-heap)         │
├──────────────────┼────────────────────┼────────────────────┼────────────────────┤
│ Completeness     │ YES*               │ YES                │ YES**              │
│                  │ (*if finite depth) │ (always)           │ (**with admissible │
│                  │                    │                    │   heuristic)       │
├──────────────────┼────────────────────┼────────────────────┼────────────────────┤
│ Optimality       │ NO                 │ Sort of***         │ YES****            │
│ (Minimum Cost)   │ (returns first     │ (***only if edges  │ (****with          │
│                  │  path found)       │  have equal cost)  │  admissible h)     │
├──────────────────┼────────────────────┼────────────────────┼────────────────────┤
│ Time Complexity  │ O(V + E)           │ O(V + E)           │ O(E log V) avg     │
│                  │ Linear             │ Linear             │ O(b^d) worst case  │
├──────────────────┼────────────────────┼────────────────────┼────────────────────┤
│ Space Complexity │ O(h) or O(V)       │ O(w) or O(V)       │ O(V)               │
│ (h=height,       │ Usually smallest   │ Usually largest    │ Medium to Large    │
│  w=width)        │                    │                    │                    │
├──────────────────┼────────────────────┼────────────────────┼────────────────────┤
│ Explores nodes   │ In depth order     │ In breadth order   │ By f-cost order    │
│ by:              │ (newest first)     │ (oldest first)     │ (most promising)   │
├──────────────────┼────────────────────┼────────────────────┼────────────────────┤
│ Implementation   │ Simple,            │ Moderate,          │ Complex,           │
│ Difficulty       │ Easy to understand │ straightforward    │ requires heuristic │
├──────────────────┼────────────────────┼────────────────────┼────────────────────┤
│ Path Quality     │ Often poor         │ Short path         │ Optimal path       │
│ (if weighted)    │ (ignores weights)  │ (needs work)       │ (if heuristic OK)  │
├──────────────────┼────────────────────┼────────────────────┼────────────────────┤
│ Practical Speed  │ Fast but paths     │ Slower than DFS    │ Fastest if good    │
│                  │ often suboptimal   │ but better paths   │ heuristic          │
│                  │                    │                    │                    │
└──────────────────┴────────────────────┴────────────────────┴────────────────────┘
""")


# ============================================================================
# 7. REAL-WORLD APPLICATIONS
# ============================================================================

print("\n" + "=" * 90)
print("7. REAL-WORLD APPLICATIONS")
print("=" * 90)

print("""
┌──────────────────────────────────────────────────────────────────────────────────┐
│ DFS (Depth-First Search)                                                         │
├──────────────────────────────────────────────────────────────────────────────────┤
│ Best Used For:                                                                   │
│                                                                                  │
│ 1. Topological Sorting                                                          │
│    • Ordering tasks with dependencies                                           │
│    • Compiler symbol resolution                                                 │
│    • Build system dependency ordering                                           │
│                                                                                  │
│ 2. Cycle Detection in Graphs                                                    │
│    • Finding circular dependencies                                              │
│    • Deadlock detection in systems                                              │
│                                                                                  │
│ 3. Connected Components                                                         │
│    • Findng isolated groups in networks                                         │
│    • Social network clustering                                                  │
│                                                                                  │
│ 4. Strongly Connected Components (SCC)                                          │
│    • Kosaraju's and Tarjan's algorithms use DFS                                 │
│                                                                                  │
│ 5. Backtracking Problems                                                        │
│    • N-Queens problem                                                           │
│    • Sudoku solver                                                              │
│    • Maze solving (find any exit)                                               │
│                                                                                  │
│ 6. Tree Traversals                                                              │
│    • In-order, pre-order, post-order traversals                                 │
│    • Expression tree evaluation                                                 │
│                                                                                  │
│ Why: DFS naturally handles these problems with its depth-first nature            │
│      Efficient memory usage with recursion                                      │
│      Simple to implement                                                        │
└──────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────────┐
│ BFS (Breadth-First Search)                                                       │
├──────────────────────────────────────────────────────────────────────────────────┤
│ Best Used For:                                                                   │
│                                                                                  │
│ 1. Shortest Path in Unweighted Graphs                                           │
│    • Robot navigation (equal cost moves)                                        │
│    • Game AI (move planning)                                                    │
│    • Social networks (degrees of separation)                                    │
│                                                                                  │
│ 2. Bipartite Graph Testing                                                      │
│    • Graph coloring with 2 colors                                               │
│    • Matching problems                                                          │
│                                                                                  │
│ 3. Level-Order Tree Traversal                                                   │
│    • Convert tree to linked list by depth                                       │
│    • Tree serialization                                                         │
│                                                                                  │
│ 4. Peer-to-Peer Networks                                                        │
│    • Finding nearest neighbors                                                  │
│    • Network broadcast (flood fill)                                             │
│                                                                                  │
│ 5. Web Crawling                                                                 │
│    • Breadth-first exploration of web                                           │
│    • Finding pages at specific distance from start                              │
│                                                                                  │
│ 6. Multi-Source Shortest Path                                                   │
│    • Object detection boundaries (in image processing)                          │
│    • Spreading activation in neural networks                                    │
│                                                                                  │
│ Why: Guarantees shortest path in unweighted case                                │
│      Systematic exploration level by level                                      │
│      Good for connectivity analysis                                             │
└──────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────────┐
│ A* ALGORITHM                                                                     │
├──────────────────────────────────────────────────────────────────────────────────┤
│ Best Used For:                                                                   │
│                                                                                  │
│ 1. GPS and Route Planning                                                       │
│    • Navigation systems (Google Maps, Waze)                                     │
│    • Urban routing with actual distances as weights                             │
│    • Flight path optimization                                                   │
│                                                                                  │
│ 2. Video Game Pathfinding (MOST COMMON!)                                        │
│    • NPC movement                                                               │
│    • Enemy AI pathfinding                                                       │
│    • Real-time strategy games                                                   │
│                                                                                  │
│ 3. Robot Motion Planning                                                        │
│    • Autonomous robots avoiding obstacles                                       │
│    • Warehouse robots (e.g., Amazon robots)                                     │
│    • Drones navigating environments                                             │
│                                                                                  │
│ 4. Puzzle Solving (if you have good heuristic)                                  │
│    • 8-puzzle or 15-puzzle                                                      │
│    • Rubik's cube solving                                                       │
│                                                                                  │
│ 5. Resource Allocation Problems                                                 │
│    • Finding optimal assignment with constraints                                │
│    • Job scheduling                                                             │
│                                                                                  │
│ 6. Heuristic Search in Artificial Intelligence                                  │
│    • Game tree search (with good evaluation heuristics)                          │
│    • Planning and scheduling                                                    │
│    • Information retrieval                                                      │
│                                                                                  │
│ 7. Network Routing Protocols                                                    │
│    • OSPF (Open Shortest Path First) uses similar concepts                      │
│    • Finding optimal paths in computer networks                                 │
│                                                                                  │
│ Why: Finds optimal paths efficiently                                            │
│      Heuristic guides search toward goal                                        │
│      Balances completeness with efficiency                                      │
│      Real-world applications need minimum-cost solutions                        │
└──────────────────────────────────────────────────────────────────────────────────┘
""")


# ============================================================================
# 8. WHEN TO USE EACH ALGORITHM
# ============================================================================

print("\n" + "=" * 90)
print("8. DECISION GUIDE: WHICH ALGORITHM TO USE?")
print("=" * 90)

print("""
Use this decision tree to choose the right algorithm:

START: "I need to find a path in a graph"
  │
  ├─ Question 1: "Is the graph weighted?" (Do edges have different costs?)
  │    │
  │    ├─ YES (weighted edges)
  │    │    │
  │    │    ├─ Question 2: "Can I define a good heuristic?"
  │    │    │    │
  │    │    │    ├─ YES (I can estimate remaining cost)
  │    │    │    │    └─→ USE A* ALGORITHM ⭐
  │    │    │    │        Best choice for weighted graphs with heuristic
  │    │    │    │        • Game pathfinding
  │    │    │    │        • Route planning
  │    │    │    │        • Robot navigation
  │    │    │    │
  │    │    │    └─ NO (No good heuristic)
  │    │    │         └─→ USE DIJKSTRA'S ALGORITHM
  │    │    │             (Similar to A* but without heuristic)
  │    │    │             • Network routing
  │    │    │             • General weighted shortest path
  │    │    │
  │    │    └─ Question 3: "Do I need optimal solution?"
  │    │         │
  │    │         ├─ YES 
  │    │         │    └─→ A* or Dijkstra (see above)
  │    │         │
  │    │         └─ NO (Any path is fine)
  │    │              └─→ USE DFS
  │    │                  Faster, uses less memory
  │    │
  │    └─ NO (unweighted edges, or all edges cost 1)
  │         │
  │         ├─ Question 2: "Do I need SHORTEST path?" (by edge count)
  │         │    │
  │         │    ├─ YES
  │         │    │    └─→ USE BFS ⭐
  │         │    │        Guarantees shortest path
  │         │    │        Linear time: O(V+E)
  │         │    │
  │         │    └─ NO (Any path is fine)
  │         │         └─→ USE DFS
  │         │             Simpler, less memory
  │         │
  │         └─ Question 3: "Memory is a critical constraint?"
  │              │
  │              ├─ YES
  │              │    └─→ USE DFS
  │              │        O(h) space vs BFS O(w)
  │              │
  │              └─ NO
  │                   └─→ USE BFS
  │                       Systematic exploration
  │
  └─ Question 4: "What's the problem type?"
       │
       ├─ Topological sort / cycle detection / SCC
       │    └─→ USE DFS
       │
       ├─ Shortest path unweighted
       │    └─→ USE BFS
       │
       ├─ Shortest path weighted
       │    └─→ USE A* or Dijkstra
       │
       ├─ Backtracking / Puzzle solving
       │    └─→ USE DFS
       │
       └─ Game pathfinding / Navigation
            └─→ USE A*


QUICK REFERENCE:

┌─────────────────────────┬────────────────────────────────┐
│ Problem                 │ Algorithm                      │
├─────────────────────────┼────────────────────────────────┤
│ Find any path           │ DFS (simple, fast)             │
│ Find shortest path      │ BFS (unweighted)               │
│ Find min-cost path      │ A* or Dijkstra                 │
│ Cycle detection         │ DFS                            │
│ Topological sort        │ DFS                            │
│ Game AI pathfinding     │ A*                             │
│ Social degree sep       │ BFS                            │
│ Route planning          │ A*                             │
│ Memory constrained      │ DFS                            │
│ Connectedcomponents    │ DFS or BFS                      │
└─────────────────────────┴────────────────────────────────┘
""")


# ============================================================================
# 9. REAL EXAMPLE COMPARISON WITH OUR GRAPH
# ============================================================================

print("\n" + "=" * 90)
print("9. EXAMPLE WITH OUR SPECIFIC GRAPH (S to G)")
print("=" * 90)

print("""
Graph Layout:
                     S (Start)
                    / \\
                   /2 \\4
                  /     \\
              B_top ← → B_bottom
              /  \\    /   |   \\
         5/3 |   |1 |     |3   \\1
            / \\  / \\ |     |     \\
           C ←→ F ←→ | ←─→ E     |
           |\\   |/  S              |
         3/ \\ 2/  (in center)     |
          /   X                    |
         /   / \\                   |
        G ←─────'                  |
  (Goal)      \\ Connect back to S /

Key Paths to G from S:
1. S → B_top → G      (cost: 2 + 5 = 7)      ← OPTIMAL!
2. S → B_top → C → G  (cost: 2 + 5 + 3 = 10)
3. S → B_bottom → C → G    (cost: 4 + 1 + 3 = 8)
4. S → B_bottom → F → G    (cost: 4 + 1 + 3 = 8)


DFS RESULT:
─────────────
Exploration order (depends on neighbor order):
If neighbors ordered as [B_top, B_bottom]:
  Pop S → push [B_top, B_bottom]
  Pop B_top → push [G, C]
  Pop C → G already in stack, continue
  Pop G → FOUND!
  
Path: S → B_top → G (cost: 7)
Nodes expanded: 3-4
Quality: GOOD! (Found optimal by luck)
Issue: Not guaranteed to be optimal


BFS RESULT:
──────────
Explores level by level:
  Level 0: S
  Level 1: B_top, B_bottom
  Level 2: C, G (from B_top), F (from B_bottom)
  
First path to G: Level 2
Path: S → B_top → G (cost: 7)
Nodes expanded: 4
Quality: GOOD for unweighted (shortest path by edges)
But: Cost is 7 because B_top→G has weight 5!
Note: BFS shortest by edges (2), but this happens to beoptimal


A* RESULT:
──────────
Using heuristics: h(S)=6, h(B_top)=5, h(B_bottom)=4, h(C)=3, h(G)=0

Step 1: Expand S
  f(S) = g(S) + h(S) = 0 + 6 = 6 (already expanded)
  Add to open: B_top (f=0+2+5=7), B_bottom (f=0+4+4=8)

Step 2: Expand B_top (lowest f=7)
  g(B_top) = 2
  Add to open: C (f=2+5+3=10), G (f=2+5+0=7)
  Already in open: B_bottom

Step 3: Now open has: G(f=7), B_bottom(f=8), C(f=10)
  Expand G (f=7, and it's the goal!)
  
Path: S → B_top → G (cost: 7)
Nodes expanded: 3
Quality: OPTIMAL! (cost: 7)
Note: Found path with fewer expansions than BFS!


COMPARISON SUMMARY:
───────────────────
┌──────────┬──────────────────────┬───────────┬──────────────────┬─────────────┐
│ Algorithm│ Path                 │ Cost      │ Nodes Expanded   │ Optimality  │
├──────────┼──────────────────────┼───────────┼──────────────────┼─────────────┤
│ DFS      │ S → B_top → G        │ 7         │ 3-4              │ Sometimes   │
│          │ (if lucky w/ order)  │           │                  │ (not guaranteed)
├──────────┼──────────────────────┼───────────┼──────────────────┼─────────────┤
│ BFS      │ S → B_top → G        │ 7         │ 4                │ Shortest by │
│          │                      │           │                  │ edges (good)│
├──────────┼──────────────────────┼───────────┼──────────────────┼─────────────┤
│ A*       │ S → B_top → G        │ 7         │ 3                │ OPTIMAL!    │
│          │                      │           │                  │ (guaranteed)│
└──────────┴──────────────────────┴───────────┴──────────────────┴─────────────┘

KEY OBSERVATIONS:
• All found the same path (by luck/by property of this graph)
• A* found it with fewest expansions: 3 nodes
• DFS was fastest but could have been worse with different neighbor order
• BFS was systematic but slightly less efficient than A*
• A* is the winner here: optimal path with fewest expansions
""")


# ============================================================================
# 10. CONCLUSION
# ============================================================================

print("\n" + "=" * 90)
print("10. CONCLUSION AND KEY TAKEAWAYS")
print("=" * 90)

print("""
┌──────────────────────────────────────────────────────────────────────────────────┐
│ KEY MATHEMATICAL PROPERTIES                                                      │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│ 1. COMPLETENESS (Will algorithm find solution if it exists?)                     │
│    DFS:  YES* (if depth is finite)                                              │
│    BFS:  YES  (always)                                                          │
│    A*:   YES* (if heuristic is admissible)                                      │
│                                                                                  │
│    ★ NOTE: Admissible means h(n) ≤ actual_cost(n to goal)                       │
│                                                                                  │
│ 2. OPTIMALITY (Will algorithm find minimum-cost solution?)                       │
│    DFS:  NO   (returns first path found, not cheapest)                          │
│    BFS:  SORT OF (optimal for unweighted, not for weighted)                     │
│    A*:   YES* (if heuristic is admissible)                                      │
│                                                                                  │
│    ★ CRITICAL: A* optimality requires admissible heuristic                      │
│                                                                                  │
│ 3. TIME COMPLEXITY                                                               │
│    DFS:  O(V + E) - linear in graph size                                        │
│    BFS:  O(V + E) - linear in graph size                                        │
│    A*:   O(E log V) with good heuristic, exponential in worst case              │
│                                                                                  │
│    ★ PRACTICAL: A* is slower per operation but explores fewer nodes             │
│                                                                                  │
│ 4. SPACE COMPLEXITY                                                              │
│    DFS:  O(h) - best, depth of tree                                             │
│    BFS:  O(w) - worst, width of tree                                            │
│    A*:   O(V) - between DFS and BFS                                             │
│                                                                                  │
│    ★ MEMORY: DFS is most memory-efficient                                       │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘

FINAL RECOMMENDATIONS:
═════════════════════════════════════════════════════════════════════════════════

When you have WEIGHTED GRAPH and CAN DEFINE HEURISTIC:
   → USE A* ALGORITHM ⭐⭐⭐
   Pros: Optimal, efficient exploration, industry standard
   Cons: Complex to implement, needs good heuristic
   Examples: GPS navigation, game AI, robot path planning

When you have UNWEIGHTED GRAPH or IGNORING WEIGHTS:
   → USE BFS ALGORITHM ⭐⭐
   Pros: Guaranteed shortest path (by edges), simple, linear time
   Cons: More memory than DFS
   Examples: Social networks, level-by-level traversal

When MEMORY IS CRITICAL or you just need ANY PATH:
   → USE DFS ALGORITHM ⭐
   Pros: Simplest, least memory, excellent for specific problems
   Cons: Not optimal, order-dependent
   Examples: Cycle detection, topological sort, recursive problems

INDUSTRY STANDARDS:
───────────────────
• Video Games: A* (standard for NPC pathfinding)
• GPS/Maps: A* with geographic heuristic
• Network Routing: Dijkstra (A* without heuristic)
• Machine Learning: A* variations (BFS* algorithms)
• Web Search: BFS-like algorithms
• Compilers: DFS (for dependency and cycle detection)

REMEMBER:
═════════════════════════════════════════════════════════════════════════════════
The choice of algorithm depends on:
1. Your problem requirements (any path vs shortest vs minimum-cost)
2. Graph properties (weighted vs unweighted)
3. Your constraints (time, memory, heuristic availability)
4. The structure of your specific graph

There is NO universally "best" algorithm - each has its place!
""")

print("\n" + "█" * 90)
print("█" + " " * 88 + "█")
print("█" + " " * 35 + "END OF ANALYSIS" + " " * 39 + "█")
print("█" + " " * 88 + "█")
print("█" * 90 + "\n")
