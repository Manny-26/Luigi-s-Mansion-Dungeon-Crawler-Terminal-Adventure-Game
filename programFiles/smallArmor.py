import item

SMALL_ARMOR_SLOTS = 1

class smallArmor(item):
    def __init__(self):
        super().__init__("Small Armor", "Adds 1 armor slot.", "smallArmor", SMALL_ARMOR_SLOTS)

    def use(self, luigi):
        luigi.armor = min(luigi.armor + self.magnitude, 3)
        print(f"Used {self.name}! Armor slots: {luigi.armor}/3")