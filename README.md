# Quarto

This Quarto agents is implemented using a MinMax approach with alpha beta pruning. 

## Bounded-depth MinMax with alpha-beta pruning

The basic block of the chosen strategy is MinMax. However, since the game has a complexity which grows as the square of the factorial of the remaining pieces to be placed, a plain version of MinMax is not feasible. Two solutions are proposed: pruning and bounding the depth of the search tree.

The used pruning is fail-soft alpha-beta pruning1. Alpha-Beta pruning is often combined with MinMax since it provides a cut-off of useless branches which higly reduces the complexity. The fail-soft term represents a variant introduced by John P. Fishburn in 1983, which guarantees not to cut-off potentially useful branches (not guaranteed by the fail-hard variant). This variant was preferred since it theoretically explores all interesting branches and it does not slow down the search in a considerable way.

The bounded-depth is necessary due to the fact that, even with pruning, the entire search tree is not explorable in a feasible time. The game has a complexity of 16!2, i.e. 4.4 * 1026, which becomes 4.4 * 1013 with pruning. Thus, a bound is required in the early stages of the game, where the search is irrealistic. Notice that the search starts to be affordable when only 5/6 pieces are left to be placed, i.e. it is almost impossible to fully explore the game tree before 10/11 pieces are placed. Three strategies were used for bounding the search:

....


The varying-depth versions (i.e. bound = 2 or bound = 3), change the maximum depth at each turn through the function tweak_depth, which behaves like this:

- bound = 2, the maximum depth is not set (math.inf) if the complexity is lower than the bound_value, otherwise is set to 1. The complexity is calculated through an auxiliary static function estimate_tree_complexity, which returns a worst-case complexity based on the missing pieces to be placed.
- bound = 3, the maximum depth is the maximum between 1 (if bound_value is too low) and the result of an auxiliary static function find_depth, which returns the maximum number of levels whose full explorations leads to a number of visited states lower than bound_value.

## Scores

....

## Heuristic: Quarticity

The chosen heuristic is based on the nature of the game. In Quarto!, the winner is the first player placing four pieces on a row, column, or diagonal (forming a quarto) with at least one common characteristic. Starting from here and following the idea by D. Castro Silva and V. Vinhas2, an efficient heuristic to determine the "power" of a state not fully explored is based on "terzo". A terzo is a configuration of three pieces on a row, column, or diagonal with at least one common characteristic.

Notice that, considering at most one terzo per line (row, column or diagonal), there can be at most 10 terzos in a given board configuration (4 rows, 4 columns, 2 diagonals).

A move is thus evaluated according to these procedure:

- if it leads to a 100% winning state, it obtains an absolute value of 12
- if it leads to a 100% draw state, it obtains an absolute value of 11
- otherwise it obtains an absolute value between 0 and 10 (endpoints included), according to how many terzo are present in the board
- 
Notice that these values are "absolute" since, in MinMax, one player is minimizing while the other is maximizing, so the sign will be chosen accordingly to the current player.

A side note must be done for the value of a certain draw, i.e. 11. This value has been chosen because it is preferred to do a move which certainly does not lead to a loss rather than a move which is not certain (i.e. when its value is decided by the heuristic because the subtree cannot be fully explored). This is a conservative choice based on the decision of minimizing losses whenever possible.

## Experiments




