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

def cheesePositio (game):
    logging.info(f'inside')
    for x in range(game.game_map.width):
        for y in range(game.game_map.height):
            #logging.info(f'structure thing: {type(game.me.shipyard)} ')
            if ((game.game_map[Position(x, y)].structure_type == type(game.me.shipyard)) and (game.me.shipyard.position != Position(x, y))):
                logging.info(f'inside')
                return Position(x, y)


def display_stuff(game):
    logging.info(f'{game.players}')
    logging.info(f'{game.players[1]}')
    logging.info(f'{type(game.players)}')
    logging.info(f'{type(game.players[0])}')
        
def cheesePosition (game):
    for id, player in game.players.items():
        if (id != game.me.id):
            return player.shipyard.position

    """for player in game.players:
        logging.info(f'{player}')
        logging.info(f'{type(player)}')"""
    """if (player != my_id):
            logging.info('not equal')"""
    """#try:
                return game.game_map.get_unsafe_moves(ship.position, player.shipyard.position)[0]
            #except:
            #    return Direction.Still"""

def is_occupied_by_me (game, pos):
    if (game.game_map[pos].is_occupied):
        for ship in game.me.get_ships():
            if (ship.position == pos):
                return True
    else:
        return False

def move(game, current_pos, destination):
    resultMoves = game.game_map.get_unsafe_moves(current_pos, destination)
    if (not resultMoves):
        return Direction.Still
    else:
        for one_move in resultMoves:
            if (not is_occupied_by_me(game, current_pos.directional_offset(one_move))) and not ship_moves_here(game, destination):
                return one_move
    return Direction.Still

def ship_moves_here(game, pos):
    for ship in game.me.get_ships():
        for direction in Direction.get_all_cardinals():
            if ship.position.directional_offset(direction) == pos:
                return True
    return False
        #return resultMoves[0]