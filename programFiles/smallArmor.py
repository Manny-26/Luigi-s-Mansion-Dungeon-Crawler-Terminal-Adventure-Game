from item import item

SMALL_ARMOR_SLOTS = 1
SMALL_ARMOR_DURABILITY = 3

class smallArmor(item):
    def __init__(self):
        super().__init__(
            "Small Armor",
            "Halves damage from the next 3 ghost attacks.",
            "smallArmor",
            SMALL_ARMOR_SLOTS,
        )
        self.durability = SMALL_ARMOR_DURABILITY 

    def use(self, player):
        print(f"{self.name} equips automatically and has {self.durability} hits remaining.")
        return False
