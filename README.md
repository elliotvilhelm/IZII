# IZII

IZII is a Python based Chess Engine providing move generation, board evaluation, and a minimax search algorithm.

IZII makes its decisions in two steps 
1. Move Generation -> Pseudo legal moves filtered to legal moves
2. Move Search -> Using a board evaluation function IZII runs minimax search with Alpha-Beta pruning to discover the optimal move

IZII provides two key functions:
get_all_moves_at_state -> inputs: state | outputs: all possible moves
run_move_at_state -> inputs: state, move | outputs: next state

To implement IZZI I use

![120sqboard](/images/120sqboard.png?raw=true "120 square board")
