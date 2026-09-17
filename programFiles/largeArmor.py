from item import item

LARGE_ARMOR_SLOTS = 3
LARGE_ARMOR_DURABILITY = 5

class largeArmor(item):
    def __init__(self):
        super().__init__(
            "Large Armor",
            "Halves damage from the next 5 ghost attacks.",
            "largeArmor",
            LARGE_ARMOR_SLOTS,
        )
        self.durability = LARGE_ARMOR_DURABILITY

    def use(self, player):
        print(f"{self.name} equips automatically and has {self.durability} hits remaining.")
        return False
