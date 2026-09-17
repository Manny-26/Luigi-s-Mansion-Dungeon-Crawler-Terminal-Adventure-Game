# This is the purplePuncher class.
# The purplePuncher class extends the ghost class.
# The purplePuncher is stronger than the goldGhost — it has two attacks: softPunch and hardPunch.
# It picks between them randomly each turn using its generic punch() method.

import random
from ghost import ghost

PURPLE_PUNCHER_BASE_DAMAGE = 15

class purplePuncher(ghost):
    def __init__(self):
        super().__init__("Purple Puncher", 100, 2, 2)

    def punch(self, player):
        # randomly pick between soft and hard punch each turn
        if random.randint(1, 2) == 1:
            self.softPunch(player)
        else:
            self.hardPunch(player)

    def softPunch(self, player):
        damage = PURPLE_PUNCHER_BASE_DAMAGE + self.skill * random.randint(1, 3)
        player.takeDamage(damage)
        print(f"{self.name} punches {player.name} for {damage} damage!")

    def hardPunch(self, player):
        damage = PURPLE_PUNCHER_BASE_DAMAGE + self.skill * random.randint(5, 10)
        player.takeDamage(damage)
        print(f"{self.name} lands a left hook onto {player.name} for {damage} damage! It's extra painful!")
