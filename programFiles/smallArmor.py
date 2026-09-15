import item

SMALL_ARMOR_SLOTS = 1

class smallArmor(item):
    def __init__(self):
        super().__init__("Small Armor", "Adds 1 armor slot.", "smallArmor", SMALL_ARMOR_SLOTS)

    def use(self, player):
        player.armor = min(player.armor + self.magnitude, player.maxArmorSlots)
        print(f"Used {self.name}! Armor slots: {player.armor}/{player.maxArmorSlots}")