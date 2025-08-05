"""
Two players play a game called Tower Breakers:
There are n towers, each of height m.
The players take turns; Player 1 always goes first.

On a turn, a player can choose one tower of height h and reduce it to height h', where:
1 <= h' < h
h' must evenly divide h (i.e., h % h' == 0)

If a player cannot make a move, they lose.

Input: Two integers
n (number of towers) and
m (initial height of each tower)

Goal:
Determine which player will win assuming both play optimally.
"""

def tower_breakers(n: int, m: int) -> int:
    # All towers are of height 1, so no moves are possible.
    # Player 1 loses immediately.
    # Winner: Player 2
    if m == 1:
        return 2

    # If n is even, Player 2 can mirror Player 1's moves and win
    if n % 2 == 0:
        return 2

    # Otherwise with optimal play, Player 1 wins
    # Else (n is odd and m > 1):
    # Player 1 can break symmetry early and force a win.
    return 1

