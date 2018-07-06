import sys
from move import run_move_at_state
from react_chess_to_IZII_state import react_chess_board_to_IZII_board
from search import best_move
from utils import print_board
from utils import int_sq120_sq64, sq64_to_RF, RF_sq64, sq64_to_sq120
from gen_moves import get_all_moves_at_state

try:
    # State = {board, turn, en pass, half move, full move, castle perms, wk sq, bk sq]}
    # init_state = [init_board, 0, -1, 0, 1, [0, 0, 0, 0], init_board.index('K'), init_board.index('k')]
    if sys.argv[1] == 'undefined':
        exit()

    state = [0,0,0,0,0,0, 0, 0]

    state[0] = react_chess_board_to_IZII_board(sys.argv[1])
    state[1] = int(sys.argv[2])
    state[2] = int(sys.argv[3])
    state[3] = 0
    state[4] = 0
    state[5] = [0,0,0,0] # for now
    state[6] = state[0].index('K')
    state[7] = state[0].index('k')

    all_moves = get_all_moves_at_state(state)
    from_sq = sys.argv[7]
    to_sq = sys.argv[8]
    from_sq = sq64_to_sq120(RF_sq64(from_sq[0], from_sq[1]))
    to_sq = sq64_to_sq120(RF_sq64(to_sq[0], to_sq[1]))
    move = [from_sq, to_sq]

    if move in all_moves:
        print("true")
    else:
        print("false")

except:
     print("EXCEPTION")
     exit()


