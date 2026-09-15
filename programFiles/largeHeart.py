
# This is a largeHeart class.
# The largeHeart class extends the item class. 
# It represents a large heart item that can be used to heal Luigi in game.

import item

LARGE_HEART_HEALTH = 100

class largeHeart(item):
    def __init__(self):
        super().__init__("Large Heart", "This is a large heart. It heals 100 health.", "largeHeart", LARGE_HEART_HEALTH)

    def use(self, player):
        player.health += self.magnitude
        print(f"Used {self.name}! Restored {self.magnitude} health.")