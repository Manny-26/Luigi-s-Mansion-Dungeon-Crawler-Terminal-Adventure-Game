
# This is a largeHeart class.
# The largeHeart class extends the item class. 
# It represents a large heart item that can be used to heal Luigi in game.

LARGE_HEART_HEALTH = 100

from item import item

class largeHeart(item):
    def __init__(self):
        super().__init__("Large Heart", "This is a large heart. It heals 100 health.", "largeHeart", LARGE_HEART_HEALTH)

    def use(self, player):
        restored = player.addHealth(self.magnitude)
        if restored == 0:
            print("Your health is already full.")
            return False
        print(f"Used {self.name}! Restored {restored} health.")
        return True
