# This class represents a ghost.
# The ghost class extends the character class.
# The ghost class adds a numAttacks attribute for determining which attack the ghost will use in battle.

from character import character
from capturedGhost import capturedGhost

class ghost(character):
    def __init__(self, name, health, skill, numAttacks):
        super().__init__(name, health, skill)
        self.numAttacks = numAttacks

    def takeDamage(self, amount):
        """Reduce this ghost's health and return the damage received."""
        return super().takeDamage(amount)

    def toItem(self):
        """Convert a defeated ghost into a collectible inventory item."""
        return capturedGhost(self.name, self.skill)
