from engine.search import best_move
from engine.utils import sq120_RF
from engine.move import move_at_state
from engine.gen_moves import get_all_moves_at_state
from engine.utils import sq120_RF
from engine.move import move_at_state
from engine.constants import EN_PAS_INDEX
from engine.utils import print_board


def test_en_passant():
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
    print_board(state[0])
    assert state[EN_PAS_INDEX] != -1
    moves = get_all_moves_at_state(state)
    assert [53, 42] in moves
