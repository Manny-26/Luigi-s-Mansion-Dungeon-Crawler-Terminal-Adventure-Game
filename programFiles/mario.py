"""Mario player character class.

Mario currently shares Luigi's player abilities, inventory layout, and base
statistics.  Keeping him as a subclass means game logic can treat both player
choices the same while still recording the selected character in save files.

This choice was mainly done to save time. Refactoring Luigi into a more generic "Player" 
class would have taken longer than just writing this simple subclass. 
"""

from player import player


class mario(player):
    def __init__(self):
        super().__init__("Mario", 100, 2)
        self.vacuumBaseDamage = 25
        self.vacuumMaxScale = 3
