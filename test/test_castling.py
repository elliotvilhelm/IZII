from engine.constants import init_state
from engine.check_castle import check_wc_k, check_wc_q, check_bc_k, check_bc_q
from engine.constants import CASTLE_OPEN, CASTLE_VOIDED, CASTLE_NEW, CASTLED, WKC_INDEX, WQC_INDEX, C_PERM_INDEX, WHITE
from engine.move import move_at_state
from engine.utils import RF_sq120, print_board


def test_init_castling():
    castle_perms = init_state[C_PERM_INDEX]
    assert castle_perms[WKC_INDEX] == CASTLE_NEW
    assert castle_perms[WQC_INDEX] == CASTLE_NEW


def test_wq_castle_voided():
    board = "xxxxxxxxxx" \
            "xxxxxxxxxx" \
            "xrnbqkbnrx" \
            "xpoppppppx" \
            "xopoooooox" \
            "xoooooooox" \
            "xoooooooox" \
            "xPooooooox" \
            "xoPPPPPPPx" \
            "xRNBQKBNRx" \
            "xxxxxxxxxx" \
            "xxxxxxxxxx"
    state = init_state
    state[0] = board
    move = [RF_sq120('A', '1'), RF_sq120('A', '2')]
    state = move_at_state(state, move)
    assert state[C_PERM_INDEX][WQC_INDEX] == CASTLE_VOIDED


def test_wk_castle_voided():
    board = "xxxxxxxxxx" \
            "xxxxxxxxxx" \
            "xrnbqkbnrx" \
            "xpoppppppx" \
            "xopoooooox" \
            "xoooooooox" \
            "xoooooooox" \
            "xoooooooPx" \
            "xPPPPPPPox" \
            "xRNBQKBNRx" \
            "xxxxxxxxxx" \
            "xxxxxxxxxx"
    state = init_state
    state[0] = board
    move = [RF_sq120('H', '1'), RF_sq120('H', '2')]
    state = move_at_state(state, move)
    assert state[C_PERM_INDEX][WKC_INDEX] == CASTLE_VOIDED
