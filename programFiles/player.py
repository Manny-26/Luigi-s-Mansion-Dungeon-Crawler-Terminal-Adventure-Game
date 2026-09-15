# This is the player class.
# The player class extends the character class.
# The player class holds all shared logic between playable characters — 
# inventory, armor, health property, item usage, and the vacuum attack.
# Luigi and Mario both extend this class and customize their own stats.

import character, random

MAX_HEALTH = 100
ITEM_ARRAY_SIZE = 3


class player(character):

    def __init__(self, name, health, skill, maxArmorSlots):
        super().__init__(name, health, skill)
        self.maxArmorSlots = maxArmorSlots
        self.armor = 0
        self.inventory = {
            "hearts": {
                "smallHearts": [None] * ITEM_ARRAY_SIZE,
                "largeHearts": [None] * ITEM_ARRAY_SIZE
            },
            "armor": {
                "smallArmor": [None] * ITEM_ARRAY_SIZE,
                "largeArmor": [None] * ITEM_ARRAY_SIZE
            },
            "ghosts": {
            "capturedGhosts": [None] * ITEM_ARRAY_SIZE   
        }
        }

    # --- Health property ---
    # Intercepts any assignment to self.health and enforces the 0-100 cap.
    # Nothing else needs to manually clamp health — it is automatic.

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if value > MAX_HEALTH:
            self._health = MAX_HEALTH
        elif value < 0:
            self._health = 0
        else:
            self._health = value

    # --- Inventory ---

    def addToInventory(self, item):
        slotMap = {
            "smallHeart": self.inventory["hearts"]["smallHearts"],
            "largeHeart": self.inventory["hearts"]["largeHearts"],
            "smallArmor": self.inventory["armor"]["smallArmor"],
            "largeArmor": self.inventory["armor"]["largeArmor"],
            "capturedGhost": self.inventory["ghosts"]["capturedGhosts"]
        }

        if item.itemType not in slotMap:
            print("Item type not recognized. Item not added to inventory.")
            return

        slots = slotMap[item.itemType]
        for i in range(len(slots)):
            if slots[i] is None:
                slots[i] = item
                print(f"{item.name} added to slot {i + 1}!")
                return
        else:
            print(f"No empty slots available for {item.name}.")

    def getInventory(self):
        print(f"\n{self.name}'s Inventory:")
        print("  Hearts:")
        print(f"    Small Hearts: {self._countSlots('hearts', 'smallHearts')}/{ITEM_ARRAY_SIZE}")
        print(f"    Large Hearts: {self._countSlots('hearts', 'largeHearts')}/{ITEM_ARRAY_SIZE}")
        print("  Armor:")
        print(f"    Small Armor:  {self._countSlots('armor', 'smallArmor')}/{ITEM_ARRAY_SIZE}")
        print(f"    Large Armor:  {self._countSlots('armor', 'largeArmor')}/{ITEM_ARRAY_SIZE}")
        print(f"  Active Armor Slots: {self.armor}/{self.maxArmorSlots}\n")
        print("  Ghosts:")
        print(f"    Captured: {self._countSlots('ghosts', 'capturedGhosts')}/{ITEM_ARRAY_SIZE}")

    def _countSlots(self, category, slotType):
        # Counts occupied slots (not None) for display in getInventory
        return sum(1 for slot in self.inventory[category][slotType] if slot is not None)

    # --- Using items ---

    def useItem(self):
        self.getInventory()
        choice = input(
            "Choose an item to use:\n"
            "1) Small Heart\n"
            "2) Large Heart\n"
            "3) Small Armor\n"
            "4) Large Armor\n"
            "> "
        )

        slotMap = {
            "1": self.inventory["hearts"]["smallHearts"],
            "2": self.inventory["hearts"]["largeHearts"],
            "3": self.inventory["armor"]["smallArmor"],
            "4": self.inventory["armor"]["largeArmor"]
        }

        if choice not in slotMap:
            print("Invalid choice. Please try again.")
            return

        slots = slotMap[choice]
        for i in range(len(slots)):
            if slots[i] is not None:
                item = slots[i]
                slots[i] = None
                item.use(self)
                return
        else:
            print("No items of that type in inventory.")

    # --- Combat ---

    def takeDamage(self, amount):
        if self.armor > 0:
            self.armor -= 1
            print(f"{self.name}'s armor absorbed the hit! ({self.armor}/{self.maxArmorSlots} slots remaining)")
        else:
            self.health -= amount

    def vacuumAttack(self, enemy):
        roll = random.randint(1, 20)
        print(f"{self.name} rolls a {roll}!")

        if roll == 1:
            enemy.health = 0
            print(f"Perfect catch! {enemy.name} is sucked in instantly!")
        else:
            damage = self.vacuumBaseDamage + self.skill * random.randint(1, self.vacuumMaxScale)
            enemy.takeDamage(damage)
            print(f"{self.name} attacks {enemy.name} for {damage} damage!")
