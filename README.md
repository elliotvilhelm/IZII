#### IZII
## Overview:
IZII is a Python based Chess Engine

Decisions are made using the minimax search algorithm with alpha-beta pruning to optimize search time. The engine is compatible with xboard and uses the xboard protocol. 

IZII makes its decisions in two steps 
1. Move Generation -> Pseudo legal moves filtered to legal moves
2. Move Search -> Using a board evaluation function IZII runs minimax search with Alpha-Beta pruning to discover the optimal move

IZII provides two key functions for playing chess:
#get_all_moves_at_state -> inputs: state | outputs: all possible moves
#run_move_at_state -> inputs: state, move | outputs: next state

## Execution
To run IZII, download all files to your local system. You also must have [xboard](https://www.gnu.org/software/xboard/) or any other GUI with xboard protocol compatibility. 

To play the engine, cd into the source directory and run: 
```python3
xboard -cp -fcp "python3 xboard.py"
```
Furthermore, to watch IZII play itself you can run, 
```python3
xboard -cp -fcp "python3 xboard.py" -scp "python3 xboard.py"
```
then press CTRL-t on the xboard GUI to run a two machine game.

## Development
To implement IZZI I used a 120 square chess board as used by cray-1, one of the first chess playing computers.
![120sqboard](/images/cray.png?raw=true "120 square board") ![120sqboard](/images/120sqboard.png?raw=true "120 square board")

Enjoy!
