from engine.constants import *


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

    if state[EN_PAS_INDEX] == to_tile_n and board[from_tile_n] == 'P':
        if abs(from_tile_n - to_tile_n) == 11 or abs(from_tile_n - to_tile_n) == 9:
            board[to_tile_n + SOUTH] = 'o'
    elif state[EN_PAS_INDEX] == to_tile_n and board[from_tile_n] == 'p':
        if abs(from_tile_n - to_tile_n) == 11 or abs(from_tile_n - to_tile_n) == 9:
            board[to_tile_n + NORTH] = 'o'


    ### En Passant case
    en_pass_sq = -1
    if board[from_tile_n] == 'P':
        if from_tile_n >= RANK2:
            if abs(to_tile_n - from_tile_n) == 20:
                en_pass_sq = from_tile_n + NORTH
        # promote
        if board[to_tile_n + NORTH] == 'x':
            board[from_tile_n] = 'Q'
    elif board[from_tile_n] == 'p':
        # if from_tile_n >= RANK2:
        if from_tile_n <= RANK7:
            if abs(to_tile_n - from_tile_n) == 20:
                en_pass_sq = from_tile_n + SOUTH
        # promote
        if board[to_tile_n + SOUTH] == 'x':
            board[from_tile_n] = 'q'

    ### King move case
    elif board[from_tile_n] == 'K':

        white_king_sq = to_tile_n
        castle_perm[WKC_INDEX] = CASTLE_VOIDED
        castle_perm[WQC_INDEX] = CASTLE_VOIDED
    elif board[from_tile_n] == 'k':
        black_king_sq = to_tile_n
        castle_perm[BKC_INDEX] = CASTLE_VOIDED
        castle_perm[BQC_INDEX] = CASTLE_VOIDED
    elif board[from_tile_n] == 'R':
        if from_tile_n == H1:  # king side
            castle_perm[WKC_INDEX] = CASTLE_VOIDED
        elif from_tile_n == A1:
            castle_perm[WQC_INDEX] = CASTLE_VOIDED
    elif board[from_tile_n] == 'r':
        if from_tile_n == H8:  # king side
            castle_perm[BKC_INDEX] = CASTLE_VOIDED
        elif from_tile_n == A8:
            castle_perm[BQC_INDEX] = CASTLE_VOIDED

    # Check if attacking black king side rook
    if to_tile_n == A1:
        castle_perm[WQC_INDEX] = CASTLE_VOIDED
    elif to_tile_n == H1:
        castle_perm[WKC_INDEX] = CASTLE_VOIDED
    elif to_tile_n == A8:
        castle_perm[BQC_INDEX] = CASTLE_VOIDED
    elif to_tile_n == H8:
        castle_perm[BKC_INDEX] = CASTLE_VOIDED

    if from_tile_n == E1 and to_tile_n == G1 and board[from_tile_n] == 'K':  # and castle_perm[0] == 1:
        board[E1] = "o"
        board[F1] = 'R'
        board[G1] = 'K'
        white_king_sq = G1
        board[H1] = 'o'
        castle_perm[WKC_INDEX] = CASTLED
        castle_perm[WQC_INDEX] = CASTLED

    elif from_tile_n == E1 and to_tile_n == C1 and board[from_tile_n] == 'K':  # queen side castle
        board[A1] = "o"
        board[B1] = 'o'
        board[C1] = 'K'
        white_king_sq = C1
        board[D1] = 'R'
        board[E1] = 'o'
        castle_perm[WKC_INDEX] = CASTLED
        castle_perm[WQC_INDEX] = CASTLED
    elif from_tile_n == E8 and to_tile_n == G8 and board[from_tile_n] == 'k':  # king side castle
        board[E8] = "o"
        board[F8] = 'r'
        board[G8] = 'k'
        black_king_sq = G8
        board[H8] = 'o'
        castle_perm[BKC_INDEX] = CASTLED
        castle_perm[BQC_INDEX] = CASTLED
    elif from_tile_n == E8 and to_tile_n == C8 and board[from_tile_n] == 'k':  # queen side castle
        board[A8] = "o"
        board[B8] = 'o'
        board[C8] = 'k'
        black_king_sq = C8
        board[D8] = 'r'
        board[E8] = 'o'
        castle_perm[BKC_INDEX] = CASTLED
        castle_perm[BQC_INDEX] = CASTLED
    else:
        board[to_tile_n] = board[from_tile_n]
        board[from_tile_n] = "o"

    # Change Turns
    if turn == WHITE:
        turn = BLACK
    else:
        turn = WHITE
    # print(board[to_tile_n])
    return [board, turn, en_pass_sq, half_move, full_move, castle_perm, white_king_sq, black_king_sq]

