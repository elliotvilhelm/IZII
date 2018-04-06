from constants import *


def run_move_at_state(state, move):
    return_state = move_at_state(state, move)
    return return_state


def move_at_state(state, move):
    board = list(state[BOARD_INDEX])
    turn = state[TURN_INDEX]
    en_pass_sq = state[EN_PAS_INDEX]
    half_move = state[HALF_MOVE_INDEX]
    full_move = state[FULL_MOVE_INDEX]
    castle_perm = list(state[C_PERM_INDEX])
    white_king_sq = state[WK_SQ_INDEX]
    black_king_sq = state[BK_SQ_INDEX]
    from_tile_n = move[0]
    to_tile_n = move[1]

    ### En Passant case
    en_pass_sq = -1
    if board[from_tile_n] == 'P':
        if from_tile_n >= 81:
            if abs(to_tile_n - from_tile_n) == 20:
                en_pass_sq = from_tile_n - 10
        # promote
        if board[to_tile_n - 10] == 'x':
            board[from_tile_n] = 'Q'
    elif board[from_tile_n] == 'p':
        if from_tile_n >= 38:
            if abs(to_tile_n - from_tile_n) == 20:
                en_pass_sq = from_tile_n + 10
        # promote
        if board[to_tile_n + 10] == 'x':
            board[from_tile_n] = 'q'

    ### King move case
    elif board[from_tile_n] == 'K':

        white_king_sq = to_tile_n
        castle_perm[WKC_INDEX] = -1
        castle_perm[WQC_INDEX] = -1
    elif board[from_tile_n] == 'k':
        black_king_sq = to_tile_n
        castle_perm[BKC_INDEX] = -1
        castle_perm[BQC_INDEX] = -1
    elif board[from_tile_n] == 'R':
        if from_tile_n == H1:  # king side
            castle_perm[WKC_INDEX] = -1
        elif from_tile_n == A1:
            castle_perm[WQC_INDEX] = -1
    elif board[from_tile_n] == 'r':
        if from_tile_n == H8:  # king side
            castle_perm[BKC_INDEX] = -1
        elif from_tile_n == A8:
            castle_perm[BQC_INDEX] = -1

    # Check if attacking black king side rook
    if to_tile_n == A1:
        castle_perm[WQC_INDEX] = -1
    elif to_tile_n == H1:
        castle_perm[WKC_INDEX] = -1
    elif to_tile_n == A8:
        castle_perm[BQC_INDEX] = -1
    elif to_tile_n == H8:
        castle_perm[BKC_INDEX] = -1

    if from_tile_n == 95 and to_tile_n == 97 and board[from_tile_n] == 'K':  # and castle_perm[0] == 1:
        board[95] = "o"
        board[96] = 'R'
        board[97] = 'K'
        white_king_sq = 97
        board[98] = 'o'
        castle_perm[0] = 2
        castle_perm[1] = 2

    elif from_tile_n == 95 and to_tile_n == 93 and board[from_tile_n] == 'K':  # queen side castle
        board[91] = "o"
        board[92] = 'o'
        board[93] = 'K'
        white_king_sq = 93
        board[94] = 'R'
        board[95] = 'o'
        castle_perm[0] = 2
        castle_perm[1] = 2
    elif from_tile_n == 25 and to_tile_n == 27 and board[from_tile_n] == 'k':  # king side castle
        board[25] = "o"
        board[26] = 'r'
        board[27] = 'k'
        black_king_sq = 27
        board[28] = 'o'
        castle_perm[2] = 2
        castle_perm[3] = 2
    elif from_tile_n == 25 and to_tile_n == 23 and board[from_tile_n] == 'k':  # queen side castle
        board[21] = "o"
        board[22] = 'o'
        board[23] = 'k'
        black_king_sq = 23
        board[24] = 'r'
        board[25] = 'o'
        castle_perm[2] = 2
        castle_perm[3] = 2
    else:
        board[to_tile_n] = board[from_tile_n]
        board[from_tile_n] = "o"

    # Change Turns
    if turn == 0:
        turn = 1
    else:
        turn = 0
    # print(board[to_tile_n])
    return board, turn, en_pass_sq, half_move, full_move, castle_perm, white_king_sq, black_king_sq

