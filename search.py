from evaluate_state import evaluate_state
import random
from check_detection import white_in_check, black_in_check
from utils import copy_state
from gen_moves import get_all_moves_at_state
from move import move_at_state, run_move_at_state


# Algorithm
def best_move(state, depth=2):
    moves = get_all_moves_at_state(state)
    if len(moves) == 0:
        return None

    if state[1] == 0:
        current_score = -9999.0
    else:
        current_score = 9999.0
    move_n = -1
    turn = state[1]
    for i in range(len(moves)):
        new_state = move_at_state(state, moves[i])
        score = minimax(depth, new_state, -999, 999)
        if turn == 0:
            if score > current_score:
                move_n = i
                current_score = score
            elif score == current_score:
                if random.randint(1, 5) == 3:
                    move_n = i
                    current_score = score
        elif turn == 1:
            if score < current_score:
                move_n = i
                current_score = score
            elif score == current_score:
                if random.randint(1, 5) == 3:
                    move_n = i
                    current_score = score
    return moves[move_n]


def minimax(depth, state, alpha, beta):
    player_turn = state[1]

    if depth == 0:
        b_val = evaluate_state(state)
        return b_val
    legal_moves = get_all_moves_at_state(state)

    if player_turn == 0:
        best_value = -999
        history = []
        if len(legal_moves) is 0:
            if white_in_check(state[0], state[6]):
                return -9999
            else:
                return 9999
        for i in range(len(legal_moves)):

            moveset = legal_moves[i]
            history.append(copy_state(state))
            state = run_move_at_state(state, moveset)
            value = minimax(depth - 1, state, alpha, beta)
            state = history.pop()
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)
            if beta <= alpha:  # prune
                break
        return best_value
    elif player_turn == 1:
        history = []
        best_value = 999
        if len(legal_moves) == 0:
            if black_in_check(state[0], state[7]):
                return 9999
            else:
                return -999
        for i in range(len(legal_moves)):
            moveset = legal_moves[i]
            history.append(state)
            state = run_move_at_state(state, moveset)
            value = minimax(depth - 1, state, alpha, beta)
            state = history.pop()
            best_value = min(best_value, value)
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value
