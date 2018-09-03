from engine.search import best_move
from engine.utils import sq120_RF
from engine.move import move_at_state


def test_white_checkmates():
    one_from_mate_board = \
        "x" * 20 + \
        "xoooooookx" + \
        "xQooooooox" + \
        "xoooooooox" * 4 + \
        "xoooooooox" + \
        "xoRoKoooox" + \
        "x" * 20
    state = [one_from_mate_board, 0, -1, 0, 0, [0, 0, 0, 0],
             one_from_mate_board.index('K'), one_from_mate_board.index('k')]
    move = best_move(state, 3, randomness=False)
    assert sq120_RF(move[0]) == 'B1'
    assert sq120_RF(move[1]) == 'B8'
    state = move_at_state(state, move)
    assert best_move(state, 3, randomness=False) is None
