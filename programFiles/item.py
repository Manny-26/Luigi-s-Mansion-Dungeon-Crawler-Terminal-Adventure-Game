# This is the item class.
# Each item has a name, description, and item type.
# Items are used to represent the various objects that can be added to Luigi's inventory.
# Name and description are strings detailing the item name and description.
# item type is a string that represents the type of item (e.g. smallHeart, largeHeart, smallArmor, largeArmor).
# magntude is an integer that represents the magnitude of the item (e.g. how much health it restores or how much armor it provides).

class item:
    def __init__(self, name, description, itemType, magnitude):
        self.name = name
        self.description = description
        self.itemType = itemType
        self.magnitude = magnitude

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getItemType(self):
        return self.itemType

    def getMagnitude(self):
        return self.magnitude

    def setName(self, name):
        self.name = name;

    def setMagnitude(self, magnitude):
        self.magnitude = magnitude

    def setDescription(self, description):
        self.description = description

    def setItemType(self, itemType):
        self.itemType = itemType

    def use(self, player):
        """Apply this item to a player; concrete item classes define the effect."""
        raise NotImplementedError(f"{type(self).__name__} must implement use().")
