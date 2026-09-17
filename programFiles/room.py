# This class represents a room in the game. It contains information about the room's name, floor, descriptions, and interactable objects.
# roomName is a string that represents the name of the room.
# floor is an integer that represents the floor the room is on.
# darkDescription is a string that represents the description of the room when it is dark. This is shown to the player while the room is not cleared.
# litDescription is a string that represents the description of the room when it is lit. This is shown to the player after the room is cleared.
# interactableObjects is a dictionary that contains information about the objects in the room that the player can interact with. 
# - The keys of the dictionary are the names of the objects
# - The values are dictionaries that contain information about the object, which include:
# -- isSearched is a boolean that represents whether the object has been searched by the player.
# -- outcome is a string that represents the outcome of searching the object. This can be money, a consumable item, or a ghost.

from ghost import ghost

class room:
    def __init__(self, roomName, floor, darkDescriptiion, litDescription, interactableObjects):

        # roomName is a string that represents the name of the room.
        #
        # floor is an integer that represents the floor the room is on.
        #
        # darkDescription is a string that represents the description of the room when it is dark. It is displayed to the player while the room is not cleared.
        # litDescription is a string that represents the description of the room when it is lit. It is displayed to the player after the room is cleared.
        # interactableObjects is a dictionary that contains information about the objects in the room that the player can interact with.
        # - The keys of the dictionary are the names of the objects
        # - The values are dictionaries that contain information about the object, which include:
        # -- isSearched is a boolean that represents whether the object has been searched by the
        # -- outcome is a string that represents the outcome of searching the object. This can be money, a consumable item, or a ghost.
        #
        # isCleared is a boolean that represents whether the room has been cleared by the player.
        # - A room is considered cleared when all the objects in the room have been searched.
        self.roomName = roomName
        self.floor = floor
        self.darkDescription = darkDescriptiion
        self.litDescription = litDescription
        self.interactableObjects = interactableObjects
        self.isCleared = False

    # This function returns the description of the room based on whether it is cleared or not.
    def getRoomDescription(self):
        if (self.isCleared):
            return self.litDescription
        else:
            return self.darkDescription

    # This function processes player inspection of an object in the room.
    # This function returns a dictionary containing the status of the inspection, 
    # a message to be displayed to the screen, 
    # and the outcome of the inspection (i.e item or ghost)
    def inspectObject(self, objectName):

        # If the object is not in the room, do nothing
        if (objectName not in self.interactableObjects):
            print(f"The is no {objectName} in this room.")
            return {
                "status": "error",
                "message": f"The is no {objectName} in this room.",
                "outcome": None
            }

        # Get the data for the object from the interactableObjects dictionary
        objectData = self.interactableObjects[objectName]

        # If the object has already been searched, do nothing
        if objectData["isSearched"]:
            return {
                "status": "empty",
                "message": f"You have already searched the {objectName}.",
                "outcome": None
            }

        # If the object has not been searched, mark it as searched.
        # A living ghost still prevents the room from being cleared.
        objectData["isSearched"] = True
        self.isRoomCleared()

        # return the outcome of the search
        return {
            "status": "success",
            "message": f"You searched the {objectName}.",
            "outcome": objectData["outcome"]
        }

    # This function checks if the room is cleared
    # If all the objects have been searched, the room is cleared
    # otherwise, the room is not cleared
    def isRoomCleared(self):

        # Every object must be searched, and every revealed ghost must be
        # defeated, before the room can be cleared.
        for objectData in self.interactableObjects.values():
            if not objectData["isSearched"]:
                self.isCleared = False
                return False

            outcome = objectData.get("outcome")
            if isinstance(outcome, ghost) and outcome.health > 0:
                self.isCleared = False
                return False

        # if all the objects have been searched, set the isCleared attribute to True
        self.isCleared = True
        return True




        

        
