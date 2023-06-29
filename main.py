import random

import numpy as np
from bcolors import bcolors
import evaluate_functions as eval_strategy
import copy
import math
from mcts_board import mcts_board

from node import Node

##### Variables #####
lines = 6
columns = 7
strategy = [0, 0]
currentPlayer = 1


def mcts(maxIter, root, player):
    for iter in range(maxIter):
        front, turn = tree_policy(root, player, 2.0)
        reward = default_policy(front.state, turn)
        backup(front, reward, turn)
    ans = best_child(root, 0)
    return ans


def tree_policy(node, turn, factor):
    while not node.state.terminal() and node.state.winner() == 0:
        if not node.fully_explored():
            return expand(node, turn), -turn
        else:
            node = best_child(node, factor)
            turn *= -1
    return node, turn


def expand(node, turn):
    tried_children_move = [m for m in node.children_move]
    possible_moves = node.state.legal_moves()

    for move in possible_moves:
        if move not in tried_children_move:
            row = node.state.try_move(move)
            new_state = copy.deepcopy(node.state)
            new_state.board[row][move] = turn
            new_state.last_move = [row, move]
            break

    node.add_child(new_state, move)
    return node.children[-1]


def best_child(node, factor):
    best_score = -10000000.0
    best_children = []
    for c in node.children:
        exploit = c.reward / c.visits
        explore = math.sqrt(math.log(2.0 * node.visits) / float(c.visits))
        score = exploit + factor * explore
        if score == best_score:
            best_children.append(c)
        if score > best_score:
            best_children = [c]
            best_score = score
    return random.choice(best_children)


def default_policy(state, turn):
    while not state.terminal() and state.winner() == 0:
        state = state.next_state(turn)
        turn *= -1
    return state.winner()


def backup(node, reward, turn):
    while node is not None:
        node.visits += 1
        node.reward -= turn * reward
        node = node.parent
        turn *= -1
    return


######################################## Gestion du jeu ###############################################

# Fonction pour créer le plateau de jeu vide
def create_board():
    return np.zeros((lines, columns), dtype=int)


# Fonction pour afficher la grille de jeu
def display_grid(grid):
    print(bcolors.BORDER + "▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄")
    for lines in grid:
        display_line = "█ "
        for cells in lines:
            if cells == 1:
                display_line += bcolors.X + "◉ " + bcolors.BORDER
            elif cells == 2:
                display_line += bcolors.O + "◉ " + bcolors.BORDER
            else:
                display_line += "  "
        display_line += "█"
        print(display_line)
    print("▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀")
    print("\n" + bcolors.ENDC, end="")


# Fonction pour placer un jeton dans une colonne
def place_token(grid, column, player):
    for line in range(len(grid) - 1, -1, -1):
        if grid[line][column] == 0:
            grid[line][column] = player
            return True
    return False


# Fonction pour vérifier si un joueur a gagné
def check_victory(grid, player):
    # Vérification des lignes
    for line in range(len(grid)):
        for column in range(len(grid[0]) - 3):
            if grid[line][column] == player and grid[line][column + 1] == player and grid[line][
                column + 2] == player and grid[line][column + 3] == player:
                return True

    # Vérification des columns
    for column in range(len(grid[0])):
        for line in range(len(grid) - 3):
            if grid[line][column] == player and grid[line + 1][column] == player and grid[line + 2][
                column] == player and grid[line + 3][column] == player:
                return True

    # Vérification des diagonales ascendantes
    for line in range(len(grid) - 3):
        for column in range(len(grid[0]) - 3):
            if grid[line][column] == player and grid[line + 1][column + 1] == player and grid[line + 2][
                column + 2] == player and grid[line + 3][column + 3] == player:
                return True

    # Vérification des diagonales descendantes
    for line in range(3, len(grid)):
        for column in range(len(grid[0]) - 3):
            if grid[line][column] == player and grid[line - 1][column + 1] == player and grid[line - 2][
                column + 2] == player and grid[line - 3][column + 3] == player:
                return True

    return False


# Fonction pour obtenir les colonnes valides
def get_valid_columns(grid):
    valid_columns = []
    for column in range(columns):
        if grid[0][column] == 0:
            valid_columns.append(column)
    return valid_columns


def get_mcts_board(grid):
    board = []
    for i in range(lines):
        row = []
        for j in range(columns):
            if grid[i][j] == 0:
                row.append(0)
            if grid[i][j] == 1:
                row.append(1)
            if grid[i][j] == 2:
                row.append(-1)
        board.append(row)
    return board


def get_board(board):
    plateau = []
    for i in range(lines):
        row = []
        for j in range(columns):
            if board[i][j] == 0:
                row.append(0)
            if board[i][j] == 1:
                row.append(1)
            if board[i][j] == -1:
                row.append(2)
        plateau.append(np.asarray(row))
    return np.asarray(plateau)


################################################## MINIMAX & ALPHABETA #############################################

def minimax(grid, depth, player):
    _, action = player_max(grid, 5, player)
    return action


def alphabeta(grid, depth, player):
    _, action = player_max(grid, depth, player, float("-inf"), float("inf"))
    return action


def player_max(grid, depth, player, alpha=None, beta=None):
    valid_columns = get_valid_columns(grid)
    if depth == 0 or check_victory(grid, 1) or check_victory(grid, 2) or len(valid_columns) == 0:
        score = eval_strategy.evaluate(grid, player, strategy[player - 1])
        print("depth = " + str(depth) + " score = " + str(score) + " player = " + str(player))
        return score, None

    best_score = float("-inf")
    action = None
    for column in valid_columns:
        new_grid = grid.copy()
        place_token(new_grid, column, player)
        score, _ = player_min(new_grid, depth - 1, 3 - player, alpha, beta)
        if score > best_score:
            best_score = score
            action = column
        print("column = " + str(column))
        if alpha is not None and beta is not None:
            print("best_score = " + str(best_score) + " beta = " + str(beta))
            if best_score >= beta:
                return best_score, action
            alpha = max(alpha, best_score)
    return best_score, action


def player_min(grid, depth, player, alpha=None, beta=None):
    valid_columns = get_valid_columns(grid)
    if depth == 0 or check_victory(grid, 1) or check_victory(grid, 2) or len(valid_columns) == 0:
        # Si la profondeur maximale est atteinte ou si le jeu est terminé, retourner le score de la position
        score = eval_strategy.evaluate(grid, 3 - player, strategy[2 - player])
        print("depth = " + str(depth) + " score = " + str(score) + " player = " + str(player))
        return score, None

    best_score = float("inf")
    action = None
    for column in valid_columns:
        new_grid = grid.copy()
        place_token(new_grid, column, player)
        score, _ = player_max(new_grid, depth - 1, 3 - player, alpha, beta)
        if score < best_score:
            best_score = score
            action = column
        if alpha is not None and beta is not None:
            if best_score <= alpha:
                return best_score, action
            beta = min(beta, best_score)
    return best_score, action


def get_mcts_move(grid, player):
    node = Node(mcts_board(get_mcts_board(grid)))
    best_coup = mcts(10000, node, 1 if player == 1 else -1)
    grid = get_board(best_coup.state.board)
    return grid


def get_best_move(grid, depth, player, algo):
    match algo:
        case 1:
            return minimax(grid, depth, player)
        case 2:
            return alphabeta(grid, depth, player)


#################### Gestion affichage ############################
def agent_name_from_index(player_number, agents, layers):
    if player_number == 1:
        print("Joueur", player_number, " " + bcolors.X + "◉ " + bcolors.ENDC, ":")
    else:
        print("Joueur", player_number, " " + bcolors.O + "◉ " + bcolors.ENDC, ":")
    player_number = player_number - 1
    agent = agents[player_number]
    match agent:
        case 0:
            name = "Joueur"
        case 1:
            name = "Minimax"
        case 2:
            name = "Alpha-Beta"
        case 3:
            name = "MCTS"
    if (agent == 1 or agent == 2):
        name += " profondeur " + str(layers[player_number])

    return name


def play(agents, depths):
    board = create_board()
    global currentPlayer
    player = 1
    end_game = False
    while not end_game:
        if agents[player - 1] == 0:
            column = int(input("Joueur " + str(player) + bcolors.X + " ◉ " + bcolors.ENDC + ", choisissez une colonne (de 1 à 7) : ")) - 1
            while column < 0 or column > columns-1:
                column = int(input("Joueur " + str(player) + ", choisissez une colonne (de 1 à 7) : ")) - 1
            if not place_token(board, column, player):
                move = False
            else:
                move = True
        else:
            if agents[player - 1] == 1 or agents[player - 1] == 2:
                column = get_best_move(board, depths[player - 1], player, agents[player - 1])
                place_token(board, column, player)
            else:
                board = get_mcts_move(board, player)
            move = True

        print(agent_name_from_index(player, agents, depths))
        display_grid(board)

        if move:
            if check_victory(board, player):
                if player == 1:
                    print("Joueur " + str(player) + bcolors.X + " ◉ " + bcolors.ENDC + " a gagné !")
                else :
                    print("Joueur " + str(player) + bcolors.O + " ◉ " + bcolors.ENDC + " a gagné !")
                end_game = True
            elif len(get_valid_columns(board)) == 0:
                print("Match nul !")
                end_game = True
            else:
                player = 3 - player
                currentPlayer = player
        else:
            print("La colonne est pleine. Veuillez choisir une autre colonne.")


def main():
    print("Connect 4")
    print("_________________________")
    print("0: Joueur\n1: Minimax\n2: AlphaBeta\n3: MCTS")
    print("_________________________")
    agent1 = int(input("Type de joueur 1 : "))
    agent2 = int(input("Type de joueur 2 : "))
    depth1 = 0
    depth2 = 0

    if agent1 == 1 or agent1 == 2:
        depth1 = int(input("Profondeur IA 1: "))
        print("0: Agressive |  1: Modérée |  2: Défensive")
        strategy[0] = int(input("Stratégie IA 1: "))
    if agent2 == 1 or agent2 == 2:
        depth2 = int(input("Profondeur IA 2: "))
        print("0: Agressive |  1: Modérée |  2: Défensive")
        strategy[1] = int(input("Stratégie IA 2: "))

    play([agent1, agent2], [depth1, depth2])


# Stratégie - 0: Agressive |  1: Modérée |  2: Défensive
# Premier paramètre
# 0: Joueur
# 1: Minimax
# 2: AlphaBeta
# 3: MCTS
# Deuxième paramètre = profondeur

main()
