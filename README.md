[![Build Status](https://travis-ci.org/ElliotVilhelm/IZII.svg?branch=master)](https://travis-ci.org/ElliotVilhelm/IZII)
## Overview
IZII is a Python Chess Engine

Decisions are made using the minimax search algorithm with alpha-beta pruning to optimize search time. The engine is compatible with xboard or any other GUI using xboard/winboard protocol.

![chess gif](/images/chess.gif)
## Execution
To run IZII, download all files to your local system. You also must have [xboard](https://www.gnu.org/software/xboard/) or any other GUI with xboard protocol compatibility.
* For OSX users, brew supposrts xboard so simply 'brew install xboard'

To play the engine, cd into the source directory and run:
```python3
xboard -cp -fcp "python3 engine/xboard.py"
```
Furthermore, to watch IZII play itself you can run,
```python3
xboard -cp -fcp "python3 xboard.py" -scp "python3 engine/xboard.py"
```
then press CTRL-t on the xboard GUI to run a two machine game.

There is a script included to run this command
```
./scripts/run.sh
```

## Development
I wrote IZII on my free time as a means to improve my python and because I love chess! To implement IZII I used a 120 square chess board as used by Cray-1, one of the first chess playing computers.

![120sqboard](/images/cray.png?raw=true "120 square board") ![120sqboard](/images/120sqboard.png?raw=true "120 square board")

IZII makes its decisions in two key steps
1. Move Generation -> Pseudo legal moves filtered to legal moves
2. Move Search -> Using a board evaluation function IZII runs minimax search with Alpha-Beta pruning to discover the optimal move

IZII provides two key functions for playing chess:
get_all_moves_at_state -> inputs: state | outputs: all possible moves
run_move_at_state -> inputs: state, move | outputs: next state

As noted above, IZII works by first generating a moveset of all possible pseudo legal moves. This would include moves which would put the king in check. Then IZII prunes this moveset by checking for all cases and produces a set of legal moves. A minimax search is performed on the given board state generating a game tree at which all possible moves are explored to a modular set depth.



Enjoy!
