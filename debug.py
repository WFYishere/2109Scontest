from simulator import GameController, HumanAgent
from AIAgent import *
from minimax import MNXAgent
from connect_four import ConnectFour

board = ConnectFour()
game = GameController(board=board, agents=[MNXAgent(2), AIAgent(1)])
game.run()