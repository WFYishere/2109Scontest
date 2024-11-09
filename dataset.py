from AIAgent import evaluate_intermediate_state
import numpy as np
board = np.array([
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,1,1,0,0,0],
        ])
player_id = 1
score = evaluate_intermediate_state(board, player_id)
print(score)