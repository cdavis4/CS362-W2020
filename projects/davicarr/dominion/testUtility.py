"""
Created on Tue Jan 15 15:42:42 2015

@author: davicarr
"""

import importlib
from collections import defaultdict

Dominion = importlib.import_module('Dominion')
if Dominion is None:
    print("can't find tbe Dominion module")

"""Global Variables"""

action_cards = ["Woodcutter","Smithy","Laboratory","Village","Festival","Market",
             "Chancellor","Workshop","Moneylender","Chapel","Cellar","Remodel",
             "Adventurer","Feast","Mine","Library","Gardens","Moat","Council Room",
                "Witch","Bureaucrat","Militia","Spy","Thief","Throne Room"]

supply_cards = ["Copper","Silver","Gold","Estate","Duchy","Province","Curse"]


names = ["Annie","*Ben","*Carla"]


"""This is a box of the same card"""
class CardSet:
    def __init__(self,type,value):
        self.card = getattr(Dominion,type)()
        self.num = value
    def getSet(self):
        return [self.card] * self.num

#standalone scripts
def getPlayerNames():
    return names

def getSupplies(nV,nC):
    supplies = {}
    for card in supply_cards:
        if card is "Copper":
            #Aware if a card has a space in name will fail
            players = getPlayerNames()
            player_number = len(players)
            value = 60-player_number * 7
            supplies[card] = CardSet(card,value).getSet()
        elif card is "Silver":
            supplies[card] = CardSet(card, 40).getSet()
        elif card is "Gold":
            supplies[card] = CardSet(card, 30).getSet()
        elif card is "Curse":
            supplies[card] = CardSet(card, nC).getSet()
        else:
            supplies[card] = CardSet(card, nV).getSet()
    return supplies

def defineCostArray(array,cost,value,card_name):
    if cost == value:
        array.append(card_name)

def getSupplyOrder():
    cost_dict = {}
    zero= []
    two = []
    three = []
    four = []
    five = []
    six = []
    eight = []
    complete_list = supply_cards + action_cards
    for type in complete_list:
        type_function = type.replace(" ", "_")
        card = getattr(Dominion,type_function)()
        cost = card.cost
        name = card.name
        #define card arrays for each cost
        defineCostArray(zero,cost,0, name)
        defineCostArray(two, cost, 2, name)
        defineCostArray(three, cost, 3, name)
        defineCostArray(four, cost, 4, name)
        defineCostArray(five, cost, 5, name)
        defineCostArray(six, cost, 6, name)
        defineCostArray(eight, cost, 8, name)
    #add card arrays to appropriate key in dict
    cost_dict[0] = zero
    cost_dict[2] = two
    cost_dict[3] = three
    cost_dict[4] = four
    cost_dict[5] = five
    cost_dict[6] = six
    cost_dict[8] = eight
    return cost_dict


def getBoxes():
    box = {}
    for card in action_cards:
        card_function = card.replace(" ","_")
        box[card] = CardSet(card_function, 10).getSet()
    return box




