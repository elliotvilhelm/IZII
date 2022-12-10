[![Build Status](https://travis-ci.org/ElliotVilhelm/IZII.svg?branch=master)](https://travis-ci.org/ElliotVilhelm/IZII)
## Overview
IZII is a Python Chess Engine

Decisions are made using the minimax search algorithm with alpha-beta pruning to optimize search time. The engine is compatible with xboard or any other GUI using xboard/winboard protocol.

IZII makes decisions in two key steps.
1. Move Generation
2. Search
IZII works by first generating a moveset of all possible pseudo legal moves.
This would include moves which would put the king in check. Then IZII prunes this moveset by checking
for all cases and produces a set of legal moves. A minimax search is performed on the given board state
generating a game tree at which all possible moves are explored to a modular set depth.
Enjoy!

![chess gif](images/chess.gif)
![chess tree](images/chess_tree.jpeg)

## Execution
IZII is packed with a script to run IZII on xboard
1. Be sure you have xboard installed `brew install xboard`
2. Clone the repository `git clone https://github.com/ElliotVilhelm/IZII.git`
3. Navigate to the directory `cd IZII`
4. Execute the script `./scripts/run.sh`

You can press `ctrl-t` on your keyboard and IZII will begin to play itself

## Test
```
pip3 install pytest
pytest
```

## Development
I wrote IZII on my free time as a means to improve my python and because I love chess!
To implement IZII I used a 120 square chess board as used by Cray-1, one of the first chess playing computers.

![120sqboard](/images/cray.png?raw=true "120 square board")
![120sqboard](/images/120sqboard.png?raw=true "120 square board")

IZII provides two key functions for playing chess:
`get_all_moves_at_state(state)`
outputs: all possible moves
`run_move_at_state(state, move)`
outputs: next state

