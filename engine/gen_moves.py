from engine.check_castle import check_wc_k, check_wc_q, check_bc_k, check_bc_q, can_castle
from engine.check_detection import white_in_check, black_in_check
from engine.constants import *
from engine.move import move_at_state


# Get Moves
def get_all_moves_at_state(state):
    legal = get_legal_moves(state, gen_pseudo_moves(state))
    return legal


def get_legal_moves(state, pseudo_moves):
    legal_moves = []
    in_check = False
    turn = state[TURN_INDEX]
    for move in pseudo_moves:
        from_sq = move[0]
        to_sq = move[1]
        # WK Castle
        if move == [E1, G1]:
            move_at_state(state, (E1, G1))  # move king
            s2 = move_at_state(state, (H1, F1))  # move castle
        # WQ Castle
        elif move == [E1, C1]:
            move_at_state(state, (E1, C1))  # move king
            s2 = move_at_state(state, (A1, D1))  # move castle
        # BK Castle
        elif move == [E8, G8]:
            move_at_state(state, (E8, G8))  # move king
            s2 = move_at_state(state, (H8, F8))  # move castle
        # BQ Castle
        elif move == [E8, C8]:
            move_at_state(state, (E8, C8))  # move king
            s2 = move_at_state(state, (A8, D8))  # move castle
        # Non Castle Move
        else:
            s2 = move_at_state(state, (from_sq, to_sq))

        # Check if I am in check after making the move, if so do not append move to legal moves list
        if turn == WHITE:
            in_check = white_in_check(s2[BOARD_INDEX], s2[WK_SQ_INDEX])
        elif turn == BLACK:
            in_check = black_in_check(s2[BOARD_INDEX], s2[BK_SQ_INDEX])
        if in_check is False:
            legal_moves.append(move)
    return legal_moves


"""
 _ __   __ ___      ___ __  ___
| '_ \ / _` \ \ /\ / | '_ \/ __|
| |_) | (_| |\ V  V /| | | \__ \
| .__/ \__,_| \_/\_/ |_| |_|___/
|_|

"""


def get_black_pawn_moves2(board, en_passant_square, tile_n):
    result = []
    # en_passant_square = self.current_state[2]
    if en_passant_square != -1:
        if tile_n == en_passant_square + NORTH_EAST or tile_n == en_passant_square + NORTH_WEST:
            result.append([tile_n, en_passant_square])
    # forward
    # initial move
    if tile_n <= RANK7:  # first row
        if board[tile_n + SOUTH] == "o":
            result.append([tile_n, tile_n + SOUTH])
            if board[tile_n + (SOUTH * 2)] == "o":
                result.append([tile_n, tile_n + (SOUTH * 2)])
    else:
        if board[tile_n + SOUTH] == "o":
            result.append([tile_n, tile_n + SOUTH])
    ###########
    # attack
    #############
    if board[tile_n + SOUTH_EAST] in white_pieces:  # attack left only black pawn only
        result.append([tile_n, tile_n + SOUTH_EAST])
    if board[tile_n + SOUTH_WEST] in white_pieces:  # attack right only black pawn only
        result.append([tile_n, tile_n + SOUTH_WEST])
    return result


def get_white_pawn_moves2(board, en_passant_square, tile_n):
    result = []
    # en_passant_square = self.current_state[2]
    # forward
    # initial move
    if en_passant_square != -1:
        if tile_n == en_passant_square + SOUTH_WEST or tile_n == en_passant_square + SOUTH_EAST:
            result.append([tile_n, en_passant_square])
    if tile_n >= RANK2:  # first row
        if board[tile_n + NORTH] == "o":
            result.append([tile_n, tile_n + NORTH])
            if board[tile_n + (2 * NORTH)] == "o":
                result.append([tile_n, tile_n + (2 * NORTH)])
    else:
        if board[tile_n + NORTH] == "o":
            result.append([tile_n, tile_n + NORTH])
    ###########
    # attack
    #############
    if board[tile_n + NORTH_WEST] in black_pieces:  # attack left only black pawn only
        result.append([tile_n, tile_n + NORTH_WEST])
    if board[tile_n + NORTH_EAST] in black_pieces:  # attack right only black pawn only
        result.append([tile_n, tile_n + NORTH_EAST])
    return result


"""
| | _(_)_ __   __ _ ___
| |/ | | '_ \ / _` / __|
|   <| | | | | (_| \__ \
|_|\_|_|_| |_|\__, |___/
              |___/
"""


def get_king_moves(board, tile_n, color):
    result = []
    opponent_pieces = black_pieces if color == WHITE else white_pieces
    valid_squares = opponent_pieces + 'o'
    for move in KING_MOVES:
        to_sq = board[tile_n + move]
        if to_sq in valid_squares:
            result.append([tile_n, tile_n + move])
    return result


"""
 _          _       _     _
| | ___ __ (_) __ _| |__ | |_ ___
| |/ | '_ \| |/ _` | '_ \| __/ __|
|   <| | | | | (_| | | | | |_\__ \
|_|\_|_| |_|_|\__, |_| |_|\__|___/
              |___/
"""

def get_white_knight_moves2(board, tile_n):
    result = []
    for move in KNIGHT_MOVES:
        if board[tile_n + move] == 'o' or board[tile_n + move] in black_pieces:
            result.append([tile_n, tile_n + move])
    return result


def get_black_knight_moves2(board, tile_n):
    result = []
    for move in KNIGHT_MOVES:
        if board[tile_n + move] == 'o' or board[tile_n + move] in white_pieces:
            result.append([tile_n, tile_n + move])
    return result

def swap_turn(turn):
    if turn is WHITE:
        return BLACK
    return WHITE


def gen_pseudo_moves(state):
    moves = []
    turn = state[TURN_INDEX]
    b = state[BOARD_INDEX]
    for sq_index in range(21, 99):
        piece_at_index = b[sq_index]
        if turn is WHITE and piece_at_index in BLACK_PIECES:
            continue
        elif turn is BLACK and piece_at_index in WHITE_PIECES:
            continue
        elif piece_at_index in (OUT_OF_BOUND, EMPTY):
            continue
        elif piece_at_index is 'P':
            moves += get_white_pawn_moves2(b, state[EN_PAS_INDEX], sq_index)
        elif piece_at_index is 'p':
            moves += get_black_pawn_moves2(b, state[EN_PAS_INDEX], sq_index)
        elif piece_at_index is 'n':
            moves += get_black_knight_moves2(b, sq_index)
        elif piece_at_index is 'N':
            moves += get_white_knight_moves2(b, sq_index)
        elif piece_at_index is 'K':
            moves += get_king_moves(b, sq_index, WHITE)
        elif piece_at_index is 'k':
            moves += get_king_moves(b, sq_index, BLACK)
        else:
            piece_moves = PIECE_MOVES[piece_at_index]
            for offset in piece_moves:
                # Sliders
                sq_slider_index = sq_index
                while True:
                    sq_slider_index += offset
                    # Hit border
                    if b[sq_slider_index] == OUT_OF_BOUND:
                        break
                    # Hit myself
                    elif turn is WHITE and b[sq_slider_index] in WHITE_PIECES or b[sq_slider_index] == 'k':
                        break
                    elif turn is BLACK and b[sq_slider_index] in BLACK_PIECES or b[sq_slider_index] == 'K':
                        break
                    elif b[sq_slider_index] is OUT_OF_BOUND:
                        break
                    moves.append([sq_index, sq_slider_index])
                    # Attack, break because we are done searching!
                    if turn is WHITE and b[sq_slider_index] in BLACK_PIECES:
                        break
                    elif turn is BLACK and b[sq_slider_index] in WHITE_PIECES:
                        break
    # Castling
    if state[TURN_INDEX] == WHITE:
        if check_wc_k(state):  # if im not in check and i have not fucked up my castle perm add the move
            state[C_PERM_INDEX][WKC_INDEX] = 1
            moves.append([E1, G1])
        if check_wc_q(state):
            state[C_PERM_INDEX][WQC_INDEX] = 1
            moves.append([E1, C1])
    elif state[TURN_INDEX] == BLACK:
        if check_bc_k(state):
            state[C_PERM_INDEX][BKC_INDEX] = 1
            moves.append([E8, G8])
        if check_bc_q(state):
            state[C_PERM_INDEX][BQC_INDEX] = 1
            moves.append([E8, C8])
    return moves

