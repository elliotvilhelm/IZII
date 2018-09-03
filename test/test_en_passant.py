from engine.gen_moves import get_all_moves_at_state
from engine.move import move_at_state
from engine.constants import EN_PAS_INDEX


def test_black_en_passant():
    one_from_mate_board = \
        "x" * 20 + \
        "xoooooooox" + \
        "xopoooooox" + \
        "xoooooooox" + \
        "xooPooooox" + \
        "xoooooooox" + \
        "xoooooooox" + \
        "xoooooooox" + \
        "xoooooooox" + \
        "x" * 20
    state = [one_from_mate_board, 1, -1, 0, 0, [0, 0, 0, 0],
             0, 0]
    moves = get_all_moves_at_state(state)
    assert [32, 52] in moves
    state = move_at_state(state, [32, 52])
    assert state[EN_PAS_INDEX] != -1
    moves = get_all_moves_at_state(state)
    assert [53, 42] in moves
    state = move_at_state(state, [53, 42])
    assert 'p' not in state[0]


def test_white_en_passant():
    one_from_mate_board = \
        "x" * 20 + \
        "xoooooooox" + \
        "xoooooooox" + \
        "xoooooooox" + \
        "xoooooooox" + \
        "xoopooooox" + \
        "xoooooooox" + \
        "xoPoooooox" + \
        "xoooooooox" + \
        "x" * 20
    state = [one_from_mate_board, 0, -1, 0, 0, [0, 0, 0, 0],
             0, 0]
    moves = get_all_moves_at_state(state)
    assert [82, 62] in moves
    state = move_at_state(state, [82, 62])
    assert state[EN_PAS_INDEX] != -1
    moves = get_all_moves_at_state(state)
    assert [63, 72] in moves
    state = move_at_state(state, [63, 72])
    assert 'P' not in state[0]

