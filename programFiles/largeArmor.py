import item

LARGE_ARMOR_SLOTS = 3

class largeArmor(item):
    def __init__(self):
        super().__init__("Large Armor", "Fills all armor slots.", "largeArmor", LARGE_ARMOR_SLOTS)

    def use(self, player):
        player.armor = min(player.armor + self.magnitude, player.maxArmorSlots)
        print(f"Used {self.name}! Armor slots: {player.armor}/{player.maxArmorSlots}")