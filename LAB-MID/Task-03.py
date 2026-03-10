# ============================================================
#   BAHRIA UNIVERSITY, ISLAMABAD CAMPUS
#   Department of Software Engineering
#   Mid Term Examination — Spring 2026
#   Subject : Artificial Intelligence  |  Code: CSC-411
#   Student : Enrollment 057
#   Task    : TASK 3 — Strategic Analysis
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
    print("             TASK 3 — STRATEGIC ANALYSIS")
    print("=" * 65)


# ─────────────────────────────────────────────────────────────
#   QUESTION 1 — Temporal Constraint Analysis
# ─────────────────────────────────────────────────────────────
def q1_temporal_analysis():
    print("""
  ══════════════════════════════════════════════════════════
  QUESTION 1
  Did the temporal constraint force a sub-optimal (longer)
  path? Explain why.
  ══════════════════════════════════════════════════════════

  STUDENT CONTEXT (Enrollment: 057 — ODD):
  ─────────────────────────────────────────
    Fmax        = 22 fuel units
    Constraint  = Edge  A → C  collapses at time T ≥ 8

  SHORT ANSWER:
  ─────────────────────────────────────────────────────────
    For Enrollment 057, the temporal constraint does NOT
    force a longer path — but it does eliminate an entire
    class of strategies, leaving S → A → C → G as the
    ONLY valid route.

  DETAILED REASONING:
  ─────────────────────────────────────────────────────────

  STEP-BY-STEP ANALYSIS OF ALL CANDIDATE PATHS:

  Path 1:  S → A → C → G
  ─────────────────────────────────────────────
    S→A : cost = 2  (arrive A at T=2)
    A→C : cost = 3  (start at T=2, arrive C at T=5)
          Is T=2 ≥ 8?  NO → edge A→C is OPEN ✔
    C→G : cost = 4  (arrive G at T=9)
    ─────────────────────────────────────────
    Time    = 9  |  Fuel used = 9  |  Remaining fuel = 13
    Has kit = YES at C ✔  |  Goal test at G = PASS ✔
    STATUS  → VALID & OPTIMAL

  Path 2:  S → A → C → D → G  (longer alternate)
  ─────────────────────────────────────────────
    Total cost = 2 + 3 + 1 + 6 = 12
    Arrives at A at T=2 → A→C still OPEN ✔
    Collects kit at C ✔
    STATUS  → VALID but sub-optimal (extra 3 time units)

  Path 3:  S → B → D → G  (no kit — through refuel station)
  ─────────────────────────────────────────────
    Total cost = 5 + 2 + 6 = 13
    Never visits C → has_kit = False
    Goal test at G = FAIL ✗
    STATUS  → INVALID (mission fails — no medical kit)

  Path 4:  S → A → G  (direct — skips C)
  ─────────────────────────────────────────────
    Total cost = 2 + 10 = 12
    Never visits C → has_kit = False
    STATUS  → INVALID

  Path 5:  S → B → ... → C → G  (via refuel first)
  ─────────────────────────────────────────────
    From B, only D and E are reachable.
    Neither D nor E connects to C anywhere in the graph.
    → There is NO path from B to C.
    STATUS  → STRUCTURALLY IMPOSSIBLE

  ┌─────────────────────────────────────┬──────┬──────┬────────┐
  │ Path                                │ Time │ Fuel │ Valid  │
  ├─────────────────────────────────────┼──────┼──────┼────────┤
  │ S → A → C → G          (optimal)   │  9   │  13  │  YES ✔ │
  │ S → A → C → D → G      (longer)    │  12  │  10  │  YES ✔ │
  │ S → A → G              (no kit)    │  12  │  10  │  NO  ✗ │
  │ S → B → D → G          (no kit)    │  13  │   9  │  NO  ✗ │
  │ S → B → ... → C → G   (no route)  │  —   │  —   │  NO  ✗ │
  └─────────────────────────────────────┴──────┴──────┴────────┘

  KEY INSIGHT — The Temporal Constraint as a Pressure Tool:
  ─────────────────────────────────────────────────────────
    Even though the optimal path S→A→C→G is unaffected for
    Enrollment 057 (A→C is traversed at T=2, well before T=8),
    the temporal constraint changes the agent's STRATEGY SPACE:

    • It rules out: going to B for refuel before heading to C.
      (Arriving at A after visiting B would be at T=5; then
       A→C traversal starts at T=5 → arrives T=8 → blocked!)
    • It forces the agent to prioritise the A→C route early.
    • It imposes urgency: the refuel detour is not free.

  CONCLUSION:
  ─────────────────────────────────────────────────────────
    The temporal event does NOT lengthen the final chosen
    path (S→A→C→G remains optimal at cost 9), but it does
    ELIMINATE all strategies that visit B before C, making
    the mission structurally simpler — or impossible if the
    agent wastes time.  The constraint acts as a survival
    pressure mechanism that rewards immediate commitment to
    the critical route.
    """)
    input("  Press Enter to return to menu...")


# ─────────────────────────────────────────────────────────────
#   QUESTION 2 — Time Complexity with Extra Depots
# ─────────────────────────────────────────────────────────────
def q2_complexity_analysis():
    print("""
  ══════════════════════════════════════════════════════════
  QUESTION 2
  How would Time Complexity change if we added 5 more
  Supply Depots?
  ══════════════════════════════════════════════════════════

  CURRENT SETUP (1 Supply Depot — Node C):
  ─────────────────────────────────────────
  State  =  (node, has_kit, fuel, time_elapsed, has_refueled)

    Dimension         Values
    ─────────────────────────────────────────────────────
    node              7 nodes  (S, A, B, C, D, E, G)
    has_kit           2 values  {True, False}
    fuel              0 … 22   =  23 possible levels
    time_elapsed      0 … ~30  ≈  30 values
    has_refueled      2 values  {True, False}
    ─────────────────────────────────────────────────────
    Approx. State Space ≈  7 × 2 × 23 × 30 × 2  =  19,320

  WITH 5 ADDITIONAL SUPPLY DEPOTS  (6 Total Depots):
  ─────────────────────────────────────────────────────────
  Each new depot adds a boolean "collected" flag to the state.
  Instead of one has_kit flag, we need a 6-bit bitmask:

    new_state = (node, kit_bitmask, fuel, time, refueled)
    kit_bitmask ∈  {0 … 63}  →  2^6 = 64 combinations

  Also, the number of nodes grows (6 new depot nodes added):
    nodes  →  7 + 5 = 12

    Dimension         Values (6 depots)
    ─────────────────────────────────────────────────────
    node              12 nodes
    kit_bitmask       2^6  =  64 combinations
    fuel              0 … 22  =  23 levels
    time_elapsed      ≈ 50 values  (longer paths now)
    has_refueled      2 values
    ─────────────────────────────────────────────────────
    State Space ≈  12 × 64 × 23 × 50 × 2  =  1,766,400

    Growth Factor  ≈  91×  vs original state space!

  FORMAL TIME COMPLEXITY:
  ─────────────────────────────────────────────────────────
  Let:
    |V|  = number of nodes
    k    = number of supply depots
    F    = Fmax  (fuel capacity)
    T    = maximum time horizon

  A* Time Complexity  =  O( |V| × 2^k × F × T × log(|V| × 2^k) )
                                         ↑
                               Each depot doubles the state space

  ┌──────────────────────────┬──────────────────────────────────┐
  │ Scenario                 │ Approximate Time Complexity      │
  ├──────────────────────────┼──────────────────────────────────┤
  │ 1 depot  (current)       │ O(|V| · 2¹ · F · T · log(…))   │
  │ 2 depots                 │ O(|V| · 2² · F · T · log(…))   │
  │ 6 depots  (+5 more)      │ O(|V| · 2⁶ · F · T · log(…))   │
  │ k depots  (general)      │ O(|V| · 2^k · F · T · log(…))  │
  └──────────────────────────┴──────────────────────────────────┘

  This is EXPONENTIAL in k — the classic Combinatorial Explosion
  problem. It is equivalent in structure to the Travelling
  Salesman Problem (TSP) for multiple mandatory visits.

  WHY IT GROWS THIS WAY:
  ─────────────────────────────────────────────────────────
    With k depots, the agent must determine which SUBSET it
    has collected so far. The number of distinct collection
    states = 2^k (each depot either collected or not).
    A* must track all of these separately, because two agents
    at the same node with different subsets of collected items
    are in genuinely DIFFERENT states — they have different
    remaining objectives and different valid goals.

  PRACTICAL MITIGATIONS:
  ─────────────────────────────────────────────────────────
    [1]  Bitmasking for compact state representation.
         kit_state as an integer (e.g., 0b101 = depots 0 and 2
         collected). Avoids storing tuples of booleans.

    [2]  Better Heuristic (more informed h(n)):
         Precompute minimum spanning tree or nearest-neighbor
         tour through uncollected depots + goal. Prunes more.

    [3]  IDA* — Iterative Deepening A*:
         Dramatically reduces MEMORY usage (only O(depth) stack)
         at the cost of re-expanding nodes. Good for large k.

    [4]  Hierarchical / Landmark Planning:
         Plan a high-level depot visit order first, then route-
         plan between each pair. Breaks the exponential problem
         into polynomial sub-problems.

    [5]  Greedy Nearest-Depot heuristic:
         Not optimal, but runs in polynomial time. Useful when
         k is large and optimality can be sacrificed for speed.

  CONCLUSION:
  ─────────────────────────────────────────────────────────
    Adding 5 depots changes time complexity from
    O(|V| · 2 · F · T) to O(|V| · 64 · F · T), a 32× jump
    in the state-space multiplier, making exhaustive A* search
    increasingly impractical. Hybrid approaches (bitmask +
    improved heuristic) are necessary for k > 4.
    """)
    input("  Press Enter to return to menu...")


# ─────────────────────────────────────────────────────────────
#   SOLUTION SUMMARY
# ─────────────────────────────────────────────────────────────
def show_summary():
    print("""
  ══════════════════════════════════════════════════════════
  COMPLETE SOLUTION SUMMARY  (Enrollment: 057)
  ══════════════════════════════════════════════════════════

  Student Variables:
  ─────────────────────────────────────────────────────────
    Enrollment ID    :  057
    Last Digit       :  7
    Initial Fuel     :  Fmax = 15 + 7  =  22 units
    ID Parity        :  ODD
    Temporal Event   :  Edge  A → C  collapses at T ≥ 8

  Task 1 — State Definition:
  ─────────────────────────────────────────────────────────
    State  =  (node, has_kit, fuel, time_elapsed, has_refueled)
    Heuristic:
      h(n, no kit) = dist(n→C) + dist(C→G)   [Euclidean-style]
      h(n, has kit)= dist(n→G)

  Task 2 — A* Search Result:
  ─────────────────────────────────────────────────────────
    Final Path       :  S → A → C → G
    Total Time Taken :  9 units
    Remaining Fuel   :  13 units
    (See Task-02.py for exact node expansion count)

  Task 3 — Strategic Analysis:
  ─────────────────────────────────────────────────────────
    Q1: Temporal constraint eliminates detours via B before C.
        Optimal path S→A→C→G (cost 9) is unforced but fragile:
        any prior detour would delay A→C past the T=8 deadline.

    Q2: 5 extra depots → complexity scales as O(2^k).
        State space grows ~91× harder (19K → 1.7M states).
        Mitigations: bitmask + IDA* + stronger heuristics.

  Algorithm Properties:
  ─────────────────────────────────────────────────────────
    Algorithm        :  A*  (informed best-first search)
    Heuristic type   :  Admissible (never overestimates)
    State space      :  5-tuple covering all constraints
    Completeness     :  Yes  (within fuel and time limits)
    Optimality       :  Yes  (admissible h guarantees it)
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
    ┌──────────────────────────────────────────────────────────┐
    │                       MAIN MENU                          │
    ├──────────────────────────────────────────────────────────┤
    │  [1]  Q1 — Temporal Constraint & Path Sub-Optimality    │
    │  [2]  Q2 — Time Complexity with 5 Extra Depots          │
    │  [3]  Full Solution Summary                              │
    │  [0]  Exit Task 3                                        │
    └──────────────────────────────────────────────────────────┘""")
        choice = input("\n    Enter your choice: ").strip()

        if choice == '1':
            clear()
            header()
            q1_temporal_analysis()
        elif choice == '2':
            clear()
            header()
            q2_complexity_analysis()
        elif choice == '3':
            clear()
            header()
            show_summary()
        elif choice == '0':
            print("\n    Goodbye! Exiting Task 3.\n")
            break
        else:
            print("\n    Invalid choice — please enter 0, 1, 2, or 3.")
            time.sleep(1)


if __name__ == "__main__":
    main_menu()
