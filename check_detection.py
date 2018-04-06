from constants import *


def white_in_check(board, tile_n):
    if check_black_sliders(board, tile_n) is True:
        return True
    if check_black_knights(board, tile_n) is True:
        return True
    if check_black_king(board, tile_n) is True:
        return True
    if check_black_pawns(board, tile_n) is True:
        return True
    else:
        return False


def black_in_check(board, tile_n):
    if check_white_sliders(board, tile_n) is True:
        return True
    if check_white_knights(board, tile_n) is True:
        return True
    if check_white_king(board, tile_n) is True:
        return True
    if check_white_pawns(board, tile_n) is True:
        return True
    return False


def check_black_pawns(board, tile_n):
    if board[tile_n - 11] == 'p':
        # print("warning black pawn")
        return True
    if board[tile_n - 9] == 'p':
        # print("warning black pawn")
        return True
    return False


def check_white_pawns(board, tile_n):
    if board[tile_n + 11] == 'P':
        # print("warning white pawn")
        return True
    if board[tile_n + 9] == 'P':
        # print("warning white pawn")

        return True
    return False


def check_black_king(board, tile_n):
    directions = [11, 10, 9, 1, -11, -10, -9, -1]
    for direction in directions:
        if board[tile_n + direction] == 'k':
            return True
    return False


def check_white_king(board, tile_n):
    directions = [11, 10, 9, 1, -11, -10, -9, -1]
    for direction in directions:
        if board[tile_n + direction] == 'K':
            return True
    return False


def check_black_knights(board, tile_n):
    directions = [21, 19, 12, 8, -21, -19, -8, -12]
    for direction in directions:
        # print(tile_n+direction)
        if board[tile_n + direction] == 'n':
            return True
    return False


def check_white_knights(board, tile_n):
    directions = [21, 19, 12, 8, -21, -19, -8, -12]
    for direction in directions:
        if board[tile_n + direction] == 'N':
            return True
    return False


def check_black_sliders(board, tile_n):
    slider_found = False
    # UP
    i = tile_n
    while board[i] != 'x':
        i -= 10
        if board[i] in all_white:
            break
        if board[i] in "pkbn":
            break
        if board[i] in "qr":
            slider_found = True
            return slider_found  # no need to check any more

    # DOWN
    i = tile_n
    while board[i] != 'x':
        i += 10
        if board[i] in all_white:
            break
        if board[i] in "pkbn":
            break
        if board[i] in "qr":
            slider_found = True
            return slider_found  # no need to check any more

    # LEFT
    i = tile_n
    while board[i] != 'x':
        i -= 1
        if board[i] in all_white:
            break
        if board[i] in "pkbn":
            break
        if board[i] in "qr":
            slider_found = True
            return slider_found  # no need to check any more

    # RIGHT
    i = tile_n
    while board[i] != 'x':
        i += 1
        if board[i] in all_white:
            break
        if board[i] in "pkbn":
            break
        if board[i] in "qr":
            slider_found = True
            return slider_found  # no need to check any more

    # UP LEFT
    i = tile_n
    while board[i] != 'x':
        i -= 11
        if board[i] in all_white:
            break
        if board[i] in "pkrn":
            break
        if board[i] in "qb":
            slider_found = True
            return slider_found  # no need to check any more

    # UP RIGHT
    i = tile_n
    while board[i] != 'x':
        i -= 9
        if board[i] in all_white:
            break
        if board[i] in "pkrn":
            break
        if board[i] in "qb":
            slider_found = True
            return slider_found  # no need to check any more

    # DOWN LEFT
    i = tile_n
    while board[i] != 'x':
        i += 9
        if board[i] in all_white:
            break
        if board[i] in "pkrn":
            break
        if board[i] in "qb":
            slider_found = True
            return slider_found  # no need to check any more

    # DOWN RIGHT
    i = tile_n
    while board[i] != 'x':
        i += 11
        if board[i] in all_white:
            break
        if board[i] in "pkrn":
            break
        if board[i] in "qb":
            slider_found = True
            return slider_found  # no need to check any more

    return slider_found


def check_white_sliders(board, tile_n):
    slider_found = False
    # UP
    i = tile_n
    while board[i] != 'x':
        i -= 10
        if board[i] in all_black:
            break
        if board[i] in "PKBN":
            break

        if board[i] in "QR":
            slider_found = True
            return slider_found  # no need to check any more

    # DOWN
    i = tile_n
    while board[i] != 'x':
        i += 10
        if board[i] in all_black:
            break
        if board[i] in "PKBN":
            break

        if board[i] in "QR":
            # print("queen rook ")
            slider_found = True
            return slider_found  # no need to check any more

    # LEFT
    i = tile_n
    while board[i] != 'x':
        i -= 1
        if board[i] in all_black:
            break
        if board[i] in "PKBN":
            break
        if board[i] in "QR":
            # print("slider at", self.sq64_to_RF(self.sq120_sq64(i)))
            slider_found = True
            return slider_found  # no need to check any more

    # RIGHT
    i = tile_n
    while board[i] != 'x':
        i += 1
        if board[i] in all_black:
            break
        if board[i] in "PKBN":
            break
        if board[i] in "QR":
            slider_found = True
            return slider_found  # no need to check any more

    # UP LEFT
    i = tile_n
    while board[i] != 'x':
        i -= 11
        if board[i] in all_black:
            break
        if board[i] in "pkbn":
            break
        if board[i] in "QB":
            slider_found = True
            return slider_found  # no need to check any more

    # UP RIGHT
    i = tile_n
    while board[i] != 'x':
        i -= 9
        if board[i] in all_black:
            break
        if board[i] in "pkbn":
            break
        if board[i] in "QB":
            slider_found = True
            return slider_found  # no need to check any more

    # DOWN LEFT
    i = tile_n
    while board[i] != 'x':
        i += 9
        if board[i] in all_black:
            break
        if board[i] in "pkbn":
            break
        if board[i] in "QB":
            slider_found = True
            return slider_found  # no need to check any more

    # DOWN RIGHT
    i = tile_n
    while board[i] != 'x':
        i += 11
        if board[i] in all_black:
            break
        if board[i] in "pkbn":
            break
        if board[i] in "QB":
            slider_found = True
            return slider_found  # no need to check any more

    return slider_found
