# This is the mario class.
# Mario extends the player class.
# Mario has 5 armor slots and high base vacuum damage, but low random scaling —
# he hits reliably hard every time.

import player

class mario(player):
    def __init__(self):
        super().__init__("Mario", 100, 2, maxArmorSlots=5)
        self.vacuumBaseDamage = 25
        self.vacuumMaxScale = 3    # damage = 25 + skill * randint(1, 3)
