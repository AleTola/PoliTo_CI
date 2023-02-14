# Quarto

This Quarto agents is implemented using a MinMax approach with alpha beta pruning. 

## Bounded-depth MinMax with alpha-beta pruning

The basic block of the chosen strategy is MinMax. However, since the game has a complexity which grows as the square of the factorial of the remaining pieces to be placed, a plain version of MinMax is not feasible. Two solutions are proposed: pruning and bounding the depth of the search tree.
- The used pruning is alpha-beta pruning. Alpha-Beta pruning is often combined with MinMax since it provides a cut-off of useless branches which higly reduces the complexity. 
- The bounded-depth is necessary due to the fact that, even with pruning, the entire search tree is not explorable in a feasible time. Thus, a bound is required in the early stages of the game, where the search is irrealistic. The max depth is fixed to 4 in order to achieve to choose a move or a piece in plausible times, but it can also be set to 5 even if some choices can take up to a max of 10 seconds.


## Scores and Heuristic

The chosen heuristic is based on the nature of the game. In Quarto, the winner is the first player placing four pieces on a row, column, or diagonal (forming a quarto) with at least one common characteristic. Starting from here an efficient heuristic to determine the "power" of a state not fully explored is based on "terzo". A terzo is a configuration of three pieces on a row, column, or diagonal with at least one common characteristic.
Notice that, considering at most one terzo per line (row, column or diagonal), there can be at most 10 terzos in a given board configuration (4 rows, 4 columns, 2 diagonals).

A move is thus evaluated according to these procedure:

- if it leads to a win, it obtains a value of 12
- if it leads to a draw, it obtains a value of 11
- otherwise it obtains an absolute value between 0 and 10 (endpoints included), according to how many terzo are present in the board

Notice that these values are "absolute" since, in MinMax, one player is minimizing while the other is maximizing, so the sign will be chosen accordingly to the current player.

A side note must be done for the value of a certain draw, i.e. 11. This value has been chosen because it is preferred to do a move which certainly does not lead to a loss rather than a move which is not certain (i.e. when its value is decided by the heuristic because the subtree cannot be fully explored). This is a conservative choice based on the decision of minimizing losses whenever possible.

## Experiments

Number of games: 1000

First Agent to Play: RandomPlayer

Second Agent to Play: myAgent

Max Depth of Minmax: 4

- Results: {win: 989, loss: 7, draw: 4} (Win rate: 99%)
- Turn timing: { 'select': 0.011 s, 'place': 0.490 s } on average, { 'select': 0.162 s, 'place': 2.622 s } max
- Match timing: 9.36 turns on average

Number of games: 1000

First Agent to Play: myAgent

Second Agent to Play: RandomPlayer

Max Depth of Minmax: 4

- Results: {win: , loss: , draw: } (Win rate: %)
- Turn timing: { 'select': 0.011 s, 'place': 0.490 s } on average, { 'select': 0.162 s, 'place': 2.622 s } max
- Match timing: 9.36 turns on average

----

Number of games: 100

First Agent to Play: RandomPlayer

Second Agent to Play: myAgent

Max Depth of Minmax: 5

- Results: {win: , loss: , draw: } (Win rate: %)
- Turn timing: { 'select': 0.011 s, 'place': 0.490 s } on average, { 'select': 0.162 s, 'place': 2.622 s } max
- Match timing: 9.36 turns on average

Number of games: 100

First Agent to Play: myAgent

Second Agent to Play: RandomPlayer

Max Depth of Minmax: 5

- Results: {win: , loss: , draw: } (Win rate: %)
- Turn timing: { 'select': 0.011 s, 'place': 0.490 s } on average, { 'select': 0.162 s, 'place': 2.622 s } max
- Match timing: 9.36 turns on average




