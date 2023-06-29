from copy import deepcopy
import random

lines = 6
columns = 7

dx = [1, 1, 1, 0]
dy = [1, 0, -1, 1]

class mcts_board(object):

    def __init__(self, board, last_move=None):
        if last_move is None:
            last_move = [None, None]
        self.board = board
        self.last_move = last_move

    def try_move(self, move):
        if move < 0 or move > columns or self.board[0][move] != 0:
            return -1

        for i in range(len(self.board)):
            if self.board[i][move] != 0:
                return i - 1
        return len(self.board) - 1

    def terminal(self):
        for i in range(len(self.board[0])):
            if self.board[0][i] == 0:
                return False
        return True

    def legal_moves(self):
        legal = []
        for i in range(len(self.board[0])):
            if self.board[0][i] == 0:
                legal.append(i)

        return legal

    def next_state(self, turn):
        aux = deepcopy(self)
        moves = aux.legal_moves()
        if len(moves) > 0:
            ind = random.randint(0, len(moves) - 1)
            row = aux.try_move(moves[ind])
            aux.board[row][moves[ind]] = turn
            aux.last_move = [row, moves[ind]]
        return aux

    def winner(self):
        x = self.last_move[0]
        y = self.last_move[1]

        if x is None:
            return 0

        for d in range(4):
            h_counter = 0
            c_counter = 0
            for k in range(-3, 4):
                u = x + k * dx[d]
                v = y + k * dy[d]
                if u < 0 or u >= lines:
                    continue
                if v < 0 or v >= columns:
                    continue
                if self.board[u][v] == -1:
                    c_counter = 0
                    h_counter += 1
                elif self.board[u][v] == 1:
                    h_counter = 0
                    c_counter += 1
                else:
                    h_counter = 0
                    c_counter = 0
                if h_counter == 4:
                    return -1
                if c_counter == 4:
                    return 1
        return 0