# This is a smallHeart class extends the item class. 
# It represents a small heart item that can be used to heal Luigi in game.

import item

SMALL_HEART_HEALTH = 25

class smallHeart(item):
    def __init__(self):
        super().__init__("Small Heart", "This is a small heart. It heals 25 health.", "smallHeart", SMALL_HEART_HEALTH)

    def use(self, luigi):
        luigi.health += self.magnitude
        print(f"Used {self.name}! Restored {self.magnitude} health.")