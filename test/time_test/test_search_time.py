import timeit


def test_search_speed():
    setup = \
        '''from engine.search import best_move; from engine.constants import init_state
        '''
    code = \
        '''best_move(init_state, 3)'''
    iters = 2
    assert float(timeit.timeit(setup=setup, stmt=code, number=iters)/iters) < 5.0

