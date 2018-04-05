import positional_board_values
from constants import *
from utils import *
def evaluate_state(state):
    # P = 100
    # N = 320
    # B = 330
    # R = 500
    # Q = 900
    # K = 20000
    # print("mobility diff: ", white_move_count-black_move_count)
    count = {'K': 0, 'Q': 0, 'R': 0, 'B': 0, 'N': 0, 'P': 0, 'k': 0, 'q': 0, 'r': 0, 'b': 0, 'n': 0, 'p': 0}

    board = state[0][20:100]
    # print("board", board)
    # value = 0
    # white_castle = 0
    # black_castle = 0
    # if state[1] == 0 or state[1] == 1:
    # 	if state[5][0] == -1 or state[5][1] == -1:
    # 		value -= 1
    # 	if state[5][0] == 2 and state[5][1] == 2:
    # 		value += 10
    # if state[1] == 0:or i in board:
    white_pawn_pos = 0.0
    black_pawn_pos = 0.0
    white_knight_pos = 0.0
    black_knight_pos = 0.0

    white_bishop_pos = 0.0
    black_bishop_pos = 0.0

    white_rook_pos = 0.0
    black_rook_pos = 0.0

    white_queen_pos = 0.0
    black_queen_pos = 0.0
    for i in range(len(board)):
        if board[i] == 'x' or board[i] == 'o':
            pass
        else:
            count[board[i]] += 1
            safe_i = sq120_sq64(i + 20) - 1
            if board[i] == 'P':
                white_pawn_pos += positional_board_values.white_pawn_pos_table[safe_i]
            elif board[i] == 'p':
                black_pawn_pos += positional_board_values.black_pawn_pos_table[safe_i]
            elif board[i] == 'N':
                white_knight_pos += positional_board_values.white_knight_pos_table[safe_i]
            elif board[i] == 'n':
                black_knight_pos += positional_board_values.black_knight_pos_table[safe_i]
            elif board[i] == 'B':
                white_bishop_pos += positional_board_values.white_bishop_pos_table[safe_i]
            elif board[i] == 'b':
                black_bishop_pos += positional_board_values.black_bishop_pos_table[safe_i]
            elif board[i] == 'R':
                white_rook_pos += positional_board_values.white_rook_pos_table[safe_i]
            elif board[i] == 'r':
                black_rook_pos += positional_board_values.black_rook_pos_table[safe_i]
            elif board[i] == 'Q':
                white_queen_pos += positional_board_values.white_queen_pos_table[safe_i]
            elif board[i] == 'q':
                black_queen_pos += positional_board_values.black_queen_pos_table[safe_i]

                ###(2000.0 * (count['K'] - count['k'])) +
    value = ((900.0 * (count['Q'] - count['q'])) +
             (500.0 * (count['R'] - count['r'])) + (330.0 * (count['B'] - count['b'])) +
             (320.0 * (count['N'] - count['n'])) + (100.0 * (count['P'] - count['p']))) \
            + (0.1 * ((white_pawn_pos - black_pawn_pos) + (white_knight_pos - black_knight_pos) \
                      + (white_bishop_pos - black_bishop_pos) + (white_rook_pos - black_rook_pos) \
                      + (white_queen_pos - black_queen_pos)))

    # +(.1 * (white_move_count - black_move_count)))

    castle_mod = .25
    if state[C_PERM_INDEX][WKC_INDEX] == 2 or state[C_PERM_INDEX][WQC_INDEX] == 2:
        # print("white castle")
        value += 1 * castle_mod
    elif state[C_PERM_INDEX][WKC_INDEX] == -1 or state[C_PERM_INDEX][WQC_INDEX] == -1:
        value -= 1 * castle_mod

    if state[C_PERM_INDEX][BKC_INDEX] == 2 or state[C_PERM_INDEX][BQC_INDEX] == 2:
        # print("white castle")
        value -= 1 * castle_mod
    elif state[C_PERM_INDEX][BKC_INDEX] == -1 or state[C_PERM_INDEX][BQC_INDEX] == -1:
        value += 1 * castle_mod

    return value

