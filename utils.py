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
    
def getMaxHalitePosition(game, lb, rb, maxy):
    maximumHalite = {'amount': []}
    for x in range(lb, rb + 1):
        #logging.info("in the loop")
        for y in range(0, maxy):
            #logging.info("in the loop 2222222")
            surroundingHalite = []
            for pos in Position(x, y).get_surrounding_cardinals():
                surroundingHalite += [game.game_map[pos].halite_amount]
            totalHalite = [game.game_map[Position(x, y)].halite_amount] + surroundingHalite
            #logging.info("totalHalite =   {}".format(totalHalite))
            if (sum(maximumHalite['amount']) < sum(totalHalite)):
                maximumHalite['amount'] = totalHalite
                maximumHalite['position'] = Position(x,y)
                #logging.info("maxHaliteOld =      {}".format(maximumHalite))
    #logging.info("maxHalite =      {}".format(maximumHalite))
    return maximumHalite['position']
        


