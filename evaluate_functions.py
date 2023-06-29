import numpy as np

def evaluate(game, player, strategy=0):
    opp_player = 3 - player
    plus_factor = 10 if strategy == 1 else 1
    minus_factor = 10 if strategy == 0 else 1
    score = 0
    for row in range(6):
      for col in range(4):
        zone = [game[row][col], game[row][col + 1], game[row][col + 2], game[row][col + 3]]
        score += plus_factor*evaluate_zone(zone, player)
        score -= minus_factor*evaluate_zone(zone, opp_player)
    for row in range(3):
      for col in range(7):
        zone = [game[row][col], game[row + 1][col], game[row + 2][col], game[row + 3][col]]
        score += plus_factor*evaluate_zone(zone, player)
        score -= minus_factor*evaluate_zone(zone, opp_player)
    for row in range(3):
      for col in range(4):
        zone = [game[row][col], game[row + 1][col + 1], game[row + 2][col + 2], game[row + 3][col + 3]]
        score += plus_factor*evaluate_zone(zone, player)
        score -= minus_factor*evaluate_zone(zone, opp_player)
    for row in range(3):
      for col in range(3, 7):
        zone = [game[row][col], game[row + 1][col - 1], game[row + 2][col - 2], game[row + 3][col - 3]]
        score += plus_factor+evaluate_zone(zone, player)
        score -= minus_factor*evaluate_zone(zone, opp_player)
    return score
        
def evaluate_zone(zone, sign):
    if zone.count(sign) == 4:
        return 1000
    elif zone.count(sign) == 3 and zone.count(' ') == 1:
        return 50
    elif zone.count(sign) == 2 and zone.count(' ') == 2:
        return 5
    elif zone.count(sign) == 1 and zone.count(' ') == 3:
        return 1
    return 0