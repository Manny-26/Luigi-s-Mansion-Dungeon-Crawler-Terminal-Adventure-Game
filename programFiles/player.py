"""Shared behavior for playable characters.
##"""

import random

from character import character

MAX_HEALTH = 100
ITEM_ARRAY_SIZE = 3


class player(character):
    """Base class for Luigi, Mario, and future playable characters."""

    def __init__(self, name, health, skill):
        super().__init__(name, health, skill)
        self.inventory = {
            "hearts": {
                "smallHearts": [None] * ITEM_ARRAY_SIZE,
                "largeHearts": [None] * ITEM_ARRAY_SIZE,
            },
            "armor": {
                "smallArmor": [None] * ITEM_ARRAY_SIZE,
                "largeArmor": [None] * ITEM_ARRAY_SIZE,
            },
            # Captured ghosts are trophies, not consumable inventory slots.
            "ghosts": {"capturedGhosts": []},
        }

    @property
    def health(self):
        """Return current health."""
        return self._health

    @health.setter
    def health(self, value):
        """Keep health within the valid 0–100 range on every assignment."""
        self._health = max(0, min(MAX_HEALTH, value))

    def placeInSlot(self, foundItem):
        if foundItem.itemType == "capturedGhost":
            self.inventory["ghosts"]["capturedGhosts"].append(foundItem)
            print(f"{foundItem.name} was added to the ghost collection.")
            return True

        locations = {
            "smallHeart": ("hearts", "smallHearts"),
            "largeHeart": ("hearts", "largeHearts"),
            "smallArmor": ("armor", "smallArmor"),
            "largeArmor": ("armor", "largeArmor"),
        }
        location = locations.get(foundItem.itemType)
        if location is None:
            print("Invalid item type.")
            return False

        slots = self.inventory[location[0]][location[1]]
        for index, storedItem in enumerate(slots):
            if storedItem is None:
                slots[index] = foundItem
                return True

        print(f"No empty slots available for {foundItem.name}.")
        return False

    def addToInventory(self, foundItem):
        return self.placeInSlot(foundItem)

    @staticmethod
    def normalizeItemName(itemName):
        return "".join(letter for letter in itemName.lower() if letter.isalnum())

    def findInventoryItem(self, requestedName, includeGhosts=False):
        normalizedRequest = self.normalizeItemName(requestedName)
        for categoryName in ("hearts", "armor"):
            for slots in self.inventory[categoryName].values():
                for index, storedItem in enumerate(slots):
                    if storedItem is None:
                        continue
                    validNames = {
                        self.normalizeItemName(storedItem.name),
                        self.normalizeItemName(storedItem.itemType),
                        self.normalizeItemName(storedItem.name + "s"),
                    }
                    if normalizedRequest in validNames:
                        return storedItem, slots, index

        if includeGhosts:
            for storedItem in self.inventory["ghosts"]["capturedGhosts"]:
                validNames = {
                    self.normalizeItemName(storedItem.name),
                    self.normalizeItemName(storedItem.itemType),
                    self.normalizeItemName(storedItem.name + "s"),
                }
                if normalizedRequest in validNames:
                    return storedItem, None, None

        return None

    def inspectInventoryItem(self, requestedName):
        """Print and return the description of an item in the inventory."""
        entry = self.findInventoryItem(requestedName, includeGhosts=True)
        if entry is None:
            return None

        inventoryItem = entry[0]
        print(f"\n{inventoryItem.name}: {inventoryItem.description}\n")
        return inventoryItem

    def useInventoryItem(self, requestedName):
        entry = self.findInventoryItem(requestedName)
        if entry is None:
            print(f"You do not have '{requestedName}' in your inventory.")
            return False

        inventoryItem, slots, index = entry
        if inventoryItem.use(self):
            slots[index] = None
            return True
        return False

    def getInventory(self):
        print(f"\n{self.name}'s Inventory:\n")
        print("Hearts:")
        print("  Small Hearts: " + self.describeItemSlots("hearts", "smallHearts"))
        print("  Large Hearts: " + self.describeItemSlots("hearts", "largeHearts"))
        print("Armor:")
        print("  Small Armor: " + self.describeArmorSlots("smallArmor"))
        print("  Large Armor: " + self.describeArmorSlots("largeArmor"))
        ghosts = self.inventory["ghosts"]["capturedGhosts"]
        print(f"Captured Ghosts ({len(ghosts)}):")
        print("  " + (", ".join(ghost.name for ghost in ghosts) or "None"))
        print("\nUse an item with 'use [item name]'.\n")

    def describeItemSlots(self, category, itemType):
        return str([
            storedItem.name if storedItem is not None else "Empty"
            for storedItem in self.inventory[category][itemType]
        ])

    def describeArmorSlots(self, armorType):
        descriptions = []
        for armorItem in self.inventory["armor"][armorType]:
            if armorItem is None:
                descriptions.append("Empty")
            else:
                descriptions.append(
                    f"{armorItem.name} ({armorItem.durability} hits remaining)"
                )
        return str(descriptions)

    def findActiveArmor(self):
        defaultDurability = {"smallArmor": 3, "largeArmor": 5}
        for armorType in ("smallArmor", "largeArmor"):
            slots = self.inventory["armor"][armorType]
            for index, armorItem in enumerate(slots):
                if armorItem is None:
                    continue
                if not hasattr(armorItem, "durability"):
                    armorItem.durability = defaultDurability[armorType]
                if armorItem.durability < 1:
                    slots[index] = None
                    continue
                return armorItem, slots, index
        return None

    def getArmorStatus(self):
        activeArmor = self.findActiveArmor()
        if activeArmor is None:
            return "None"
        return f"{activeArmor[0].name} ({activeArmor[0].durability} hits remaining)"

    def addHealth(self, amount):
        previousHealth = self.health
        self.health += amount
        return self.health - previousHealth

    def takeDamage(self, amount):
        activeArmor = self.findActiveArmor()
        damage = amount
        if activeArmor is not None:
            armorItem, slots, index = activeArmor
            damage = (amount + 1) // 2
            armorItem.durability -= 1
            print(f"{armorItem.name} reduces the incoming damage from {amount} to {damage}.")
            if armorItem.durability < 1:
                print(f"{armorItem.name} has broken and was removed from your inventory.")
                slots[index] = None
        return super().takeDamage(damage)

    def attack(self, enemy):
        return self.vacuumAttack(enemy)

    def vacuumAttack(self, enemy):
        roll = 1 #random.randint(1, 20)
        print(f"{self.name} rolls a {roll}!")

        if roll == 1:
            damageDealt = enemy.takeDamage(enemy.health)
            print(f"Perfect catch! {enemy.name} is sucked in instantly!")
            return damageDealt

        damage = self.vacuumBaseDamage + (
            self.skill * random.randint(1, self.vacuumMaxScale)
        )
        damageDealt = enemy.takeDamage(damage)
        print(f"{self.name} attacks {enemy.name} for {damageDealt} damage!")
        return damageDealt
