import item

LARGE_ARMOR_SLOTS = 3

class largeArmor(item):
    def __init__(self):
        super().__init__("Large Armor", "Fills all armor slots.", "largeArmor", LARGE_ARMOR_SLOTS)

    def use(self, luigi):
        luigi.armor = 3
        print(f"Used {self.name}! Armor fully restored: {luigi.armor}/3")