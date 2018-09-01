from engine.check_castle import check_wc_k, check_wc_q, check_bc_k, check_bc_q
from engine.check_detection import white_in_check, black_in_check
from engine.constants import *
from engine.move import move_at_state


# Get Moves
def get_all_moves_at_state(state):
    # psuedo = get_pseudo_moves_beta(state)
    # psuedo = gen_pseudo_moves_v3(state)
    legal = get_legal_moves_beta(state, gen_pseudo_moves_v3(state))
    return legal


def get_legal_moves_beta(state, pseudo_moves):
    # take move
    # check if in check
    # valid/invalid move
    # undo move
    legal_moves = []
    in_check = False
    turn = state[TURN_INDEX]
    # if state[1] == 0:
    # print("pseudo moves: ", pseudo_moves)
    for i in range(len(pseudo_moves)):
        from_sq = pseudo_moves[i][0]
        to_sq = pseudo_moves[i][1]
        # WK Castle
        if pseudo_moves[i] == [E1, G1]:
            move_at_state(state, (E1, G1))  # move king
            s2 = move_at_state(state, (H1, F1))  # move castle
        # WQ Castle
        elif pseudo_moves[i] == [E1, C1]:
            move_at_state(state, (E1, C1))  # move king
            s2 = move_at_state(state, (A1, D1))  # move castle
        # BK Castle
        elif pseudo_moves[i] == [E8, G8]:
            move_at_state(state, (E8, G8))  # move king
            s2 = move_at_state(state, (H8, F8))  # move castle
        # BQ Castle
        elif pseudo_moves[i] == [E8, C8]:
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
            legal_moves.append(pseudo_moves[i])
    return legal_moves


"""
 _ __   __ ___      ___ __  ___
| '_ \ / _` \ \ /\ / | '_ \/ __|
| |_) | (_| |\ V  V /| | | \__ \
| .__/ \__,_| \_/\_/ |_| |_|___/
|_|

"""

def get_white_pawn_moves(board, en_passant_square, tile_n):
    result = []
    # en_passant_square = self.current_state[2]
    # forward
    # initial move
    if en_passant_square != -1:
        if tile_n == en_passant_square + SOUTH_WEST or tile_n == en_passant_square + SOUTH_EAST:
            result.append(en_passant_square)
    if tile_n >= RANK2:  # first row
        if board[tile_n + NORTH] == "o":
            result.append(tile_n + NORTH)
            if board[tile_n + (2 * NORTH)] == "o":
                result.append(tile_n + (2 * NORTH))
    else:
        if board[tile_n + NORTH] == "o":
            result.append(tile_n + NORTH)
    ###########
    # attack
    #############
    if board[tile_n + NORTH_WEST] in black_pieces:  # attack left only black pawn only
        result.append(tile_n + NORTH_WEST)
    if board[tile_n + NORTH_EAST] in black_pieces:  # attack right only black pawn only
        result.append(tile_n + NORTH_EAST)
    return result


def get_black_pawn_moves(board, en_passant_square, tile_n):
    result = []
    # en_passant_square = self.current_state[2]
    if en_passant_square != -1:
        if tile_n == en_passant_square + NORTH_EAST or tile_n == en_passant_square + NORTH_WEST:
            result.append(en_passant_square)
    # forward
    # initial move
    if tile_n <= RANK7:  # first row
        if board[tile_n + SOUTH] == "o":
            result.append(tile_n + SOUTH)
            if board[tile_n + (SOUTH * 2)] == "o":
                result.append(tile_n + (SOUTH * 2))
    else:
        if board[tile_n + SOUTH] == "o":
            result.append(tile_n + SOUTH)
    ###########
    # attack
    #############
    if board[tile_n + SOUTH_EAST] in white_pieces:  # attack left only black pawn only
        result.append(tile_n + SOUTH_EAST)
    if board[tile_n + SOUTH_WEST] in white_pieces:  # attack right only black pawn only
        result.append(tile_n + SOUTH_WEST)
    return result

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


def get_white_king_moves(board, tile_n):
    result = []
    down = tile_n + SOUTH
    up = tile_n - 10
    right = tile_n - 1
    left = tile_n + 1
    up_left = tile_n - 11
    up_right = tile_n - 9
    down_left = tile_n + 9
    down_right = tile_n + 11

    # passive moves
    if board[down] == 'o':
        result.append(down)
    if board[up] == 'o':
        result.append(up)
    if board[left] == 'o':
        result.append(left)
    if board[right] == 'o':
        result.append(right)
    if board[up_right] == 'o':
        result.append(up_right)
    if board[down_right] == 'o':
        result.append(down_right)
    if board[up_left] == 'o':
        result.append(up_left)
    if board[down_left] == 'o':
        result.append(down_left)

    # attack moves
    if board[down] in black_pieces:
        result.append(down)
    if board[up] in black_pieces:
        result.append(up)
    if board[left] in black_pieces:
        result.append(left)
    if board[right] in black_pieces:
        result.append(right)
    if board[up_right] in black_pieces:
        result.append(up_right)
    if board[down_right] in black_pieces:
        result.append(down_right)
    if board[up_left] in black_pieces:
        result.append(up_left)
    if board[down_left] in black_pieces:
        result.append(down_left)

    return result


def get_black_king_moves(board, tile_n):
    result = []
    up = tile_n + 10
    down = tile_n - 10
    left = tile_n - 1
    right = tile_n + 1
    down_right = tile_n - 11
    down_left = tile_n - 9
    up_right = tile_n + 9
    up_left = tile_n + 11

    # passive moves
    if board[down] == 'o':
        result.append(down)
    if board[up] == 'o':
        result.append(up)
    if board[left] == 'o':
        result.append(left)
    if board[right] == 'o':
        result.append(right)
    if board[up_right] == 'o':
        result.append(up_right)
    if board[down_right] == 'o':
        result.append(down_right)
    if board[up_left] == 'o':
        result.append(up_left)
    if board[down_left] == 'o':
        result.append(down_left)

    # attack moves
    if board[down] in white_pieces:
        result.append(down)
    if board[up] in white_pieces:
        result.append(up)
    if board[left] in white_pieces:
        result.append(left)
    if board[right] in white_pieces:
        result.append(right)
    if board[up_right] in white_pieces:
        result.append(up_right)
    if board[down_right] in white_pieces:
        result.append(down_right)
    if board[up_left] in white_pieces:
        result.append(up_left)
    if board[down_left] in white_pieces:
        result.append(down_left)

    return result


def get_white_king_moves2(board, tile_n):
    result = []
    down = tile_n + SOUTH
    up = tile_n - 10
    right = tile_n - 1
    left = tile_n + 1
    up_left = tile_n - 11
    up_right = tile_n - 9
    down_left = tile_n + 9
    down_right = tile_n + 11

    # passive moves
    if board[down] == 'o':
        result.append([tile_n, down])
    if board[up] == 'o':
        result.append([tile_n, up])
    if board[left] == 'o':
        result.append([tile_n, left])
    if board[right] == 'o':
        result.append([tile_n, right])
    if board[up_right] == 'o':
        result.append([tile_n, up_right])
    if board[down_right] == 'o':
        result.append([tile_n, down_right])
    if board[up_left] == 'o':
        result.append([tile_n, up_left])
    if board[down_left] == 'o':
        result.append([tile_n, down_left])

    # attack moves
    if board[down] in black_pieces:
        result.append([tile_n, down])
    if board[up] in black_pieces:
        result.append([tile_n, up])
    if board[left] in black_pieces:
        result.append([tile_n, left])
    if board[right] in black_pieces:
        result.append([tile_n, right])
    if board[up_right] in black_pieces:
        result.append([tile_n, up_right])
    if board[down_right] in black_pieces:
        result.append([tile_n, down_right])
    if board[up_left] in black_pieces:
        result.append([tile_n, up_left])
    if board[down_left] in black_pieces:
        result.append([tile_n, down_left])

    return result


def get_black_king_moves2(board, tile_n):
    result = []
    up = tile_n + 10
    down = tile_n - 10
    left = tile_n - 1
    right = tile_n + 1
    down_right = tile_n - 11
    down_left = tile_n - 9
    up_right = tile_n + 9
    up_left = tile_n + 11

    # passive moves
    if board[down] == 'o':
        result.append([tile_n, down])
    if board[up] == 'o':
        result.append([tile_n, up])
    if board[left] == 'o':
        result.append([tile_n, left])
    if board[right] == 'o':
        result.append([tile_n, right])
    if board[up_right] == 'o':
        result.append([tile_n, up_right])
    if board[down_right] == 'o':
        result.append([tile_n, down_right])
    if board[up_left] == 'o':
        result.append([tile_n, up_left])
    if board[down_left] == 'o':
        result.append([tile_n, down_left])

    # attack moves
    if board[down] in white_pieces:
        result.append([tile_n, down])
    if board[up] in white_pieces:
        result.append([tile_n, up])
    if board[left] in white_pieces:
        result.append([tile_n, left])
    if board[right] in white_pieces:
        result.append([tile_n, right])
    if board[up_right] in white_pieces:
        result.append([tile_n, up_right])
    if board[down_right] in white_pieces:
        result.append([tile_n, down_right])
    if board[up_left] in white_pieces:
        result.append([tile_n, up_left])
    if board[down_left] in white_pieces:
        result.append([tile_n, down_left])

    return result


"""
 _          _       _     _
| | ___ __ (_) __ _| |__ | |_ ___
| |/ | '_ \| |/ _` | '_ \| __/ __|
|   <| | | | | (_| | | | | |_\__ \
|_|\_|_| |_|_|\__, |_| |_|\__|___/
              |___/
"""


def get_white_knight_moves(board, tile_n):
    result = []
    for i in range(len(KNIGHT_MOVES)):
        if board[tile_n + KNIGHT_MOVES[i]] == 'o' or board[tile_n + KNIGHT_MOVES[i]] in black_pieces:
            result.append(tile_n + KNIGHT_MOVES[i])
    return result


def get_black_knight_moves(board, tile_n):
    result = []
    for i in range(len(KNIGHT_MOVES)):
        if board[tile_n + KNIGHT_MOVES[i]] == 'o' or board[tile_n + KNIGHT_MOVES[i]] in white_pieces:
            result.append(tile_n + KNIGHT_MOVES[i])
    return result


def get_white_knight_moves2(board, tile_n):
    result = []
    for i in range(len(KNIGHT_MOVES)):
        if board[tile_n + KNIGHT_MOVES[i]] == 'o' or board[tile_n + KNIGHT_MOVES[i]] in black_pieces:
            result.append([tile_n, tile_n + KNIGHT_MOVES[i]])
    return result


def get_black_knight_moves2(board, tile_n):
    result = []
    for i in range(len(KNIGHT_MOVES)):
        if board[tile_n + KNIGHT_MOVES[i]] == 'o' or board[tile_n + KNIGHT_MOVES[i]] in white_pieces:
            result.append([tile_n, tile_n + KNIGHT_MOVES[i]])
    return result


def swap_turn(turn):
    if turn is WHITE:
        return BLACK
    return WHITE


def gen_pseudo_moves_v3(state):
    moves = []
    turn = state[TURN_INDEX]
    b = state[BOARD_INDEX]
    for sq_index in range(21, 99):
        piece_at_index = b[sq_index]
        if turn is WHITE and piece_at_index in BLACK_PIECES:
            continue
        elif turn is BLACK and piece_at_index in WHITE_PIECES:
            continue
        elif piece_at_index is OUT_OF_BOUND:
            continue
        elif piece_at_index is EMPTY:
            continue

        # PAWNS
        if piece_at_index is 'P':
            moves += get_white_pawn_moves2(b, state[EN_PAS_INDEX], sq_index)
            continue
        elif piece_at_index is 'p':
            moves += get_black_pawn_moves2(b, state[EN_PAS_INDEX], sq_index)
            continue

        elif piece_at_index is 'n':
            moves += get_black_knight_moves2(b, sq_index)
            continue
        elif piece_at_index is 'N':
            moves += get_white_knight_moves2(b, sq_index)
            continue
        elif piece_at_index is 'K':
            moves += get_white_king_moves2(b, sq_index)
            continue
        elif piece_at_index is 'k':
            moves += get_black_king_moves2(b, sq_index)
            continue
        else:
            piece_moves = PIECE_MOVES[piece_at_index]
            for offset in piece_moves:
                # Sliders
                sq_slider_index = sq_index
                while True:
                    sq_slider_index += offset

                    # Hit myself
                    if turn is WHITE and b[sq_slider_index] in WHITE_PIECES or b[sq_slider_index] == 'k':
                        break
                    elif turn is BLACK and b[sq_slider_index] in BLACK_PIECES or b[sq_slider_index] == 'K':
                        break
                    elif b[sq_slider_index] is OUT_OF_BOUND:
                        break

                    moves.append([sq_index, sq_slider_index])

                    # Attack!
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
    if state[TURN_INDEX] == BLACK:
        if check_bc_k(state):
            state[C_PERM_INDEX][BKC_INDEX] = 1
            moves.append([E8, G8])
        if check_bc_q(state):
            state[C_PERM_INDEX][BQC_INDEX] = 1
            moves.append([E8, C8])


    return moves

