# ============================================================
#   BAHRIA UNIVERSITY, ISLAMABAD CAMPUS
#   Department of Software Engineering
#   Mid Term Examination — Spring 2026
#   Subject : Artificial Intelligence  |  Code: CSC-411
#   Student : Enrollment 057
#   Task    : TASK 2 — A* Search Implementation
# ============================================================

import heapq
import itertools
import os
import time as time_module


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# ─────────────────────────────────────────────────────────────
#   STUDENT PARAMETERS  (Enrollment: 057)
# ─────────────────────────────────────────────────────────────
ENROLLMENT_ID = 57
LAST_DIGIT    = ENROLLMENT_ID % 10          # → 7
F_MAX         = 15 + LAST_DIGIT             # → 22 units
IS_ODD        = (ENROLLMENT_ID % 2 != 0)   # → True


# ─────────────────────────────────────────────────────────────
#   GRAPH — Adjacency List  (neighbor, travel_cost)
# ─────────────────────────────────────────────────────────────
GRAPH = {
    'S': [('A', 2), ('B', 5)],
    'A': [('C', 3), ('G', 10)],
    'B': [('D', 2), ('E', 4)],
    'C': [('G', 4), ('D', 1)],
    'D': [('G', 6)],
    'E': [],            # dead end
    'G': []
}


# ─────────────────────────────────────────────────────────────
#   HEURISTIC — Precomputed admissible lower bounds
#
#   DIST_TO_C[n]  = minimum cost to reach C from n
#   DIST_TO_G[n]  = minimum cost to reach G from n (kit already held)
#
#   h(n, has_kit=False) = DIST_TO_C[n] + DIST_TO_G['C']
#   h(n, has_kit=True)  = DIST_TO_G[n]
#
#   Admissible: these are actual shortest-path lower bounds,
#   so they never overestimate the true remaining cost.
# ─────────────────────────────────────────────────────────────
DIST_TO_C = {
    'S': 5,             # S→A(2)→C(3)
    'A': 3,             # A→C direct
    'B': float('inf'), # B has no path to C
    'C': 0,
    'D': float('inf'), # D has no path to C
    'E': float('inf'),
    'G': float('inf')
}

DIST_TO_G = {
    'S': 9,             # S→A→C→G = 2+3+4
    'A': 7,             # A→C→G   = 3+4
    'B': 8,             # B→D→G   = 2+6
    'C': 4,             # C→G direct
    'D': 6,             # D→G direct
    'E': float('inf'),  # dead end
    'G': 0
}


def heuristic(node: str, has_kit: bool) -> float:
    """Admissible h(n) — guaranteed to never overestimate."""
    if has_kit:
        return DIST_TO_G.get(node, float('inf'))
    else:
        to_c = DIST_TO_C.get(node, float('inf'))
        if to_c == float('inf'):
            return float('inf')
        return to_c + DIST_TO_G['C']   # cost to C  +  cost C→G


# ─────────────────────────────────────────────────────────────
#   DYNAMIC CONSTRAINT — Temporal Bridge Collapse
# ─────────────────────────────────────────────────────────────
def is_edge_blocked(frm: str, to: str, current_t: int) -> bool:
    """
    Returns True when an edge has collapsed due to the
    temporal event tied to the student's ID parity.

    ODD  (057): A → C blocked when current_t >= 8
    EVEN      : C → G blocked when current_t >= 10
    """
    if IS_ODD:
        return frm == 'A' and to == 'C' and current_t >= 8
    else:
        return frm == 'C' and to == 'G' and current_t >= 10


# ─────────────────────────────────────────────────────────────
#   A* SEARCH
# ─────────────────────────────────────────────────────────────
def a_star_search(verbose: bool = False):
    """
    A* Search for the Medical Logistics Crisis.

    State tuple: (node, has_kit, fuel, time_elapsed, has_refueled)
    ─────────────────────────────────────────────────────────────
    Priority Queue element: (f_score, tie_counter, state, path)

    Visited key: (node, has_kit, has_refueled)
      With an admissible heuristic, the first time A* pops
      a state key it has already found the optimal cost.
    """
    # ── Initialise ──────────────────────────────────────────
    initial_state = ('S', False, F_MAX, 0, False)
    h0 = heuristic('S', False)
    counter = itertools.count()          # tie-breaker — avoids comparing tuples

    pq      = [(h0, next(counter), initial_state, ['S'])]
    visited = set()
    nodes_expanded = 0

    print(f"\n  Enrollment  : 057")
    print(f"  Fmax        : {F_MAX} fuel units")
    parity_info = "A → C blocked at T ≥ 8  (ODD)" if IS_ODD else "C → G blocked at T ≥ 10 (EVEN)"
    print(f"  Temporal    : {parity_info}")
    print("─" * 65)

    if verbose:
        print(f"\n  {'#':<4} {'Node':<5} {'Kit':<6} {'Fuel':<5} {'T':<4}"
              f"  {'g':<5} {'h':<7} {'f':<7}  Path")
        print("─" * 78)

    # ── Search Loop ─────────────────────────────────────────
    while pq:
        f, _, state, path = heapq.heappop(pq)
        node, has_kit, fuel, t, has_refueled = state

        # Duplicate check
        s_key = (node, has_kit, has_refueled)
        if s_key in visited:
            continue
        visited.add(s_key)
        nodes_expanded += 1

        if verbose:
            g_val = t
            h_val = heuristic(node, has_kit)
            print(f"  {nodes_expanded:<4} {node:<5} {str(has_kit):<6} {fuel:<5} {t:<4}"
                  f"  {g_val:<5} {h_val:<7.3f} {f:<7.3f}  {' → '.join(path)}")

        # ── Goal Test ────────────────────────────────────────
        if node == 'G' and has_kit:
            _print_success(path, t, fuel, nodes_expanded)
            return path, t, fuel, nodes_expanded

        # ── Fuel out — terminal failure state ────────────────
        if fuel == 0:
            if verbose:
                print(f"  {'':4} [FUEL EMPTY — cannot expand further]")
            continue

        # ── Expand Neighbours ────────────────────────────────
        for neighbour, cost in GRAPH[node]:

            # 1. Dynamic collapse check
            if is_edge_blocked(node, neighbour, t):
                if verbose:
                    print(f"  {'':4} [COLLAPSE] {node}→{neighbour}  at T={t}")
                continue

            # 2. Fuel check
            new_fuel = fuel - cost
            if new_fuel < 0:
                if verbose:
                    print(f"  {'':4} [NO FUEL ] {node}→{neighbour}  needs {cost}, have {fuel}")
                continue

            new_time     = t + cost
            new_kit      = has_kit or (neighbour == 'C')
            new_refueled = has_refueled

            # 3. Refuel at Station B (once only)
            if neighbour == 'B' and not has_refueled:
                new_fuel     = F_MAX
                new_refueled = True
                if verbose:
                    print(f"  {'':4} [REFUEL  ] Reached B — fuel reset to {F_MAX}")

            new_key = (neighbour, new_kit, new_refueled)
            if new_key not in visited:
                new_h = heuristic(neighbour, new_kit)
                if new_h < float('inf'):               # skip provably dead ends
                    new_g = new_time
                    new_f = new_g + new_h
                    new_state = (neighbour, new_kit, new_fuel, new_time, new_refueled)
                    heapq.heappush(pq, (new_f, next(counter), new_state, path + [neighbour]))

    # ── No solution found ────────────────────────────────────
    print("\n" + "═" * 65)
    print("  ✗  MISSION FAILED — No valid path exists.")
    print("     (All routes exhausted or collapsed by temporal event)")
    print("═" * 65)
    return None, None, None, nodes_expanded


def _print_success(path, t, fuel, expanded):
    print("\n" + "═" * 65)
    print("  ★   MISSION ACCOMPLISHED — Medical Kit Delivered!   ★")
    print("═" * 65)
    print(f"  Final Path         : {' → '.join(path)}")
    print(f"  Total Time Taken   : {t} units")
    print(f"  Remaining Fuel     : {fuel} units")
    print(f"  Nodes Expanded     : {expanded}")
    print("═" * 65)


# ─────────────────────────────────────────────────────────────
#   DISPLAY HELPERS
# ─────────────────────────────────────────────────────────────
def header():
    print("=" * 65)
    print("    BAHRIA UNIVERSITY, ISLAMABAD CAMPUS")
    print("    Dept. of Software Engineering — Mid Term 2026")
    print("    Subject : Artificial Intelligence  |  CSC-411")
    print("    Enrollment: 057        Faculty: Engr. Saad Mazhar Khan")
    print("=" * 65)
    print("          TASK 2 — A* SEARCH IMPLEMENTATION")
    print("=" * 65)


def show_config():
    print(f"""
  ┌──────────────────────────────────────────────────────┐
  │  CONFIGURATION  (Student Enrollment: 057)            │
  ├──────────────────────────────────────────────────────┤
  │  Last digit of ID  : {LAST_DIGIT}                             │
  │  Initial Fuel Fmax : 15 + {LAST_DIGIT}  =  {F_MAX} units            │
  │  ID Parity         : ODD                             │
  │  Temporal Event    : A → C collapses at T ≥ 8       │
  └──────────────────────────────────────────────────────┘

  GRAPH STRUCTURE:
  ──────────────────────────────────────────────────────
  S   →  A (cost 2)   B (cost 5)
  A   →  C (cost 3)   G (cost 10)
  B   →  D (cost 2)   E (cost 4)    ← Refuel → resets to {F_MAX}
  C   →  G (cost 4)   D (cost 1)    ← Must visit to grab kit
  D   →  G (cost 6)
  E   →  (dead end — no outgoing edges)
  G   →  GOAL

  ADMISSIBLE HEURISTIC USED:
  ──────────────────────────────────────────────────────
  h(n, no kit) = min_dist(n → C) + min_dist(C → G)
  h(n, has kit)= min_dist(n → G)

  Precomputed values used internally:
    Node  dist_to_C  dist_to_G
    S     5          9
    A     3          7
    B     ∞          8   (cannot reach C from B)
    C     0          4
    D     ∞          6   (cannot reach C from D)
    G     ∞          0
    """)
    input("  Press Enter to return to menu...")


# ─────────────────────────────────────────────────────────────
#   MAIN MENU
# ─────────────────────────────────────────────────────────────
def main_menu():
    while True:
        clear()
        header()
        print("""
    ┌────────────────────────────────────────────────────────┐
    │                      MAIN MENU                         │
    ├────────────────────────────────────────────────────────┤
    │  [1]  Run A* Search  —  Normal Output                  │
    │  [2]  Run A* Search  —  Verbose / Step-by-Step         │
    │  [3]  Show Configuration & Graph                       │
    │  [0]  Exit Task 2                                      │
    └────────────────────────────────────────────────────────┘""")
        choice = input("\n    Enter your choice: ").strip()

        if choice == '1':
            clear()
            header()
            a_star_search(verbose=False)
            input("\n  Press Enter to return to menu...")

        elif choice == '2':
            clear()
            header()
            a_star_search(verbose=True)
            input("\n  Press Enter to return to menu...")

        elif choice == '3':
            clear()
            header()
            show_config()

        elif choice == '0':
            print("\n    Goodbye! Exiting Task 2.\n")
            break

        else:
            print("\n    Invalid choice — please enter 0, 1, 2, or 3.")
            time_module.sleep(1)


if __name__ == "__main__":
    main_menu()
