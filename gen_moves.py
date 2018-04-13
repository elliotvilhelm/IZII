from check_castle import check_wc_k, check_wc_q, check_bc_k, check_bc_q
from check_detection import white_in_check, black_in_check
from constants import *
from move import run_move_at_state


# Get Moves
def get_all_moves_at_state(state):
    psuedo = get_pseudo_moves_beta(state)
    legal = get_legal_moves_beta(state, psuedo)
    return legal


def get_piece_moves(state, tile_n):
    board = state[BOARD_INDEX]
    en_pass_sq = state[EN_PAS_INDEX]
    result = []
    # print(tile_n, board[tile_n])
    if board[tile_n] == "P":
        result = get_white_pawn_moves(board, en_pass_sq, tile_n)
    elif board[tile_n] == "p":
        result = get_black_pawn_moves(board, en_pass_sq, tile_n)
    elif board[tile_n] == "K":
        result = get_white_king_moves(board, tile_n)
    elif board[tile_n] == "k":
        result = get_black_king_moves(board, tile_n)
    elif board[tile_n] == "R":
        result = get_white_rook_moves(board, tile_n)
    elif board[tile_n] == "r":
        result = get_black_rook_moves(board, tile_n)
    elif board[tile_n] == "B":
        result = get_white_bishop_moves(board, tile_n)
    elif board[tile_n] == "b":
        result = get_black_bishop_moves(board, tile_n)
    elif board[tile_n] == "N":
        result = get_white_knight_moves(board, tile_n)
    elif board[tile_n] == "n":
        result = get_black_knight_moves(board, tile_n)
    elif board[tile_n] == "Q":
        result = get_white_queen_moves(board, tile_n)
    elif board[tile_n] == "q":
        result = get_black_queen_moves(board, tile_n)
    return result


def get_pseudo_moves_beta(state):
    moves = []
    b = state[BOARD_INDEX]
    turn = state[TURN_INDEX]
    for i in range(len(b)):
        if turn == WHITE:
            if b[i] in all_white:
                piece_moves = get_piece_moves(state, i)
                for k in range(len(piece_moves)):
                    moves.append([i, piece_moves[k]])
                    # if len(piece_moves) > 0:
                    # 	moves.append([i, piece_moves])
        elif turn == BLACK:
            if b[i] in all_black:
                piece_moves = get_piece_moves(state, i)
                for k in range(len(piece_moves)):
                    moves.append([i, piece_moves[k]])
                    # if len(piece_moves) > 0:
                    # 	moves.append([i, piece_moves])

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
        move_set = pseudo_moves[i]
        from_sq = move_set[0]
        to_sq = move_set[1]
        # WK Castle
        if pseudo_moves[i] == [E1, G1]:
            s2 = run_move_at_state(state, (E1, G1))  # move king
            s2 = run_move_at_state(state, (H1, F1))  # move castle
        # WQ Castle
        elif pseudo_moves[i] == [E1, C1]:
            s2 = run_move_at_state(state, (E1, C1))  # move king
            s2 = run_move_at_state(state, (A1, D1))  # move castle
        # BK Castle
        elif pseudo_moves[i] == [E8, G8]:
            s2 = run_move_at_state(state, (E8, G8))  # move king
            s2 = run_move_at_state(state, (H8, F8))  # move castle
        # BQ Castle
        elif pseudo_moves[i] == [E8, C8]:
            s2 = run_move_at_state(state, (E8, C8))  # move king
            s2 = run_move_at_state(state, (A8, D8))  # move castle
        # Non Castle Move
        else:
            s2 = run_move_at_state(state, (from_sq, to_sq))

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


"""
                 _        
 _ __ ___   ___ | | _____ 
| '__/ _ \ / _ \| |/ / __|
| | | (_) | (_) |   <\__ \
|_|  \___/ \___/|_|\_|___/
                          
"""


def get_white_rook_moves(board, tile_n):
    result = []
    # UP
    i = tile_n
    while board[i] != 'x':
        i += NORTH
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in black_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in white_pieces or board[i] == "K" or board[i] == "k":
            break
    # DOWN
    i = tile_n
    while board[i] != 'x':
        i += SOUTH
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in black_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in white_pieces or board[i] == "K" or board[i] == "k":
            break

    # LEFT
    i = tile_n
    while board[i] != 'x':
        i += WEST
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in black_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in white_pieces or board[i] == "K" or board[i] == "k":
            break

    # RIGHT
    i = tile_n
    while board[i] != 'x':
        i += EAST
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in black_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in white_pieces or board[i] == "K" or board[i] == "k":
            break
    return result


def get_black_rook_moves(board, tile_n):
    result = []
    # UP
    i = tile_n
    while board[i] != 'x':
        i += SOUTH
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in white_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in black_pieces or board[i] == "k" or board[i] == "K":
            break
    # DOWN
    i = tile_n
    while board[i] != 'x':
        i += NORTH
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in white_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in black_pieces or board[i] == "k" or board[i] == "K":
            break

    # LEFT
    i = tile_n
    while board[i] != 'x':
        i += EAST
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in white_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in black_pieces or board[i] == "k" or board[i] == "K":
            break

    # RIGHT
    i = tile_n
    while board[i] != 'x':
        i += WEST
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in white_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in black_pieces or board[i] == "k" or board[i] == "K":
            break
    return result


"""

 _     _     _                     
| |__ (_)___| |__   ___  _ __  ___ 
| '_ \| / __| '_ \ / _ \| '_ \/ __|
| |_) | \__ | | | | (_) | |_) \__ \
|_.__/|_|___|_| |_|\___/| .__/|___/
                        |_|        

"""


def get_white_bishop_moves(board, tile_n):
    result = []
    # UP LEFT
    i = tile_n
    while board[i] != 'x':
        i += NORTH_WEST
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in black_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in white_pieces or board[i] == "K" or board[i] == "k":
            break

    # UP RIGHT
    i = tile_n
    while board[i] != 'x':
        i += NORTH_EAST
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in black_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in white_pieces or board[i] == "K" or board[i] == "k":
            break
    # DOWN LEFT
    i = tile_n
    while board[i] != 'x':
        i += SOUTH_WEST
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in black_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in white_pieces or board[i] == "K" or board[i] == "k":
            break

    # DOWN RIGHT
    i = tile_n
    while board[i] != 'x':
        i += SOUTH_EAST
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in black_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in white_pieces or board[i] == "K" or board[i] == "k":
            break
    return result


def get_black_bishop_moves(board, tile_n):
    result = []
    # DOWN LEFT
    i = tile_n
    while board[i] != 'x':
        i += SOUTH_EAST
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in white_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in black_pieces or board[i] == "K" or board[i] == "k":
            break

    # DOWN RIGHT
    i = tile_n
    while board[i] != 'x':
        i += SOUTH_WEST
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in white_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in black_pieces or board[i] == "K" or board[i] == "k":
            break
    # UP LEFT
    i = tile_n
    while board[i] != 'x':
        i += NORTH_EAST
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in white_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in black_pieces or board[i] == "K" or board[i] == "k":
            break

    # UP RIGHT
    i = tile_n
    while board[i] != 'x':
        i += NORTH_WEST
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in white_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in black_pieces or board[i] == "K" or board[i] == "k":
            break
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


"""
  __ _ _   _  ___  ___ _ __  ___ 
 / _` | | | |/ _ \/ _ | '_ \/ __|
| (_| | |_| |  __|  __| | | \__ \
 \__, |\__,_|\___|\___|_| |_|___/
    |_|                          

"""


def get_white_queen_moves(board, tile_n):
    result = []
    # UP
    i = tile_n
    while board[i] != 'x':
        i += NORTH
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in black_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in white_pieces or board[i] == "K" or board[i] == "k":
            break
    # DOWN
    i = tile_n
    while board[i] != 'x':
        i += SOUTH
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in black_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in white_pieces or board[i] == "K" or board[i] == "k":
            break

    # LEFT
    i = tile_n
    while board[i] != 'x':
        i += WEST
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in black_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in white_pieces or board[i] == "K" or board[i] == "k":
            break

    # RIGHT
    i = tile_n
    while board[i] != 'x':
        i += EAST
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in black_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in white_pieces or board[i] == "K" or board[i] == "k":
            break

    # UP LEFT
    i = tile_n
    while board[i] != 'x':
        i += NORTH_WEST
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in black_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in white_pieces or board[i] == "K" or board[i] == "k":
            break

    # UP RIGHT
    i = tile_n
    while board[i] != 'x':
        i += NORTH_EAST
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in black_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in white_pieces or board[i] == "K" or board[i] == "k":
            break
    # DOWN LEFT
    i = tile_n
    while board[i] != 'x':
        i += SOUTH_WEST
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in black_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in white_pieces or board[i] == "K" or board[i] == "k":
            break

    # DOWN RIGHT
    i = tile_n
    while board[i] != 'x':
        i += SOUTH_EAST
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in black_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in white_pieces or board[i] == "K" or board[i] == "k":
            break

    return result


def get_black_queen_moves(board, tile_n):
    result = []
    # UP
    i = tile_n
    while board[i] != 'x':
        i += SOUTH
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in white_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in black_pieces or board[i] == "k" or board[i] == "K":
            break
    # DOWN
    i = tile_n
    while board[i] != 'x':
        i += NORTH
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in white_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in black_pieces or board[i] == "k" or board[i] == "K":
            break

    # LEFT
    i = tile_n
    while board[i] != 'x':
        i += EAST
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in white_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in black_pieces or board[i] == "k" or board[i] == "K":
            break

    # RIGHT
    i = tile_n
    while board[i] != 'x':
        i += WEST
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in white_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in black_pieces or board[i] == "k" or board[i] == "K":
            break

    # DOWN LEFT
    i = tile_n
    while board[i] != 'x':
        i += SOUTH_EAST
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in white_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in black_pieces or board[i] == "K" or board[i] == "k":
            break

    # DOWN RIGHT
    i = tile_n
    while board[i] != 'x':
        i += SOUTH_WEST
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in white_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in black_pieces or board[i] == "K" or board[i] == "k":
            break
    # UP LEFT
    i = tile_n
    while board[i] != 'x':
        i += NORTH_EAST
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in white_pieces:
            result.append(i)
            break
        # self block
        if board[i] in black_pieces or board[i] == "K" or board[i] == "k":
            break

    # UP RIGHT
    i = tile_n
    while board[i] != 'x':
        i += NORTH_WEST
        # open square
        if board[i] == 'o':
            result.append(i)
        # attack
        if board[i] in white_pieces:
            # print("ATTACK WITH ROOK")
            result.append(i)
            break
        # self block
        if board[i] in black_pieces or board[i] == "K" or board[i] == "k":
            break

    return result
