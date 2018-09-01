import sys
from move import move_at_state
from react_chess_to_IZII_state import react_chess_board_to_IZII_board
from search import best_move
from utils import print_board
from utils import int_sq120_sq64, sq64_to_RF

try:
    # State = {board, turn, en pass, half move, full move, castle perms, wk sq, bk sq]}
    # init_state = [init_board, 0, -1, 0, 1, [0, 0, 0, 0], init_board.index('K'), init_board.index('k')]
    if sys.argv[1] == 'undefined':
        print("args undefined (get_move.py)")
        exit()

    state = [0,0,0,0,0,0, 0, 0]

    state[0] = react_chess_board_to_IZII_board(sys.argv[1])
    state[1] = int(sys.argv[2])
    state[2] = int(sys.argv[3])
    state[3] = 0
    state[4] = 0
    castle_perms = sys.argv[6]
    state[5] = [int(castle_perms[0]), int(castle_perms[1]), int(castle_perms[2]), int(castle_perms[3])]  # for now
    state[6] = state[0].index('K')
    state[7] = state[0].index('k')


    move = best_move(state, 2)

    piece_at_from_sq = state[0][move[0]]
    source_sq_RF = list(sq64_to_RF(int_sq120_sq64()[move[0]]))
    source_sq_RF[0] = source_sq_RF[0].lower()
    destination_sq_RF = list(sq64_to_RF(int_sq120_sq64()[move[1]]))
    destination_sq_RF[0] = destination_sq_RF[0].lower()

    print(''.join(source_sq_RF))
    print(''.join(destination_sq_RF))

    # output = run_move_at_state(state, move)

    # output[0] = ''.join(output[0])
    # output[1] = str(output[1])
    # output[2] = str(output[2])
    # output[3] = str(output[3])
    # output[4] = str(output[4])
    # output[5][0] = str(output[5][0])
    # output[5][1] = str(output[5][1])
    # output[5][2] = str(output[5][2])
    # output[5][3] = str(output[5][3])
    # output[5] = ''.join(output[5])
    # output[6] = str(output[4])
    # output[7] = str(output[4])



    # print(output)
except Exception as e:
    print("except e", e)
    exit()



