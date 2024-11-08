from game_utils import *
import numpy as np

SCORE_FOR_CENTER_COLUMN = 10
SCORE_FOR_TWO_IN_A_ROW = 8
SCORE_FOR_THREE_IN_A_ROW = 15
#TODO: test constants

class AIAgent:
    def __init__(self, player_id=0, depth=4):
        self.player_id = player_id
        self.depth = depth

    def make_move(self, state):
        best_move = None
        best_score = float('-inf') if self.player_id == 1 else float('inf')
        alpha = float('-inf')
        beta = float('inf')
        cache = {}

        for col_id in get_valid_col_id(state):
            next_state = step(state.copy(), col_id=col_id, player_id=self.player_id, in_place=False)
            score = minimax(next_state, self.depth, False, self.player_id, alpha, beta, cache)

            if self.player_id == 1:
                if score > best_score:
                    best_score = score
                    best_move = col_id
                alpha = max(alpha, best_score)
            else:
                if score < best_score:
                    best_score = score
                    best_move = col_id
                beta = min(beta, best_score)

            if beta <= alpha:
                break 

        return best_move

def minimax(state, depth, is_maximizing_player, player_id, alpha, beta, cache):
    state_key = state.tostring()  
    if state_key in cache:
        return cache[state_key]

    if is_win(state):
        return 100 if is_maximizing_player else -100
    if is_end(state):
        return 0 

    if depth == 0:
        return evaluate_intermediate_state(state, player_id)

    if is_maximizing_player:
        max_eval = float('-inf')
        for col_id in get_valid_col_id(state):
            next_state = step(state.copy(), col_id=col_id, player_id=player_id, in_place=False)
            eval = minimax(next_state, depth - 1, False, player_id, alpha, beta, cache)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        cache[state_key] = max_eval
        return max_eval
    else:
        min_eval = float('inf')
        opponent_id = 3 - player_id
        for col_id in get_valid_col_id(state):
            next_state = step(state.copy(), col_id=col_id, player_id=opponent_id, in_place=False)
            eval = minimax(next_state, depth - 1, True, player_id, alpha, beta, cache)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        cache[state_key] = min_eval
        return min_eval

def evaluate_intermediate_state(state, player_id):
    score = 0

    center_count = sum(1 for row in state if row[3] == player_id)
    score += center_count * SCORE_FOR_CENTER_COLUMN

    score += two_in_a_row(state, player_id) * SCORE_FOR_TWO_IN_A_ROW  
    score += three_in_a_row(state, player_id) * SCORE_FOR_THREE_IN_A_ROW 

    opponent_id = 3 - player_id
    score -= two_in_a_row(state, opponent_id) * SCORE_FOR_TWO_IN_A_ROW
    score -= three_in_a_row(state, opponent_id) * SCORE_FOR_THREE_IN_A_ROW

    return max(1, min(100, score))

def two_in_a_row(state, player_id):
    count = 0
    rows, cols = state.shape

    for row in range(rows):
        for col in range(cols): 
            count += is_two_in_a_row(state, player_id, row, col)

    return count

def three_in_a_row(state, player_id):
    count = 0
    rows, cols = state.shape

    for row in range(rows):
        for col in range(cols):
            count += is_three_in_a_row(state, player_id, row, col)

    return count

def is_two_in_a_row (state, player_id, row, col):
    rows,cols = state.shape
    count = 0

    is_horizontal_two = ((col < cols - 1) and 
                         ((state[row, col] == player_id and state[row, col + 1] == player_id) and 
                          (((col > 0 and state[row, col - 1] != player_id) or col ==0) and 
                           ((col < cols - 2 and state[row, col + 2] != player_id) or col == cols - 2))))
    
    is_vertical_two = ((row < rows - 1) and
                       ((state[row, col] == player_id and state[row + 1, col] == player_id) and
                        (((row > 0 and state[row - 1, col] == 0) or row == 0) and
                         ((row < rows - 2 and state[row + 2, col] == 0) or row == rows - 2))))
    is_left_to_right_two = ((row < rows - 1 and col < cols - 1) and
                            ((state[row, col] == player_id and state[row + 1, col + 1] == player_id)  and 
                             (((row == 0 or col ==0) or (row > 0 and col > 0 and state[row - 1, col - 1] != player_id)) and 
                              ((row == rows - 2 or cols == cols-2) or
                               (row < rows - 2 and col < cols - 2 and state[row + 2, col + 2] == 0)))))
    is_right_to_left_two = ((row < rows - 1 and col > 0) and
                            ((state[row, col] == player_id and state[row + 1, col - 1] == player_id)  and 
                             (((row == 0 or col == cols - 1) or (row > 0 and col < cols - 1 and state[row - 1, col + 1] != player_id)) and 
                              ((row == rows - 2 or cols == 1) or
                               (row < rows - 2 and col > 1 and state[row + 2, col - 2] == 0)))))
    
    for flag in [is_horizontal_two, is_vertical_two, is_left_to_right_two, is_right_to_left_two]:
        if flag:
            count += 1

    return count

def is_three_in_a_row (state, player_id, row, col):
    rows,cols = state.shape
    count = 0

    is_horizontal = ((col < cols - 2) and 
                     (state[row, col] == player_id and state[row, col + 1] == player_id and state[row, col + 2] == player_id))
    is_vertical = ((row < rows - 2) and 
                   (state[row, col] == player_id and state[row + 1, col] == player_id and state[row + 2, col] == player_id))
    is_left_to_right = ((row < rows - 2 and col < cols - 2) and 
                        (state[row, col] == player_id and state[row + 1, col + 1] == player_id and state[row + 2, col + 2] == player_id))
    is_right_to_left = ((row > 1 and col < cols - 2) and 
                        (state[row, col] == player_id and state[row - 1, col + 1] == player_id and state[row - 2, col + 2] == player_id))
    
    for flag in [is_horizontal, is_vertical, is_left_to_right, is_right_to_left]:
        if flag:
            count += 1

    return count
