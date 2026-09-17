from item import item

SMALL_HEART_HEALTH = 25


class smallHeart(item):
    def __init__(self):
        super().__init__("Small Heart", "Restores 25 health.", "smallHeart", SMALL_HEART_HEALTH)

    def use(self, player):
        restored = player.addHealth(self.magnitude)
        if restored == 0:
            print("Your health is already full.")
            return False
        print(f"Used {self.name}! Restored {restored} health.")
        return True
