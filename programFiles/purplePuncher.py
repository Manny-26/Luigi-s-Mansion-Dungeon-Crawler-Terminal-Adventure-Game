# This is the purplePuncher class.
# The purplePuncher class extends the ghost class.
# The purplePuncher is stronger than the goldGhost as it has two attacks: softPunch and hardPunch.
# softPunch is a weaker attack that does less damage than hardPunch (but more than the goldGhost's attack).
# hardPunch is a stronger attack that does more damage than softPunch.

import ghost, random

PURPLE_PUNCHER_BASE_DAMAGE = 15

class purplePuncher(ghost):
    def __init__(self):
        super().__init__("Purple Puncher", 50, 2, 2)

    def softPunch(self, player):
        damage = PURPLE_PUNCHER_BASE_DAMAGE + self.skill * random.randint(1, 3)
        player.takeDamage(damage)
        print(f"{self.name} punches {player.name} for {damage} damage!")

    def hardPunch(self, player):
        damage = PURPLE_PUNCHER_BASE_DAMAGE + self.skill * random.randint(5, 10)
        player.takeDamage(damage)
        print(f"{self.name} lands a left hook onto {player.name} for {damage} damage! It's extra painful!")