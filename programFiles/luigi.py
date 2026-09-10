
# This is the luigi class.
# The luigi class extends the character class
# The luigi class adds an inventory to the character class that allows luigi to obtain/store items.
# The inventory is a dictionary that contains two dictionaries: one for hearts and one for armor.

import item, character

SMALL_HEART_HEALTH = 25
LARGE_HEART_HEALTH = 100

VACUUM_BASE_DAMAGE = 15

SMALL_ARMOR_VALUE = 1
LARGE_ARMOR_VALUE = 3

ITEM_ARRAY_SIZE = 3



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

    def addToInventory(self, item):
        luigi_funcs.placeInSlot(self, item)

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
        self.health = self.health - amount
        if self.health < 0:
            # TO-DO: Investigate if we can tie health to the game state
            # (i.e. if health is zero, then the game ends.)
            self.health = 0

    def vacuumAttack(self, enemy):
        ...# TO-DO: Implement vacuum attack functionality here

    def useItem(self, item):
        if (item.type == "heart"):
            self.addHealth(item.value)
        elif (item.type == "armor"):
            self.armor = self.armor + item.value

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

    # TO-DO: Implement functions that use the item from the inventory and add to the attributes on luigi

    
    
    
# rando commnts to tst git fork stuff



    

