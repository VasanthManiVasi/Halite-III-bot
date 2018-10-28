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
            if ((sum(maximumHalite['amount']) < sum(totalHalite)) and (game.game_map.calculate_distance(current_pos, Position(x,y)) < 10)):
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

def move_to_pos(game, current_pos, destination, ship_positions, ship):
    resultMoves = game.game_map.get_unsafe_moves(current_pos, destination)
    #resultMoves += [move for move in Direction.get_all_cardinals() if move not in resultMoves]
    #resultMoves.sort(key = lambda move: game.game_map.calculate_distance(current_pos.directional_offset(move), destination), reverse = False)
    '''if (not resultMoves):
        return Direction.Still
    else:'''
    for one_move in resultMoves:
        if (not is_occupied_by_me(game, current_pos.directional_offset(one_move))) and not ship_moves_here(game, current_pos.directional_offset(one_move), ship_positions, ship):
            return one_move
    return Direction.Still

def swap_ships(game, ship, nextPos, ship_moves, ship_positions, swap_counter, command_queue):
    if (not already_swapped(ship, swap_counter)):
        next_ship = game.me.get_ship(get_id_of_ship(game, nextPos))
        if can_move(game, ship) and can_move(game, next_ship):
            append_to_queue(ship.move(just_move(game, ship.position, next_ship.position)), command_queue)
            append_to_queue(next_ship.move(just_move(game, next_ship.position, ship.position)), command_queue)
            swap_counter[ship.id] = 'swapped'
            swap_counter[next_ship.id] = 'swapped'
        else:
            append_to_queue(ship.move(Direction.Still), command_queue)
            append_to_queue(next_ship.move(Direction.Still), command_queue)
        
        ship_positions += [next_ship.position] + [ship.position]
        ship_moves[ship.id] = 'done'
        ship_moves[next_ship.id] = 'done'
        
    else:
        append_to_queue(ship.move(Direction.Still), command_queue)
        ship_positions += [ship.position]

def just_move (game, current_pos, destination):
    resultMoves = game.game_map.get_unsafe_moves(current_pos, destination)
    #logging.info(f'{resultMoves}')
    if (not resultMoves):
        return Direction.Still
    else:
        return shortest_move(game, current_pos, destination, resultMoves)
    return Direction.Still

def already_swapped (ship, swap_counter):
    if swap_counter:
        for ship_id in swap_counter:
            if ship_id == ship.id:
                return True
    return False

def can_move (game, ship):
    if ship.position == game.me.shipyard.position:
        return True
    if game.game_map[ship.position].halite_amount * 0.1 < ship.halite_amount:
        return True
    return False

"""def just_move_around (game, pos, des):
    resultMoves = game.game_map.get_unsafe_moves(pos,des)
    if (not resultMoves):
        return Direction.Still
    else:
        """

def just_move_pos (game, current_pos, destination):
    resultMoves = game.game_map.get_unsafe_moves(current_pos, destination)
    if (not resultMoves):
        return current_pos.directional_offset(Direction.Still)
    else:
        for one_move in resultMoves:
            return current_pos.directional_offset(one_move)
    return current_pos.directional_offset(Direction.Still)

def ship_moves_here(game, pos, ship_positions, main_ship):
    if pos in ship_positions:
        return True
    for ship in game.me.get_ships():
        if ship.id != main_ship.id and ship.position == pos:
            return True
    return False

    '''def ship_moves_here(game, pos, main_ship):
    """for stuff, ship in sorted(game.me._ships.items()):
        if (ship.id != main_ship.id):
            for direction in Direction.get_all_cardinals() + [Direction.Still]:
                if ship.position.directional_offset(direction) == pos:
                    return True"""
    return False'''

def get_id_of_ship(game, pos):
    for ship in game.me.get_ships():
            if (ship.position == pos):
                #logging.info(f'got ship id: {ship.id}')
                return ship.id

def shortest_move (game, pos, des, moves):
    move = Direction.North
    for one_move in moves:
        if game.game_map.calculate_distance(pos.directional_offset(move), des) > game.game_map.calculate_distance(pos.directional_offset(one_move), des): 
            move = one_move
            #logging.info(f'{pos.directional_offset(move)}, and one move: {pos.directional_offset(one_move)}')
    return move

def append_to_queue(command, command_queue):
    if not command_queue:
        command_queue.append(command)
    else:    
        for one_command in command_queue:
            if (one_command[0] == 'm') and (command[2] in one_command):
                command_queue.remove(one_command)
        command_queue.append(command)
        


#return resultMoves[0]