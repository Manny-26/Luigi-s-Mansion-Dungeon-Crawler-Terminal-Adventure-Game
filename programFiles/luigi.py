
# This is the luigi class.
# The luigi class extends the character class
# The luigi class adds an inventory to the character class that allows luigi to obtain/store items.
# The inventory is a dictionary that contains two dictionaries: one for hearts and one for armor.

from player import player



# This class represents the main character in the game.
# This class extends the character class.
# This class adds an inventory that Luigi can use to obtain/store items.
# This class also adds an armor attribute that allows luigi to shield themselves from damage.
class luigi(player):
    
    def __init__(self):
        super().__init__("Luigi", 100, 1)
        self.vacuumBaseDamage = 10
        self.vacuumMaxScale = 15

    

    
    
    




    
