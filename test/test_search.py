from engine.search import best_move
from engine.constants import init_state
from engine.utils import RF_sq120
from engine.utils import sq120_RF
from engine.utils import print_board


def test_search_initial_move():
    assert best_move(list(init_state), 2, randomness=False) == [RF_sq120('B', '1'), RF_sq120('C', '3')]
