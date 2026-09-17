


import json
from pathlib import Path
from level import level
from luigi import luigi
from ghost import ghost
from item import item

MAX_LEVEL_COUNT = 4
class game:
    def __init__(self, player=None):
        self.state = "EXPLORATION"
        self.isRunning = True
        self.player = player if player is not None else luigi()
        self.currentLevelNumber = 1
        self.currentLevel = None
        self.currentRoomName = None
        self.activeGhost = None
        self.activeGhostObjectName = None
        self.saveId = None
        self.saveName = None

    # This function initializes the game and loads the first level
    def start(self):
        # Print the game welcome message
        print("==================================================")
        print("      LUIGI'S MANSION: TERMINAL ADVENTURE         ")
        print("==================================================")
        print()

        self.loadLevel(self.currentLevelNumber)

    # This function loads the level blueprints from the associated JSON file and initializes the level object
    def loadLevel(self, levelNumber):
        #TO-DO: Create the JSON files that contain the rooms for each level
        fileName = Path(__file__).with_name(f"level_{levelNumber}_rooms.json")

        # try to open the JSON file and load the level data
        try:
            with fileName.open("r", encoding="utf-8") as file:
                data = json.load(file)
                levelName = data["levelName"]
                roomBlueprints = data["rooms"]
                numGhosts = data["numGhosts"]
                numItems = data["numItems"]

                self.currentLevel = level(levelName, roomBlueprints, numGhosts, numItems)

                self.currentRoomName = list(self.currentLevel.rooms.keys())[0]
                print(f"\n[Entering Floor {levelNumber}: {self.currentLevel.levelName}]")
        except FileNotFoundError:
            print(f"Error: Level {levelNumber} file not found.")
            self.isRunning = False

    def runGameLoop(self):
        while self.isRunning:

            currentRoom = self.currentLevel.rooms[self.currentRoomName]

            if self.player.health <= 0:
                self.state = "GAME_OVER"


            if self.state == "EXPLORATION":
                self.processExplorationState(currentRoom)
            elif self.state == "COMBAT":
                self.processCombatTurn()
            elif self.state == "GAME_OVER":
                print("\nYou got Ghosted! Game Over!")
                self.isRunning = False
            elif self.state == "VICTORY":
                print("\nCongratulations! You have now cleared the mansion!")
                self.isRunning = False

    def processExplorationState(self, currentRoom):

        print("\n--------------------------------------------------")
        print(
            f"Location: {currentRoom.roomName} (Floor {currentRoom.floor}) | "
            f"{self.player.name} HP: {self.player.health} | "
            f"Armor: {self.player.getArmorStatus()}"
        )
        print()
        print(currentRoom.getRoomDescription())

        print("\nObjects you can inspect:")
        for objectName, objectData in currentRoom.interactableObjects.items():
            status = "(Searched)" if objectData["isSearched"] else "(Unsearched)"
            print(f" - {objectName} {status}")
            
        # Get player input
        userInput = input(
            "\nWhat would you like to do? "
            "(e.g., 'inspect [object]', 'map', 'move [room]', 'inventory', "
            "'use [item]', 'save', 'quit'): "
        ).strip().lower()
        parts = userInput.split(" ", 1)
        
        verb = parts[0] if len(parts) > 0 else ""
        noun = parts[1] if len(parts) > 1 else ""
        
        # Command Parsing
        if verb == "quit":
            print("\nExiting game. Goodbye!\n")
            self.isRunning = False
        
        # Loops back to print room details    
        elif verb == "look":
            pass 
            
        elif verb == "inventory":
            self.player.getInventory()

        elif verb == "map":
            self.displayMap()

        elif verb == "use":
            if not noun:
                print("\nSpecify an item to use.\n")
                return
            self.player.useInventoryItem(noun)

        elif verb == "save":
            self.save()
            
        elif verb == "inspect":
            if not noun:
                print("\nSpecify an object.\n")
                
            # Call the inspectObject method from the room class
            result = currentRoom.inspectObject(noun)
            print(f"\n{result['message']}")
            
            # Handle outcome if something was found successfully
            if result["status"] == "success":
                outcome = result["outcome"]
                
                # Check if the outcome is a Ghost object (not a string or None)
                if isinstance(outcome, ghost):
                    self.activeGhost = outcome
                    self.activeGhostObjectName = noun
                    self.state = "COMBAT"
                    print(f"\nA wild {self.activeGhost.getName()} appears! Prepare for battle!")
                    
                # Check if the outcome is an Item object / string 
                elif isinstance(outcome, item):
                    print(f"\nYou found an item: {outcome.name}!")
                    # Use Luigi's built-in inventory routing method from luigi.py
                    self.player.addToInventory(outcome)
                    
            # Check if clearing this object finished the room
            if (
                result["status"] == "success"
                and currentRoom.isCleared
                and self.state != "COMBAT"
            ):
                self.completeClearedRoom(currentRoom)
                
        elif verb == "move" or verb == "go":
            if not noun:
                print("\nSpecify a room name. Type 'map' to see the available rooms.\n")
                return
                
            targetRoom = noun.title()
            if targetRoom in self.currentLevel.rooms:
                self.currentRoomName = targetRoom
                print(f"\nYou walk into the {targetRoom}.\n")
            else:
                print(
                    f"\nYou cannot reach '{noun}' from here or it doesn't exist. "
                    "Type 'map' to see the available rooms.\n"
                )
        else:
            print(
                "\nUnknown command. Try 'inspect [object]', 'map', "
                "'move [room]', 'inventory', 'use [item]', 'save', "
                "'look', or 'quit'.\n"
            )

    def displayMap(self):
        """Display every room currently reachable on this floor."""
        print("\n==================================================")
        print(f"MAP: {self.currentLevel.levelName}")
        print("==================================================")
        print("All rooms on this floor are available to explore:\n")

        for roomName, roomData in self.currentLevel.rooms.items():
            currentMarker = "->" if roomName == self.currentRoomName else "  "
            locationStatus = "CURRENT" if roomName == self.currentRoomName else "AVAILABLE"
            clearStatus = "CLEARED" if roomData.isCleared else "UNCLEARED"
            print(f"{currentMarker} {roomName} [{locationStatus} | {clearStatus}]")

        print("\nMove with: move [room name]")
        print("Example: move library\n")

    def processCombatTurn(self):
        if self.activeGhost is None:
            self.state = "EXPLORATION"
            return

        print("\n*** BATTLE MODE ***")
        print(
            f"{self.player.name} HP: {self.player.health} | "
            f"Armor: {self.player.getArmorStatus()} | "
            f"{self.activeGhost.name} HP: {self.activeGhost.health}"
        )

        choice = input(
            "\nChoose action: [1] Vacuum Attack [2] Run "
            "[3] Use Item [4] Save [5] Inventory [6] Map: "
        ).strip().lower()

        if choice in {"4", "save"}:
            self.save()
            return

        if choice in {"5", "inventory"}:
            self.player.getInventory()
            return

        if choice in {"6", "map"}:
            self.displayMap()
            return

        if choice == "3":
            requestedItem = input("Which item would you like to use? ").strip()
            itemWasUsed = self.player.useInventoryItem(requestedItem)
            if itemWasUsed:
                self.processGhostCounterattack()
            return

        if choice.startswith("use "):
            requestedItem = choice.split(" ", 1)[1]
            itemWasUsed = self.player.useInventoryItem(requestedItem)
            if itemWasUsed:
                self.processGhostCounterattack()
            return

        if choice in {"1", "attack", "vacuum", "vacuum attack"}:
            print("You flash the ghost with your Poltergust and pull!")
            self.player.attack(self.activeGhost)

            if self.activeGhost.health <= 0:
                defeated_ghost_name = self.activeGhost.name
                print(f"You captured the {defeated_ghost_name}!")
                self.finishCombat()
                return

            self.processGhostCounterattack()

        elif choice in {"2", "run", "flee"}:
            print("You managed to scramble away! The ghost returns to its hiding spot.")
            self.returnGhostToHidingSpot()
            self.activeGhost = None
            self.activeGhostObjectName = None
            self.state = "EXPLORATION"
        else:
            print("\nInvalid choice.\n")

    def processGhostCounterattack(self):
        """Allow the active ghost to attack after the player's turn."""
        if self.activeGhost is None or self.activeGhost.health <= 0:
            return

        print(f"\nThe {self.activeGhost.name} counterattacks!")
        self.activeGhost.attack(self.player)

        if self.player.health <= 0:
            self.state = "GAME_OVER"

    def finishCombat(self):
        """End a won battle and process any resulting room completion."""
        currentRoom = self.currentLevel.rooms[self.currentRoomName]
        hidingSpotName = getattr(self, "activeGhostObjectName", None)

        defeatedGhost = self.activeGhost
        if defeatedGhost is not None:
            self.player.addToInventory(defeatedGhost.toItem())

        if hidingSpotName in currentRoom.interactableObjects:
            currentRoom.interactableObjects[hidingSpotName]["outcome"] = None

        currentRoom.isRoomCleared()

        self.activeGhost = None
        self.activeGhostObjectName = None
        self.state = "EXPLORATION"

        if currentRoom.isCleared:
            self.completeClearedRoom(currentRoom)

    def returnGhostToHidingSpot(self):
        """Make a fled encounter available to discover and fight again."""
        currentRoom = self.currentLevel.rooms[self.currentRoomName]
        hidingSpotName = getattr(self, "activeGhostObjectName", None)

        if hidingSpotName in currentRoom.interactableObjects:
            currentRoom.interactableObjects[hidingSpotName]["isSearched"] = False
            currentRoom.isCleared = False

    def completeClearedRoom(self, currentRoom):
        print(
            f"\n* Click * The lights in {currentRoom.roomName} flicker on! "
            "The room is cleared.\n"
        )
        self.checkLevelProgression()

    def save(self, filePath=None):
        """Save the current game into its existing save slot."""
        # Imported here to avoid the module-level game/game_funcs import cycle.
        from game_funcs import SaveFileError, save_game

        previousSaveId = getattr(self, "saveId", None)
        try:
            self.saveId = save_game(
                self,
                save_id=previousSaveId,
                file_path=filePath,
            )
        except (SaveFileError, TypeError) as error:
            self.saveId = previousSaveId
            print(f"\nUnable to save the game: {error}\n")
            return False

        print(f"\nGame '{self.saveName}' saved successfully.\n")
        return True
                

    def checkLevelProgression(self):

        allRoomsClear = all(r.isCleared for r in self.currentLevel.rooms.values())

        if allRoomsClear:
            print(f"\n***LEVEL {self.currentLevelNumber} COMPLETE! ***")
            self.currentLevelNumber += 1

            if self.currentLevelNumber > MAX_LEVEL_COUNT:
                self.state = "VICTORY"

            else:
                print("A key drops from the ceiling! I wonder where this leads to?")
                self.loadLevel(self.currentLevelNumber)
