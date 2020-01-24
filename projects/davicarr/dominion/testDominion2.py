# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 15:42:42 2015

@author: davicarr
"""

# import Dominion file
import importlib

Dominion = importlib.import_module('Dominion')
if Dominion is None:
    print("can't find tbe Dominion module")

testUtility = importlib.import_module('testUtility')
if testUtility is None:
    print("can't find tbe testUtility module")

import random
from collections import defaultdict

# Get player names
player_names = testUtility.getPlayerNames()

# number of curses and victory cards
if len(player_names) > 2:
    nV=0 #This is the introduced test scenario issue; nV = 12
else:
    nV=0 ##This is the introduced test scenario issue; nV = 8
nC = -10 + 10 * len(player_names)

# Define box
box = testUtility.getBoxes()

# Pick 10 cards from box to be in the supply.
boxlist = [k for k in box]
random.shuffle(boxlist)
random10 = boxlist[:10]
supply = defaultdict(list, [(k, box[k]) for k in random10])

# Create a supply order based on card cost
supply_order = testUtility.getSupplyOrder()

# The supply always has these cards
base_supplies = testUtility.getSupplies(nV, nC)
for key in base_supplies:
    value = base_supplies[key]
    supply[key] = value

# initialize the trash
trash = []

# Costruct the Player objects
players = []
for name in player_names:
    if name[0] == "*":
        players.append(Dominion.ComputerPlayer(name[1:]))
    elif name[0] == "^":
        players.append(Dominion.TablePlayer(name[1:]))
    else:
        players.append(Dominion.Player(name))

# Play the game
turn = 0
while not Dominion.gameover(supply):
    turn += 1
    print("\r")
    for value in supply_order:
        print(value)
        for stack in supply_order[value]:
            if stack in supply:
                print(stack, len(supply[stack]))
    print("\r")
    for player in players:
        print(player.name, player.calcpoints())
    print("\rStart of turn " + str(turn))
    for player in players:
        if not Dominion.gameover(supply):
            print("\r")
            player.turn(players, supply, trash)

# Final score
dcs = Dominion.cardsummaries(players)
vp = dcs.loc['VICTORY POINTS']
vpmax = vp.max()
winners = []
for i in vp.index:
    if vp.loc[i] == vpmax:
        winners.append(i)
if len(winners) > 1:
    winstring = ' and '.join(winners) + ' win!'
else:
    winstring = ' '.join([winners[0], 'wins!'])

print("\nGAME OVER!!!\n" + winstring + "\n")
print(dcs)
