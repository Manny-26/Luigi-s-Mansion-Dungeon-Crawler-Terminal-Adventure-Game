# This class represents a level in the game.
# Each level has a name, a collection of rooms, a number of ghosts, and a number of items.
# levelName is a string that represents the name of the level.
# rooms is a dictionary that contains the rooms in the level.
# numGhostsTotal tracks the original ghost count for the door mechanic.
# roomBlueprints is a list of dictionaries provided by a JSON file.

import random

from room import room
from goldGhost import goldGhost
from purplePuncher import purplePuncher
from smallHeart import smallHeart
from largeHeart import largeHeart
from smallArmor import smallArmor
from largeArmor import largeArmor


class level:
    def __init__(self, levelName, roomBlueprints, numGhosts, numItems):
        self.levelName = levelName
        self.rooms = {}
        self.numGhostsTotal = numGhosts   # saved before distributeEntities decrements it
        self.numGhosts = numGhosts
        self.numItems = numItems
        self.isCleared = False

        self.buildRooms(roomBlueprints)
        self.distributeEntities()

    def buildRooms(self, roomBlueprints):
        for roomData in roomBlueprints:
            roomName               = roomData["name"]
            roomFloor              = roomData["floor"]
            roomDarkDescription    = roomData["darkDescription"]
            roomLitDescription     = roomData["litDescription"]
            roomInteractableObjects = roomData["interactableObjects"]

            newRoom = room(roomName, roomFloor, roomDarkDescription, roomLitDescription, roomInteractableObjects)
            self.rooms[roomName] = newRoom

    def distributeEntities(self):
        # Build a flat list of every interactable object across all rooms
        hidingSpots = []
        for roomName, roomData in self.rooms.items():
            for interactableName in roomData.interactableObjects.keys():
                hidingSpots.append({
                    "roomName": roomName,
                    "interactableName": interactableName
                })

        random.shuffle(hidingSpots)

        # Place ghosts — alternate between goldGhost and purplePuncher
        while self.numGhosts > 0 and len(hidingSpots) > 0:
            spot = hidingSpots.pop()
            targetRoom = self.rooms[spot["roomName"]]

            if self.numGhosts % 2 == 0:
                targetRoom.interactableObjects[spot["interactableName"]]["outcome"] = goldGhost()
            else:
                targetRoom.interactableObjects[spot["interactableName"]]["outcome"] = purplePuncher()

            self.numGhosts -= 1

        # Item pool — weighted so smaller items appear more often
        itemPool = (
            [smallHeart] * 4 +   # most common
            [largeHeart] * 3 +   # common
            [smallArmor] * 2 +   # uncommon
            [largeArmor] * 1     # rare
        )

        # Place items as actual objects so addToInventory can use them
        while self.numItems > 0 and len(hidingSpots) > 0:
            spot = hidingSpots.pop()
            targetRoom = self.rooms[spot["roomName"]]

            itemClass = random.choice(itemPool)
            targetRoom.interactableObjects[spot["interactableName"]]["outcome"] = itemClass()

            self.numItems -= 1
