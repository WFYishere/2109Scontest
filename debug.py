from simulator import GameController, HumanAgent
from AIAgent import *
from connect_four import ConnectFour

board = ConnectFour()
game = GameController(board=board, agents=[HumanAgent(1), AIAgent(2)])
game.run()