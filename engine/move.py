from engine.constants import BOARD_INDEX, C_PERM_INDEX, WK_SQ_INDEX, BK_SQ_INDEX, EN_PAS_INDEX, NORTH, SOUTH, \
    RANK2, RANK7, WKC_INDEX, WQC_INDEX, BKC_INDEX, BQC_INDEX, CASTLE_VOIDED, CASTLED, A1, A8, E1, E8, C1, C8, G1, \
    G8, H1, H8, WHITE, BLACK, HALF_MOVE_INDEX, FULL_MOVE_INDEX, TURN_INDEX, B8, B1, D1, D8, F1, F8
from engine.utils import update
from engine import board_hash
import logging

def move_at_state(state, move, live_move=False):
    board = state[BOARD_INDEX]
    castle_perm = state[C_PERM_INDEX]
    white_king_sq = state[WK_SQ_INDEX]
    black_king_sq = state[BK_SQ_INDEX]
    from_tile_n = move[0]
    to_tile_n = move[1]

    if state[EN_PAS_INDEX] == to_tile_n and board[from_tile_n] == 'P':
        if abs(from_tile_n - to_tile_n) == 11 or abs(from_tile_n - to_tile_n) == 9:
            board = update(board, to_tile_n + SOUTH, 'o')
    elif state[EN_PAS_INDEX] == to_tile_n and board[from_tile_n] == 'p':
        if abs(from_tile_n - to_tile_n) == 11 or abs(from_tile_n - to_tile_n) == 9:
            board = update(board, to_tile_n + NORTH, 'o')

    en_pass_sq = -1
    if board[from_tile_n] == 'P':
        if from_tile_n >= RANK2:
            if abs(to_tile_n - from_tile_n) == 20:
                en_pass_sq = from_tile_n + NORTH
        if board[to_tile_n + NORTH] == 'x':
            board = update(board, from_tile_n, 'Q')
    elif board[from_tile_n] == 'p':
        if from_tile_n <= RANK7:
            if abs(to_tile_n - from_tile_n) == 20:
                en_pass_sq = from_tile_n + SOUTH
        if board[to_tile_n + SOUTH] == 'x':
            board = update(board, from_tile_n, 'q')

    # King move case
    elif board[from_tile_n] == 'K':
        white_king_sq = to_tile_n
        castle_perm = update(castle_perm, WKC_INDEX, CASTLE_VOIDED)
        castle_perm = update(castle_perm, WQC_INDEX, CASTLE_VOIDED)
    elif board[from_tile_n] == 'k':
        black_king_sq = to_tile_n
        castle_perm = update(castle_perm, BQC_INDEX, CASTLE_VOIDED)
        castle_perm = update(castle_perm, BQC_INDEX, CASTLE_VOIDED)
    elif board[from_tile_n] == 'R':
        if from_tile_n == H1:  # king side
            castle_perm = update(castle_perm, WKC_INDEX, CASTLE_VOIDED)
        elif from_tile_n == A1:
            castle_perm = update(castle_perm, WQC_INDEX, CASTLE_VOIDED)
    elif board[from_tile_n] == 'r':
        if from_tile_n == H8:  # king side
            castle_perm = update(castle_perm, BKC_INDEX, CASTLE_VOIDED)
        elif from_tile_n == A8:
            castle_perm = update(castle_perm, BQC_INDEX, CASTLE_VOIDED)

    # Check if attacking black king side rook
    if to_tile_n == A1:
        castle_perm = update(castle_perm, WQC_INDEX, CASTLE_VOIDED)
    elif to_tile_n == H1:
        castle_perm = update(castle_perm, WKC_INDEX, CASTLE_VOIDED)
    elif to_tile_n == A8:
        castle_perm = update(castle_perm, BQC_INDEX, CASTLE_VOIDED)
    elif to_tile_n == H8:
        castle_perm = update(castle_perm, BKC_INDEX, CASTLE_VOIDED)

    if from_tile_n == E1 and to_tile_n == G1 and board[from_tile_n] == 'K':  # and castle_perm[0] == 1:
        board = update(board, E1, 'o')
        board = update(board, F1, 'R')
        board = update(board, G1, 'K')
        board = update(board, H1, 'o')
        white_king_sq = G1
        castle_perm = update(castle_perm, WKC_INDEX, CASTLED)
        castle_perm = update(castle_perm, WQC_INDEX, CASTLED)
    elif from_tile_n == E1 and to_tile_n == C1 and board[from_tile_n] == 'K':  # queen side castle
        board = update(board, A1, 'o')
        board = update(board, B1, 'o')
        board = update(board, C1, 'K')
        board = update(board, D1, 'R')
        board = update(board, E1, 'o')
        white_king_sq = C1
        castle_perm = update(castle_perm, WKC_INDEX, CASTLED)
        castle_perm = update(castle_perm, WQC_INDEX, CASTLED)
    elif from_tile_n == E8 and to_tile_n == G8 and board[from_tile_n] == 'k':  # king side castle
        board = update(board, E8, 'o')
        board = update(board, F8, 'r')
        board = update(board, G8, 'k')
        board = update(board, H8, 'o')
        black_king_sq = G8
        castle_perm = update(castle_perm, BKC_INDEX, CASTLED)
        castle_perm = update(castle_perm, BQC_INDEX, CASTLED)
    elif from_tile_n == E8 and to_tile_n == C8 and board[from_tile_n] == 'k':  # queen side castle
        board = update(board, A8, 'o')
        board = update(board, B8, 'o')
        board = update(board, C8, 'K')
        board = update(board, D8, 'R')
        board = update(board, E8, 'o')
        black_king_sq = C8
        castle_perm = update(castle_perm, BKC_INDEX, CASTLED)
        castle_perm = update(castle_perm, BQC_INDEX, CASTLED)
    else:
        if live_move:
            if board[to_tile_n] != 'o':
                logging.debug('cleared board hash!!!')
                print("cleared board hash", board[to_tile_n])
                board_hash = {}
        board = update(board, to_tile_n, board[from_tile_n])
        board = update(board, from_tile_n, 'o')
    # Change Turns
    turn = BLACK if state[TURN_INDEX] == WHITE else WHITE
    return [board, turn, en_pass_sq, state[HALF_MOVE_INDEX], state[FULL_MOVE_INDEX], castle_perm, white_king_sq, black_king_sq]
