#!/usr/bin/env python3
# Python 3.6

# Import the Halite SDK, which will let you interact with the game.
import hlt

# This library contains constant values.
from hlt import constants

# This library contains direction metadata to better interface with the game.
from hlt.positionals import Direction

# This library allows you to generate random numbers.
import random

# Logging allows you to save messages for yourself. This is required because the regular STDOUT
#   (print statements) are reserved for the engine-bot communication.
import logging

import utils

""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()

#cheesePos = game.players[1].shipyard.position
cheesePos = utils.cheesePosition(game)

'''logging.info(f'cheese position = {cheesePos}')
logging.info(f'{game.players}')
logging.info(f'{game.players[0]}')
logging.info(f'{game.players[1].shipyard}')
utils.display_stuff(game)'''

# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("cheeserteaser")

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

    for ship in me.get_ships():

        logging.info('Ship {} has {} halite'.format(ship.id, ship.halite_amount))
        # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
        #   Else, collect halite.
        if (ship.position != cheesePos):
            if game_map[ship.position].halite_amount < constants.MAX_HALITE / 100 or ship.is_full:
                    utils.append_to_queue(ship.move(utils.move_to_pos(game, ship.position, cheesePos)), command_queue)
                    #ship.move(game_map.get_unsafe_moves(ship.position, cheesePos)[0]))
                    #ship.stay_still()
        else:
            command_queue.append(ship.stay_still())

    # If the game is in the first 200 turns and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though - the ships will collide.

    if (game.turn_number <= 1 or not me.get_ships()): 
       command_queue.append(me.shipyard.spawn())

    #logging.info('type of structure: {}'.format(game_map[me.shipyard.position].structure_type))

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)

