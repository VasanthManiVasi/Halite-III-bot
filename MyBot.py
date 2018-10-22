#!/usr/bin/env python3

# Import the Halite SDK, which will let you interact with the game.
import hlt
from hlt import constants

import random
import logging
import utils

# This game object contains the initial game state.
game = hlt.Game()
ship_status = {}
maxx, maxy = utils.getMax(game)
lb, rb = utils.setBorders(game, maxx)
#logging.info('lb = {}, rb = {}'.format(lb, rb))

# Respond with your name.
game.ready("TheMadMan")

while True:
    # Get the latest game state.
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map

    # A command queue holds all the commands you will run this turn.
    command_queue = []

    for ship in me.get_ships():
        # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
        #   Else, collect halite.
        if ship.id not in ship_status:
            ship_status[ship.id] = "exploring"

        if ship_status[ship.id] == "returning":
            if ship.position == me.shipyard.position:
                ship_status[ship.id] = "exploring"
            else:
                dropoffs = me.get_dropoffs()
                if (dropoffs):
                    tndrop = []
                    for dropoff in dropoffs:
                        tndrop.append(game_map.calculate_distance(ship.position, dropoff.position))
                    tndrop.sort(reverse = True)
                    move = game_map.naive_navigate(ship, tndrop[0])
                else:
                    move = game_map.naive_navigate(ship, me.shipyard.position)
                command_queue.append(ship.move(move))
                continue
        elif ship.is_full:
            ship_status[ship.id] = "returning"
            
        logging.info("Ship {} has {} halite.".format(ship.id, ship.halite_amount))

        if game_map[ship.position].halite_amount < constants.MAX_HALITE / 95 or ship.is_full:
            maxPos = utils.getNearestMaxHalitePosition(game, lb, rb, maxy, ship.position)
            #ayyy look new param for nearest maxhalite pos that is ship.postition
            command_queue.append(
                ship.move(game_map.naive_navigate(ship, maxPos)))
                #ship.move(random.choice(['s','e','w','n'])))
        else:
            command_queue.append(ship.stay_still())

    # If you're on the first turn and have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though.
    if ((game.turn_number >= 1 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied) or (not me.get_ships())):
        command_queue.append(game.me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)