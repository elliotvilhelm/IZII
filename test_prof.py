from engine.search import best_move
from engine.constants import init_state
from engine.move import move_at_state

depth = 3
state = move_at_state(init_state, best_move(init_state, depth))
state = move_at_state(state, best_move(state, depth))
# state = move_at_state(state, best_move(state, depth))
# state = move_at_state(state, best_move(state, depth))
# state = move_at_state(state, best_move(state, depth))

