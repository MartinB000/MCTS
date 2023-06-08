from copy import deepcopy
import random

class Player:
  def __init__(self, sign, strategy='random', *args):
    self.sign = sign
    self.strategy = strategy
    self.args = args
  
  def move(self, game):
    if self.strategy == 'random':
      self.random(game)
    elif self.strategy == 'minimax':
      self.minimax(game, 4)
    elif self.strategy == 'alpha_beta':
      self.alpha_beta(game)
    elif self.strategy == 'mcts':
      self.mcts(game)
    else:
      raise Exception('Invalid strategy')
  
  def random(self, game):
    col = random.randint(0, 6)
    try:
      game.append_checker(col, self.sign)
    except Exception as e:
      self.random(game)
  
  def evaluate(self, game):
    opp_sign = 'O' if self.sign == 'X' else 'X'
    score = 0
    for row in range(6):
      for col in range(4):
        zone = game.board[row][col] + game.board[row][col + 1] + game.board[row][col + 2] + game.board[row][col + 3]
        score += self._evaluate_zone(zone, self.sign)
        score -= self._evaluate_zone(zone, opp_sign)
    for row in range(3):
      for col in range(7):
        zone = game.board[row][col] + game.board[row + 1][col] + game.board[row + 2][col] + game.board[row + 3][col]
        score += self._evaluate_zone(zone, self.sign)
        score -= self._evaluate_zone(zone, opp_sign)
    for row in range(3):
      for col in range(4):
        zone = game.board[row][col] + game.board[row + 1][col + 1] + game.board[row + 2][col + 2] + game.board[row + 3][col + 3]
        score += self._evaluate_zone(zone, self.sign)
        score -= self._evaluate_zone(zone, opp_sign)
    for row in range(3):
      for col in range(3, 7):
        zone = game.board[row][col] + game.board[row + 1][col - 1] + game.board[row + 2][col - 2] + game.board[row + 3][col - 3]
        score += self._evaluate_zone(zone, self.sign)
        score -= self._evaluate_zone(zone, opp_sign)
    return score
        
  def _evaluate_zone(self, zone, sign):
    if zone.count(sign) == 4:
      return 100000
    elif zone.count(sign) == 3 and zone.count(' ') == 1:
      return 50
    elif zone.count(sign) == 2 and zone.count(' ') == 2:
      return 5
    elif zone.count(sign) == 1 and zone.count(' ') == 3:
      return 1  
    return 0
  
  ########################################
  ################ Minimax ###############
  ########################################
  def minimax(self, game, depth=5):
    _, action = self.max_player(game, depth)
    game.append_checker(action, self.sign)
  
  def max_player(self, game, depth):
    if depth == 0 or game.is_over():
      return self.evaluate(game), None
    max_eval = float('-inf')
    max_action = None
    for action in game.get_actions():
      temp_game = deepcopy(game)
      temp_game.append_checker(action, self.sign)
      eval, _ = self.min_player(temp_game, depth - 1)
      if eval > max_eval:
        max_eval = eval
        max_action = action
    return max_eval, max_action
  
  def min_player(self, game, depth):
    if depth == 0 or game.is_over():
      return self.evaluate(game), None
    min_eval = float('inf')
    min_action = None
    for action in game.get_actions():
      temp_game = deepcopy(game)
      temp_game.append_checker(action, self.sign)
      eval, _ = self.max_player(temp_game, depth - 1)
      if eval < min_eval:
        min_eval = eval
        min_action = action
    return min_eval, min_action
    
  
  ########################################
  ############## Alpha-Beta ##############
  ########################################
  def alpha_beta(self, game):
    pass
  
  ########################################
  ################# MCTS #################
  ########################################
  def mcts(self, game):
    pass