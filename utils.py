from hlt.positionals import *
import logging

def getMax (game):
    return [game.game_map.width, game.game_map.height]

def setBorders(game, maxx):
    if (game.me.shipyard.position.x > maxx / 2):
        lb = maxx / 2
        rb = maxx
        return int(lb), int(rb)
    else:
        rb = maxx /2 - 1
        lb = 0
        return int(lb), int(rb)
    
def getNearestMaxHalitePosition(game, lb, rb, maxy, current_pos):
    maximumHalite = {'amount': []}
    for x in range(lb, rb + 1):
        for y in range(0, maxy):
            surroundingHalite = []
            for pos in Position(x, y).get_surrounding_cardinals():
                surroundingHalite += [game.game_map[pos].halite_amount]
            totalHalite = [game.game_map[Position(x, y)].halite_amount] + surroundingHalite
            if ((sum(maximumHalite['amount']) < sum(totalHalite)) and (game.game_map.calculate_distance(current_pos, Position(x,y)) < 15)):
                maximumHalite['amount'] = totalHalite
                maximumHalite['position'] = Position(x,y)
    return maximumHalite['position']

"""def getNearestMaxHalite(game, lb, rb, maxy):
    maximumHalites = []
    for x in range(lb, rb + 1):
        maximumHalites.append([])
        for y in range(0, maxy):
            totalHalite = []
            for pos in Position(x, y).get_surrounding_cardinals():
                totalHalite += [game.game_map[pos].halite_amount]
            totalHalite = [game.game_map[Position(x, y)].halite_amount] + totalHalite
            maximumHalites[x] += sum(totalHalite)

            #use zip and sorted(zip, key = operator.getitem())
"""


