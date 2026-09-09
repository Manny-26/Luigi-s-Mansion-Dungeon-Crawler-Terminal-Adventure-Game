
# This is the luigi class.
# The luigi class extends the character class
# The luigi class adds an inventory to the character class that allows luigi to obtain/store items.
# The inventory is a dictionary that contains two dictionaries: one for hearts and one for armor.

import item, character, random

MAX_HEALTH = 100
MAX_ARMOR_SLOTS = 3
ITEM_ARRAY_SIZE = 3
VACUUM_BASE_DAMAGE = 15

# This class represents the main character in the game.
# This class extends the character class.
# This class adds an inventory that Luigi can use to obtain/store items.
# This class also adds an armor attribute that allows luigi to shield themselves from damage.
class luigi(character):
    
    def __init__(self):
        super().__init__("Luigi", 100, 1)
        self.inventory = {
                            "hearts":   {
                                            "smallHearts": [None] * ITEM_ARRAY_SIZE,
                                            "largeHearts": [None] * ITEM_ARRAY_SIZE
                                        },

                            "armor":    {
                                            "smallArmor": [None] * ITEM_ARRAY_SIZE,
                                            "largeArmor": [None] * ITEM_ARRAY_SIZE
                                        }
                        }
        self.armor = 0

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


        def addToInventory(self, item):
            slotMap = {
                "smallHeart": self.inventory["hearts"]["smallHearts"],
                "largeHeart": self.inventory["hearts"]["largeHearts"],
                "smallArmor": self.inventory["armor"]["smallArmor"],
                "largeArmor": self.inventory["armor"]["largeArmor"]
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
        print("Inventory:")
        print("Hearts:")
        print("  Small Hearts: " + str(self.inventory["hearts"]["smallHearts"]))
        print("  Large Hearts: " + str(self.inventory["hearts"]["largeHearts"]))
        print("Armor:")
        print("  Small Armor: " + str(self.inventory["armor"]["smallArmor"]))
        print("  Large Armor: " + str(self.inventory["armor"]["largeArmor"]))

    # Separate function for adding health to Luigi.
    # Items that heal luigi will call this function to add health.
    def addHealth(self, amount):
        self.health = self.health + amount
        if self.health > 100:
            self.health = 100

    def takeDamage(self, amount):
        if self.armor > 0:
            self.armor -= 1
            print(f"Armor absorbed the hit! ({self.armor}/{MAX_ARMOR_SLOTS} slots remaining)")
        else:
            self.health -= amount

    def vacuumAttack(self, enemy):
        print(f"something")
        instantCatch = random.randint(1,20)
        if instantCatch == 1:
            enemy.health = 0
            print("perfect catch")
        else:
            damage = VACUUM_BASE_DAMAGE + self.skill * random.randint(1, 3)
            #TO-DO print damage message and enemy takes damage at same time
            enemy.takeDamage (damage)
        
    def placeInSlot(luigi, item):
        if item.itemType == "smallHeart":
            for i in range(len(luigi.inventory["hearts"]["smallHearts"])):
                if luigi.inventory["hearts"]["smallHearts"][i] is None:
                    luigi.inventory["hearts"]["smallHearts"][i] = item
                    break;
            print("No empty slots available for small hearts.")

        elif item.itemType == "largeHeart":
            for i in range(len(luigi.inventory["hearts"]["largeHearts"])):
                if luigi.inventory["hearts"]["largeHearts"][i] is None:
                    luigi.inventory["hearts"]["largeHearts"][i] = item
                    break;
            print("No empty slots available for large hearts.")
            

        elif item.itemType == "smallArmor":
            for i in range(len(luigi.inventory["armor"]["smallArmor"])):
                if luigi.inventory["armor"]["smallArmor"][i] is None:
                    luigi.inventory["armor"]["smallArmor"][i] = item
                    break;
            print("No empty slots available for small armor.")
            
        elif item.itemType == "largeArmor":
            for i in range(len(luigi.inventory["armor"]["largeArmor"])):
                if luigi.inventory["armor"]["largeArmor"][i] is None:
                    luigi.inventory["armor"]["largeArmor"][i] = item
                    break;
            print("No empty slots available for large armor.")
            
        else:
            print("Invalid item type.")

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
 

    
    
    




    

