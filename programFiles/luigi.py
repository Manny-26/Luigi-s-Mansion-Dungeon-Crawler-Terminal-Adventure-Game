# This is the luigi class.
# Luigi extends the player class.
# Luigi has 3 armor slots, low base vacuum damage, but high random scaling —
# he can hit very hard but is inconsistent.

import player

class luigi(player):
    def __init__(self):
        super().__init__("Luigi", 100, 1, maxArmorSlots=3)
        self.vacuumBaseDamage = 10
        self.vacuumMaxScale = 15   # damage = 10 + skill * randint(1, 10)
