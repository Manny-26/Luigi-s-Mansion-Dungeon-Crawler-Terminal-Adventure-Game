# This class represents a ghost.
# The ghost class extends the character class.
# The ghost class adds a numAttacks attribute for determining which attack the ghost will use in battle.

import character
from capturedGhost import capturedGhost

class ghost(character):
    def __init__(self, name, health, skill, numAttacks):
        super().__init__(name, health, skill)
        self.numAttacks = numAttacks

    def toItem(self):
        return capturedGhost(self.name, self.skill)
