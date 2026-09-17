# This is the goldGhost class. 
# The goldGhost class extends the ghost class.
# The gold ghost is the simplest enemy in the game. It has low health and only 1 weak attack.

import random

from ghost import ghost

GOLD_GHOST_BASE_DAMAGE = 10

class goldGhost(ghost):
    def __init__(self):
        super().__init__("Gold Ghost", 30, 1, 1)

    def attack(self, target):
        """Attack a target with the Gold Ghost's punch."""
        return self.punch(target)

    def punch(self, target):
        damage = GOLD_GHOST_BASE_DAMAGE
        damageDealt = target.takeDamage(damage)
        print(f"{self.name} punches {target.name} for {damageDealt} damage!")
