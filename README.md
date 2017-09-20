# IZII
IZII is a Python based Chess Engine providing move generation, board evaluation, and a minimax search algorithm currently running a CPU vs CPU match

IZII makes its decisions in two steps 
1. Move Generation -> Pseudo legal moves filtered to legal moves
2. Move Search -> Using a board evaluation function IZII runs minimax search with Alpha-Beta pruning to discover the optimal move

IZII provides two key functions:
get_all_moves_at_state -> inputs: state | outputs: all possible moves
run_move_at_state -> inputs: state, move | outputs: next state

