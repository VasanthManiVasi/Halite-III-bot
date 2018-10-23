#!/usr/bin/env python3
# Python 3.6

# Import the Halite SDK, which will let you interact with the game.
import hlt

# This library contains constant values.
from hlt import constants

# This library contains direction metadata to better interface with the game.
from hlt.positionals import Direction
#from hlt.positionals import Position

# This library allows you to generate random numbers.
import random

# Logging allows you to save messages for yourself. This is required because the regular STDOUT
#   (print statements) are reserved for the engine-bot communication.
import logging

import utils

""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()

#def swap_position (game, ship1, ship2, ship_moves):
    
maxx, maxy = utils.getMax(game)
lb, rb = utils.setBorders(game, maxx)
ship_status = {}
# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("MyPythonBot")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

""" <<<Game Loop>>> """

while True:
    
    # This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
    #   running update_frame().
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map

    # A command queue holds all the commands you will run this turn. You build this list up and submit it at the
    #   end of the turn.
    command_queue = []
    ship_moves = {}
    

    for ship in me.get_ships():
        if ship.id not in ship_moves:
            ship_moves[ship.id] = 'no move'
        
        if ship_moves[ship.id] =='done':
            continue
        
        if ship.id not in ship_status:
            ship_status[ship.id] = "exploring"

        if ship_status[ship.id] == "returning":
            if ship.position == me.shipyard.position:
                ship_status[ship.id] = "exploring"
            else:
                logging.info(f'in else')
                nextPos = ship.position.directional_offset(utils.just_move(game, ship.position, me.shipyard.position))
                logging.info(f'next position; {nextPos}')
                if (utils.is_occupied_by_me(game, nextPos)):
                    logging.info(f'occupied by me')    
                    next_ship = me.get_ship(utils.get_id_of_ship(game, nextPos))
                    ship.move(utils.just_move(game, ship.position, next_ship.position))
                    next_ship.move(utils.just_move(game, next_ship.position, ship.position))
                    ship_moves[ship.id] = 'done'
                    ship_moves[next_ship.id] = 'done'
                
                    #swap_position(game, ship, , ship_moves)
                    logging.info(f'swapped')
                    continue
                else:
                    move = game_map.naive_navigate(ship, me.shipyard.position)
                    #move = utils.move_to_pos(game, ship.position, me.shipyard.position)
                    command_queue.append(ship.move(move))
                    continue
        elif ship.is_full:
            ship_status[ship.id] = "returning"
            
        logging.info("Ship {} has {} halite.".format(ship.id, ship.halite_amount))

        if ((game_map[me.shipyard.position].is_occupied) and (game_map[me.shipyard.position].ship.owner != me.id)):
            if me.halite_amount >= constants.SHIP_COST:
                command_queue.append(me.shipyard.spawn())
                break
            else:
                command_queue.append(ship.move(utils.move_to_pos(game, ship.position, me.shipyard.position)))
                continue

        if game_map[ship.position].halite_amount < 50 or ship.is_full:
            maxPos = utils.getNearestMaxHalitePosition(game, lb, rb, maxy, ship.position)
            #ayyy look new param for nearest maxhalite pos that is ship.postition
            command_queue.append(#ship.move(utils.move_to_pos(game, ship.position, maxPos)))
                ship.move(game_map.naive_navigate(ship, maxPos)))
                #ship.move(random.choice(['s','e','w','n'])))
        else:
            command_queue.append(ship.stay_still())
        
        ship_moves[ship.id] = 'done'

    # If you're on the first turn and have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though.
    if ((game.turn_number >= 1 and game.turn_number < 250)and (me.halite_amount >= constants.SHIP_COST * 2) and (not game_map[me.shipyard].is_occupied) or (not me.get_ships())):
        command_queue.append(game.me.shipyard.spawn())
    
    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)

