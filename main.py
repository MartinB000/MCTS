from connect4 import Connect4
from player import Player

strategy = 'minimax'
depth = 5
#strategy = 'alpha_beta'
#strategy = 'mcts'

if __name__ == '__main__':
    game = Connect4(strategy1=strategy, strategy2="human")
    print(game)
    
    while game.winner is None and game.moves < 42:
        game.play()
        print(game)