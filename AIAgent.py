from game_utils import *
from random import shuffle
import numpy as np

SCORE_FOR_CENTER_COLUMN = 3
SCORE_FOR_FOUR = 10000
SCORE_FOR_THREE = 2
SCORE_FOR_TWO = 5
OPPONENT_THREE = 4
#TODO: test constants

class AIAgent:
    def __init__(self, player_id=1, depth=4):
        self.player_id = player_id
        self.depth = depth
        self.depth = depth if player_id == 1 else depth + 1

    def make_move(self, state):
        best_move = None
        best_score = -float('inf')
        alpha = -float('inf')
        beta = float('inf')

        valid_moves = get_valid_col_id(state)
        shuffle(valid_moves)

        for col_id in valid_moves:
            next_state = step(state.copy(), col_id=col_id, player_id=self.player_id, in_place=False)
            score = minimax(next_state, self.depth - 1, False, self.player_id, alpha, beta)
            if score > best_score:
                best_score = score
                best_move = col_id
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break 

        return best_move


def minimax(state, depth, is_maximizing_player, player_id, alpha, beta):

    if is_win(state) or is_end(state) or depth == 0:
        return evaluate_intermediate_state(state, player_id)

    if is_maximizing_player:
        max_eval = float('-inf')
        valid_moves = get_valid_col_id(state)
        shuffle(valid_moves)
        for col_id in valid_moves:
            next_state = step(state.copy(), col_id=col_id, player_id=player_id, in_place=False)
            eval = minimax(next_state, depth - 1, False, player_id, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        opponent_id = 3 - player_id
        for col_id in get_valid_col_id(state):
            next_state = step(state.copy(), col_id=col_id, player_id=opponent_id, in_place=False)
            eval = minimax(next_state, depth - 1, True, player_id, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def evaluate_intermediate_state(state, player_id):
    score = 0
    opponent_id = 3 - player_id

    center_count = sum(1 for row in state if row[3] == player_id)
    score += center_count * SCORE_FOR_CENTER_COLUMN

    score += get_windows_score(state, player_id)

    return score

def get_windows_score(state, player_id, window_length=4):
    rows, cols = state.shape
    score = 0
    dirs = [[0,1], [1,0], [1,1], [-1,1]] 

    for r in range(rows):
        for c in range(cols):
            for dir in dirs:
                window = []
                for k in range(window_length):
                    r_pos = r + k * dir[0]
                    c_pos = c + k * dir[1]
                    if 0 <= r_pos < rows and 0 <= c_pos < cols:
                        window.append(state[r_pos][c_pos])
                    else:
                        break 
                if len(window) == window_length:
                    score += evaluate_window(window, player_id)

    return score

def evaluate_window(window, player_id):
    opponent_id = 3 - player_id
    score = 0

    player_scores = {4: SCORE_FOR_FOUR,
                      3: SCORE_FOR_THREE,
                      2: SCORE_FOR_TWO}

    player_count = window.count(player_id)
    opponent_count = window.count(opponent_id)

    score += player_scores.get(player_count, 0)
    if opponent_count == 3:
        score -= OPPONENT_THREE

    return score