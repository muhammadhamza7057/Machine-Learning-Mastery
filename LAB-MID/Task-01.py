# ============================================================
#   BAHRIA UNIVERSITY, ISLAMABAD CAMPUS
#   Department of Software Engineering
#   Mid Term Examination — Spring 2026
#   Subject : Artificial Intelligence  |  Code: CSC-411
#   Student : Enrollment 057
#   Task    : TASK 1 — Formal State Modeling
# ============================================================

import os
import time


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def header():
    print("=" * 65)
    print("    BAHRIA UNIVERSITY, ISLAMABAD CAMPUS")
    print("    Dept. of Software Engineering — Mid Term 2026")
    print("    Subject : Artificial Intelligence  |  CSC-411")
    print("    Enrollment: 057        Faculty: Engr. Saad Mazhar Khan")
    print("=" * 65)
    print("           TASK 1 — FORMAL STATE MODELING")
    print("=" * 65)


# ─────────────────────────────────────────────────────────────
#   SECTION 1 — State Representation
# ─────────────────────────────────────────────────────────────
def show_state_representation():
    print("""
  ┌─────────────────────────────────────────────────────────┐
  │  STATE = (node, has_kit, fuel, time_elapsed, refueled) │
  └─────────────────────────────────────────────────────────┘

  Each element explained:

    node          → Current location of the ARV
                    Possible values: S, A, B, C, D, E, G

    has_kit       → Boolean — True if Medical Kit was collected
                    (i.e., agent has visited Node C)

    fuel          → Integer — Remaining fuel units
                    Starts at Fmax = 22  (Last digit 7 → 15+7)

    time_elapsed  → Integer — Total time units consumed so far
                    Each unit of travel cost = 1 unit of time

    refueled      → Boolean — True if Station B refuel was used
                    (Station B resets fuel to Fmax ONCE only)

  ─────────────────────────────────────────────────────────
  EXAMPLE STATES:
    ('S', False, 22, 0,  False)  →  Start, full fuel, no kit
    ('A', False, 20, 2,  False)  →  At A, arrived via S→A
    ('C', True,  17, 5,  False)  →  At C, kit collected!
    ('G', True,  13, 9,  False)  →  GOAL — kit delivered
    ('B', False, 22, 5,  True )  →  At B, tank refilled
  ─────────────────────────────────────────────────────────

  WHY CAN'T THE STATE BE JUST THE NODE NAME?
  ───────────────────────────────────────────
  In basic graph search, node name alone identifies a state.
  This problem CANNOT use that simplification because:

  [1] MANDATORY ITEM PICKUP
      Being at node C *with* the kit is completely different
      from being at C *without* it. The goal test at G only
      passes when has_kit = True. Same node, different meaning.

  [2] FUEL — RESOURCE CONSTRAINT
      Arriving at D with 5 fuel remaining vs 18 fuel remaining
      determines which future moves are even possible. Running
      out of fuel = Mission Failed (terminal state).

  [3] TIME — TEMPORAL COLLAPSES (Dynamic Environment)
      Enrollment 057 is ODD → Edge A→C collapses at T ≥ 8.
      Being at node A at T=2 allows using A→C.
      Being at node A at T=9 does NOT — the bridge is gone.
      Same node, different time = different available actions.

  [4] REFUEL STATUS
      Node B resets fuel ONCE. After refueling, revisiting B
      has no effect. Tracking this prevents incorrect shortcuts.

  CONCLUSION:
      A single node name cannot capture fuel level, time,
      item status, or refuel history. All five dimensions of
      the tuple are required for a correct, complete state.
    """)
    input("  Press Enter to return to menu...")


# ─────────────────────────────────────────────────────────────
#   SECTION 2 — Heuristic Function h(n)
# ─────────────────────────────────────────────────────────────
def show_heuristic():
    import math
    print("""
  ─────────────────────────────────────────────────────────
  HEURISTIC FUNCTION  h(n)
  ─────────────────────────────────────────────────────────

  We use a EUCLIDEAN-STYLE heuristic based on approximate
  node coordinates on a 2-D plane.

  Node Coordinates Assigned:
  ┌──────┬──────────┐
  │ Node │ (X,  Y)  │
  ├──────┼──────────┤
  │  S   │ (0,  0)  │
  │  A   │ (2,  2)  │
  │  B   │ (2, -2)  │
  │  C   │ (5,  3)  │
  │  D   │ (4, -1)  │
  │  E   │ (2, -5)  │
  │  G   │ (9,  1)  │
  └──────┴──────────┘

  Euclidean Distance Formula:
      dist(X, Y) = sqrt( (x2-x1)² + (y2-y1)² )

  ─────────────────────────────────────────────────────────
  HEURISTIC LOGIC (Two Cases):

  Case 1 — Agent has NOT collected the Medical Kit:
      h(n) = dist(n, C)  +  dist(C, G)
      → Agent must detour to C first, THEN proceed to G
      → Heuristic accounts for the mandatory stop

  Case 2 — Agent HAS the Medical Kit:
      h(n) = dist(n, G)
      → Direct lower bound to the goal node

  ─────────────────────────────────────────────────────────
  ADMISSIBILITY:
      This heuristic is ADMISSIBLE because Euclidean distance
      is always ≤ actual path cost.  It NEVER overestimates
      the true remaining cost → guarantees optimal solution.

  ─────────────────────────────────────────────────────────
  SAMPLE CALCULATIONS:
    """)

    import math
    coords = {
        'S': (0, 0), 'A': (2, 2), 'B': (2, -2),
        'C': (5, 3), 'D': (4, -1), 'E': (2, -5), 'G': (9, 1)
    }

    def dist(a, b):
        ax, ay = coords[a]
        bx, by = coords[b]
        return math.sqrt((bx - ax)**2 + (by - ay)**2)

    s_no_kit = dist('S', 'C') + dist('C', 'G')
    a_no_kit = dist('A', 'C') + dist('C', 'G')
    c_kit    = dist('C', 'G')
    d_kit    = dist('D', 'G')

    print(f"    h(S, no kit) = dist(S,C) + dist(C,G)")
    print(f"                 = {dist('S','C'):.3f} + {dist('C','G'):.3f}  = {s_no_kit:.3f}")
    print()
    print(f"    h(A, no kit) = dist(A,C) + dist(C,G)")
    print(f"                 = {dist('A','C'):.3f} + {dist('C','G'):.3f}  = {a_no_kit:.3f}")
    print()
    print(f"    h(C, has kit)= dist(C,G)  = {c_kit:.3f}")
    print(f"    h(D, has kit)= dist(D,G)  = {d_kit:.3f}")
    print()
    input("  Press Enter to return to menu...")


# ─────────────────────────────────────────────────────────────
#   SECTION 3 — Student Variables
# ─────────────────────────────────────────────────────────────
def show_variables():
    print("""
  ─────────────────────────────────────────────────────────
  STUDENT VARIABLES (Enrollment: 057)
  ─────────────────────────────────────────────────────────

    Enrollment ID   :  057
    Last Digit      :  7
    Initial Fuel    :  Fmax  = 15 + 7  =  22 units
    ID Parity       :  ODD  (57 is an odd number)

  TEMPORAL EVENT (ODD Rule):
    Edge  A → C  collapses (becomes permanently blocked)
    at any time step where  T ≥ 8.

  IMPLICATION:
    The ARV must traverse A → C BEFORE time T = 8.

    Travel S → A costs 2 units  → arrive at A at T = 2.
    Travel A → C costs 3 units  → arrive at C at T = 5.

    Since T = 5 < 8, the path S → A → C is achievable if
    taken immediately from the start.

    If the agent visits B first:
        S → B costs 5  → arrive at B at T = 5.
        From B, there is NO route back to C!
        (B only connects to D and E — neither reaches C)
        → Route via B guarantees Mission Failure.

    The temporal constraint essentially FORCES the agent to
    commit to the S → A → C route without detours.

  ─────────────────────────────────────────────────────────
  GRAPH (Adjacency List):

    S  →  A(2),  B(5)
    A  →  C(3),  G(10)
    B  →  D(2),  E(4)    ← Refuel station (resets to 22)
    C  →  G(4),  D(1)    ← Must visit to collect kit
    D  →  G(6)
    E  →  (dead end)
    G  →  GOAL
  ─────────────────────────────────────────────────────────
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
    ┌─────────────────────────────────────────────────────┐
    │                    MAIN MENU                        │
    ├─────────────────────────────────────────────────────┤
    │  [1]  State Representation  &  Why Not Node Name   │
    │  [2]  Heuristic Function  h(n)  Design             │
    │  [3]  Student Variables  (Fuel, Temporal Event)    │
    │  [0]  Exit Task 1                                  │
    └─────────────────────────────────────────────────────┘""")
        choice = input("\n    Enter your choice: ").strip()

        if choice == '1':
            clear()
            header()
            show_state_representation()
        elif choice == '2':
            clear()
            header()
            show_heuristic()
        elif choice == '3':
            clear()
            header()
            show_variables()
        elif choice == '0':
            print("\n    Goodbye! Exiting Task 1.\n")
            break
        else:
            print("\n    Invalid choice — please enter 0, 1, 2, or 3.")
            time.sleep(1)


if __name__ == "__main__":
    main_menu()
