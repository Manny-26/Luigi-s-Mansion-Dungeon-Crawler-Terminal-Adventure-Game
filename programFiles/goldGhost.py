# This is the goldGhost class.
# The goldGhost class extends the ghost class.
# The gold ghost is the simplest enemy in the game. It has 100 health and 1 weak attack.

import random
from ghost import ghost

GOLD_GHOST_BASE_DAMAGE = 10

class goldGhost(ghost):
    def __init__(self):
        super().__init__("Gold Ghost", 100, 1, 1)

    def punch(self, player):
        damage = GOLD_GHOST_BASE_DAMAGE + self.skill * random.randint(1, 3)
        player.takeDamage(damage)
        print(f"{self.name} punches {player.name} for {damage} damage!")
