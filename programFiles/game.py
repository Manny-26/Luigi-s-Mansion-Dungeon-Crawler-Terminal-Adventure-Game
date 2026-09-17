import json
from level import level
from luigi import luigi

ITEM_ARRAY_SIZE = 3


class game:
    def __init__(self, player=None):
        self.state = "EXPLORATION"
        self.isRunning = True
        self.player = player if player is not None else luigi()
        self.currentLevelNumber = 1
        self.currentLevel = None
        self.currentRoomName = None
        self.activeGhost = None

    def start(self):
        print("==================================================")
        print("      LUIGI'S MANSION: TERMINAL ADVENTURE         ")
        print("==================================================")
        self.loadLevel(self.currentLevelNumber)

    def loadLevel(self, levelNumber):
        fileName = f"level_{levelNumber}_rooms.json"
        try:
            with open(fileName, "r") as file:
                data = json.load(file)
                levelName     = data["levelName"]
                roomBlueprints = data["rooms"]
                numGhosts     = data["numGhosts"]
                numItems      = data["numItems"]

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
                print("\nCongratulations! You have cleared the mansion!")
                self.isRunning = False

    def processExplorationState(self, currentRoom):
        print("\n--------------------------------------------------")
        print(f"Location: {currentRoom.roomName} (Floor {currentRoom.floor}) | {self.player.name} HP: {self.player.health} | Armor: {self.player.armor}/{self.player.maxArmorSlots}")
        print(currentRoom.getRoomDescription())

        print("\nObjects you can inspect:")
        for objectName, objectData in currentRoom.interactableObjects.items():
            status = "(Searched)" if objectData["isSearched"] else "(Unsearched)"
            print(f" - {objectName} {status}")

        userInput = input("\nWhat would you like to do? (e.g., 'inspect [object]', 'move [room]', 'inventory', 'quit'): ").strip().lower()
        parts = userInput.split(" ", 1)

        verb = parts[0] if len(parts) > 0 else ""
        noun = parts[1] if len(parts) > 1 else ""

        if verb == "quit":
            print("Exiting game. Goodbye!")
            self.isRunning = False

        elif verb == "look":
            pass

        elif verb == "inventory":
            self.player.getInventory()

        elif verb == "inspect":
            if not noun:
                print("Specify an object.")
                return

            result = currentRoom.inspectObject(noun)
            print(f"\n{result['message']}")

            if result["status"] == "success":
                outcome = result["outcome"]

                # Door — check for captured ghosts
                if outcome == "door":
                    self.tryOpenDoor()

                # Ghost — start combat
                elif outcome is not None and not isinstance(outcome, str):
                    self.activeGhost = outcome
                    self.state = "COMBAT"
                    print(f"\nA wild {self.activeGhost.getName()} appears! Prepare for battle!")

                # Item — add to inventory
                elif outcome is not None:
                    print(f"You found a {outcome.name}!")
                    self.player.addToInventory(outcome)

            if currentRoom.isCleared:
                print(f"\n* Click * The lights in {currentRoom.roomName} flicker on! The room is cleared.")
                self.checkLevelProgression()

        elif verb in ("move", "go"):
            if not noun:
                print("Specify a room name.")
                return

            targetRoom = noun.title()
            if targetRoom in self.currentLevel.rooms:
                self.currentRoomName = targetRoom
                print(f"You walk into the {targetRoom}.")
            else:
                print(f"You cannot reach '{noun}' from here or it doesn't exist. Try again.")

        else:
            print("Unknown command. Try 'inspect [object]', 'move [room]', 'inventory', 'look', or 'quit'.")

    def processCombatTurn(self):
        print("\n*** BATTLE MODE ***")
        print(f"{self.player.name} HP: {self.player.health} | Armor: {self.player.armor}/{self.player.maxArmorSlots}")
        print(f"{self.activeGhost.name} HP: {self.activeGhost.health}")

        choice = input("Choose action: [1] Vacuum Attack  [2] Use Item  [3] Run: ").strip()

        if choice == "1":
            print(f"\n{self.player.name} charges up the Poltergust!")
            self.player.vacuumAttack(self.activeGhost)

            if self.activeGhost.health <= 0:
                print(f"\n{self.activeGhost.name} has been defeated!")
                captured = self.activeGhost.toItem()
                self.player.addToInventory(captured)
                self.activeGhost = None
                self.state = "EXPLORATION"
            else:
                # Ghost survived — it attacks back
                print(f"\n{self.activeGhost.name} fights back!")
                self.activeGhost.punch(self.player)

        elif choice == "2":
            self.player.useItem()

        elif choice == "3":
            print(f"You scramble away! {self.activeGhost.name} looks tired...")
            self.activeGhost = None
            self.state = "EXPLORATION"

        else:
            print("Invalid choice.")

    def tryOpenDoor(self):
        ghostSlots = self.player.inventory["ghosts"]["capturedGhosts"]
        captured = [slot for slot in ghostSlots if slot is not None]
        needed = self.currentLevel.numGhostsTotal

        if len(captured) >= needed:
            print(f"The door rumbles open! {self.player.name} feeds the ghosts into the lock...")
            self.player.inventory["ghosts"]["capturedGhosts"] = [None] * ITEM_ARRAY_SIZE
            self.checkLevelProgression()
        else:
            remaining = needed - len(captured)
            print(f"The door won't budge. You need {remaining} more captured ghost(s).")

    def checkLevelProgression(self):
        allRoomsClear = all(r.isCleared for r in self.currentLevel.rooms.values())

        if allRoomsClear:
            print(f"\n*** LEVEL {self.currentLevelNumber} COMPLETE! ***")
            self.currentLevelNumber += 1

            if self.currentLevelNumber > 4:
                self.state = "VICTORY"
            else:
                print("A key drops from the ceiling! I wonder where this leads to?")
                self.loadLevel(self.currentLevelNumber)
