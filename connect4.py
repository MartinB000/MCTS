from player import Player

class Connect4:
  def __init__(self, strategy1='random', strategy2='random', *args1, **args2):
    self.board = [[' ' for _ in range(7)] for _ in range(6)]
    self.players = [Player('X',strategy1,args1), Player('O',strategy2,args2)]
    self.moves = 0
    self.player = self.players[self.moves % 2]
    self.winner = None
  
  def play(self):
    while self.winner is None and self.moves < 42:
      self.player = self.players[self.moves % 2]
      self.player.move(self)
      print(self)
    if self.winner is None:
      print('Draw')
    else:
      print(f'Winner: {self.winner.sign}')
  
  def append_checker(self, col, sign):
    if self.winner is not None:
      raise Exception('Game already won')
    if not 0 <= col <= 6:
      raise Exception('Invalid column')
    if self.board[0][col] != ' ':
      raise Exception('Column is full')
    
    for row in range(5, -1, -1):
      if self.board[row][col] == ' ':
        self.board[row][col] = sign
        if self._check_for_winner(row, col):
          self.winner = self.player
        break
    self.moves += 1

  
  def _check_for_winner(self, row, col):
    directions = ((1, 0), (0, 1), (1, 1), (1, -1))
    for dx, dy in directions:
      count = self._count(row, col, dx, dy)
      if count >= 4:
        self.winner = self.player
        return True
    return False
  
  def _count(self, row, col, dx, dy):
    count = 1
    count += self._count_in_direction(row, col, dx, dy)
    count += self._count_in_direction(row, col, -dx, -dy)
    return count
  
  def _count_in_direction(self, row, col, dx, dy):
    count = 0
    while True:
      row += dy
      col += dx
      if not (0 <= row < 6 and 0 <= col < 7):
        break
      if self.board[row][col] != self.player.sign:
        break
      count += 1
    return count
  
  def get_actions(self):
    return [col for col in range(7) if self.board[0][col] == ' ']
  
  def is_over(self):
    return self.winner is not None or self.moves >= 42
  
  def __str__(self):
    return ' _____________\n' + '\n'.join(['|' + ' '.join(row) + '|' for row in self.board]) + '\n ‾‾‾‾‾‾‾‾‾‾‾‾‾'