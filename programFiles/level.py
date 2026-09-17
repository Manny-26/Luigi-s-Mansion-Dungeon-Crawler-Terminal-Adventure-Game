# This class represents a level in the game
# Each level has a name, a collection of rooms, a number of ghosts, and a number of items.
# levelName is a string that represents the name of the level.
# rooms is a dictionary that contains the rooms in the level.
# - The keys of the dictionary are the names of the rooms
# - The values are room objects that contain information about the room.
# numGhosts is an integer that represents the number of ghosts in the level.
# numItems is an integer that represents the number of items in the level.

# roomBlueprints is a list of dictionaries provided by a JSON file


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
        self.numGhosts = numGhosts
        self.numItems = numItems
        self.isCleared = False

        # build the rooms in the level based on the roomBlueprints provided
        self.buildRooms(roomBlueprints)
        self.distributeEntities()

    # This function builds the rooms in the level based on the roomsBlueprints provided by the JSON file.
    # To separate the rooms for each level, each level will have an associated JSON file that contains the roomBlueprints for that level.
    def buildRooms(self, roomBlueprints):

        # for every room in the roomBlueprints provided by the associated level JSON File, create a room object and add it to the level's rooms dictionary.
        for roomData in roomBlueprints:

            # get the attributes of the current room
            roomName = roomData["name"]
            roomFloor = roomData["floor"]
            roomDarkDescription = roomData["darkDescription"]
            roomLitDescription = roomData["litDescription"]
            roomInteractableObjects = roomData["interactableObjects"]

            # instantiate a new room object with the attributes of the current room
            newRoom = room(roomName, roomFloor, roomDarkDescription, roomLitDescription, roomInteractableObjects)

            # add the new room to the level object's rooms dictionary
            # The key is the room's name
            # The value is the newly created room object
            self.rooms[roomName] = newRoom

    # This function distributes the ghosts and items in the level's rooms.
    # The ghosts and items are distributed randomly in the rooms' interactable objects.
    def distributeEntities(self):

        # create a list of all the interactable objects in the level's rooms
        hidingSpots = []

        # for every room in the level's rooms, add the room's interactable objects to the hidingSpots list
        for roomName, roomData in self.rooms.items():
            for interactableName in roomData.interactableObjects.keys():
                hidingSpots.append({
                    "roomName": roomName,
                    "interactableName": interactableName
                })

        # randomize the hidingSpots list so that the ghosts and items are distributed randomly
        random.shuffle(hidingSpots)

        # Place the ghosts into the rooms
        while self.numGhosts > 0 and len(hidingSpots) > 0:

            # grab a random hiding spot from the list of hiding spots
            spot = hidingSpots.pop()

            # get the room object for the room that contains the hiding spot
            targetRoom = self.rooms[spot["roomName"]]

            # choose a ghost to place in the hiding spot based on the number of ghosts remaining to be placed
            # easier ghosts are more likely to be placed in the level than harder ghosts
            # TO-DO: Add more ghost types to the game
            if self.numGhosts % 2 == 0:
                targetRoom.interactableObjects[spot["interactableName"]]["outcome"] = goldGhost()
            elif self.numGhosts % 2 == 1:
                targetRoom.interactableObjects[spot["interactableName"]]["outcome"] = purplePuncher()

            self.numGhosts -= 1

        # Place the items into the rooms
        while self.numItems > 0 and len(hidingSpots) > 0:

            # grab a random hiding spot from the list of hiding spots
            spot = hidingSpots.pop()

            # get the room object for the room that contains the hiding spot
            targetRoom = self.rooms[spot["roomName"]]

            # choose an item to place in the hiding spot based on the number of items remaining to be placed
            # more common items are more likely to be placed in the level than rarer items
            # TO-DO: Add more item types to the game
            match self.numItems % 4:
                case 0:
                    outcome = largeArmor()
                case 1:
                    outcome = largeHeart()
                case 2:
                    outcome = smallHeart()
                case 3:
                    outcome = smallArmor()

            targetRoom.interactableObjects[spot["interactableName"]]["outcome"] = outcome

            self.numItems -= 1
