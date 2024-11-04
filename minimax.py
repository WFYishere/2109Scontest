from game_utils import *
import numpy as np

SCORE_FOR_CENTER_COLUMN = 2
SCORE_FOR_TWO_IN_A_ROW = 1
SCORE_FOR_THREE_IN_A_ROW = 3
#TODO: test constants

def minimax_reward(state, depth, is_maximizing_player, player_id):
    if is_win(state):  # which player win
        return 100 if is_maximizing_player else 1
    if is_end(state): 
        return 50
    
    if depth == 0:  # Reached max depth for evaluation
        return evaluate_intermediate_state(state, player_id)

    #TODO: check logic
    if is_maximizing_player:
        max_eval = float('-inf')
        for col_id in get_valid_col_id(state):
            next_state = step(state.copy(), col_id=col_id, player_id=player_id, in_place=False)
            eval = minimax_reward(next_state, depth - 1, False, player_id)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        opponent_id = 3 - player_id
        for col_id in get_valid_col_id(state):
            next_state = step(state.copy(), col_id=col_id, player_id=opponent_id, in_place=False)
            eval = minimax_reward(next_state, depth - 1, True, player_id)
            min_eval = min(min_eval, eval)
        return min_eval

def evaluate_intermediate_state(state, player_id):
    score = 50

    center_columns = [2,3,4]
    center_count = 0
    for center_column in center_columns:
        center_count += sum(1 for row in state if row[center_column] == player_id)
    score += center_count * SCORE_FOR_CENTER_COLUMN

    score += two_in_a_row(state, player_id) * SCORE_FOR_TWO_IN_A_ROW  
    score += three_in_a_row(state, player_id) * SCORE_FOR_THREE_IN_A_ROW 

    opponent_id = 3 - player_id
    score += two_in_a_row(state, opponent_id) * SCORE_FOR_TWO_IN_A_ROW
    score += three_in_a_row(state, opponent_id) * SCORE_FOR_THREE_IN_A_ROW

    return max(1, min(100, score))

def two_in_a_row(state, player_id):
    count = 0
    rows, cols = state.shape

    for row in range(rows):
        for col in range(cols): 
            if is_two_in_a_row(state, player_id, row, col):
                count += 1

    for row in range(1, rows):
        for col in range(cols - 1): 
            if row < rows - 1 and col < cols - 1:
                if state[row, col] == player_id and state[row + 1, col + 1] == player_id:
                    if (row > 0 and col > 0 and state[row - 1, col - 1] == 0) or (row < rows - 2 and col < cols - 2 and state[row + 2, col + 2] == 0):
                        count += 1

    for row in range(rows - 1):
        for col in range(cols - 1): 
            if state[row, col] == player_id and state[row + 1, col + 1] == player_id:
                if (row < rows - 2 and col < cols - 2 and state[row + 2, col + 2] == 0):
                    count += 1

    return count

def is_two_in_a_row (state, player_id, row, col):
    rows,cols = state.shape
    is_horizontal_two = ((col < cols - 1) and 
                         ((state[row, col] == player_id and state[row, col + 1] == player_id) and 
                          (((col > 0 and state[row, col - 1] != player_id) or col ==0) and 
                           ((col < cols - 2 and state[row, col + 2] != player_id) or col == cols - 2))))
    
    is_vertical_two = ((row < rows - 1) and
                       ((state[row, col] == player_id and state[row + 1, col] == player_id) and
                        (((row > 0 and state[row - 1, col] == 0) or row == 0) and
                         ((row < rows - 2 and state[row + 2, col] == 0) or row == rows - 2))))
    
    #TODO: is_two_in_a_row
    return is_horizontal_two or is_vertical_two

def three_in_a_row(state, player_id):
    count = 0
    rows, cols = state.shape

    #TODO: debug
    for row in range(rows):
        for col in range(cols - 2): 
            if state[row, col] == player_id and state[row, col + 1] == player_id and state[row, col + 2] == player_id:
                if (col > 0 and state[row, col - 1] == 0) or (col < cols - 3 and state[row, col + 3] == 0):
                    count += 1

    for col in range(cols):
        for row in range(rows - 2):
            if state[row, col] == player_id and state[row + 1, col] == player_id and state[row + 2, col] == player_id:
                if (row > 0 and state[row - 1, col] == 0) or (row < rows - 3 and state[row + 3, col] == 0):
                    count += 1

    for row in range(2, rows):
        for col in range(cols - 2):
            if row < rows - 1 and col < cols - 1:
                if state[row, col] == player_id and state[row - 1, col + 1] == player_id and state[row - 2, col + 2] == player_id:
                    if (row > 2 and col > 1 and state[row - 3, col + 3] == 0) or (row < rows - 1 and col < cols - 1 and state[row - 1, col + 1] == 0):
                        count += 1

    for row in range(rows - 2):
        for col in range(cols - 2):
            if state[row, col] == player_id and state[row + 1, col + 1] == player_id and state[row + 2, col + 2] == player_id:
                if (row < rows - 3 and col < cols - 3 and state[row + 3, col + 3] == 0):
                    count += 1

    return count
