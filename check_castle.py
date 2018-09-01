from check_detection import *
from constants import CASTLED, CASTLE_NEW, CASTLE_OPEN, CASTLE_VOIDED


def check_wc_k(state):  # return true if kingside castle is availible
    # check if im in check
    # check if state perm is valid
    # check if the path is clear
    castle_perm = state[5][0]
    board = state[0]
    if castle_perm == CASTLE_VOIDED:
        return False
    elif castle_perm == CASTLED:
        return False
    elif white_in_check(state[0], state[6]):
        return False
    elif white_in_check(state[0], state[6] + 1):
        return False

    elif board[96] == 'o' and board[97] == 'o':  # and castle_perm !=  and castle_perm != 2:
        return True
    else:
        return False


def check_wc_q(state):  # return true if kingside castle is availible
    # check if im in check
    # check if state perm is valid
    # check if the path is clear
    board = state[0]
    castle_perm = state[5][1]
    if castle_perm == CASTLE_VOIDED:
        return False
    elif castle_perm == CASTLED:
        return False
    elif white_in_check(state[0], state[6]):
        return False
    elif white_in_check(state[0], state[6] - 1):
        return False

    elif board[92] == 'o' and board[93] == 'o' and board[94] == 'o':
        return True
    return False


def check_bc_k(state):  # return true if kingside castle is availible
    # check if im in check
    # check if state perm is valid
    # check if the path is clear
    board = state[0]
    castle_perm = state[5][2]
    if castle_perm == CASTLE_VOIDED:
        return False
    elif castle_perm == CASTLED:
        return False
    elif black_in_check(state[0], state[7]):
        return False
    elif black_in_check(state[0], state[7] + 1):
        return False

    elif board[26] == 'o' and board[27] == 'o':
        return True
    return False


def check_bc_q(state):  # return true if kingside castle is availible
    # check if im in check
    # check if state perm is valid
    # check if the path is clear
    board = state[0]
    castle_perm = state[5][3]

    if castle_perm == CASTLE_VOIDED:
        return False
    elif castle_perm == CASTLED:
        return False
    elif black_in_check(state[0], state[7]):
        return False
    elif black_in_check(state[0], state[7] - 1):
        return False

    elif board[22] == 'o' and board[23] == 'o' and board[24] == 'o':
        return True
    return False
