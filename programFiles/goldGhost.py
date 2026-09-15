# This is the goldGhost class. 
# The goldGhost class extends the ghost class.
# The gold ghost is the simplest enemy in the game. It has low health and only 1 weak attack.

import ghost, random

GOLD_GHOST_BASE_DAMAGE = 10

class goldGhost(ghost):
    def __init__(self):
        super().__init__("Gold Ghost", 30, 1, 1)

    def punch(self, player):
        damage = GOLD_GHOST_BASE_DAMAGE
        player.takeDamage(damage)
        print(f"{self.name} punches {player.name} for {damage} damage!")
