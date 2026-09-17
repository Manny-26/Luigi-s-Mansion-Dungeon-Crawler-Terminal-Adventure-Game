# This is the purplePuncher class.
# The purplePuncher class extends the ghost class.
# The purplePuncher is stronger than the goldGhost as it has two attacks: softPunch and hardPunch.
# softPunch is a weaker attack that does less damage than hardPunch (but more than the goldGhost's attack).
# hardPunch is a stronger attack that does more damage than softPunch.

import random

from ghost import ghost

PURPLE_PUNCHER_BASE_DAMAGE = 15

class purplePuncher(ghost):
    def __init__(self):
        super().__init__("Purple Puncher", 50, 2, 2)

    def attack(self, target):
        """Attack a target with a randomly selected punch."""
        selected_attack = random.choice((self.softPunch, self.hardPunch))
        return selected_attack(target)

    def softPunch(self, target):
        damage = PURPLE_PUNCHER_BASE_DAMAGE + self.skill * random.randint(1, 3)
        damageDealt = target.takeDamage(damage)
        print(f"{self.name} punches {target.name} for {damageDealt} damage!")

    def hardPunch(self, target):
        damage = PURPLE_PUNCHER_BASE_DAMAGE + self.skill * random.randint(5, 10)
        damageDealt = target.takeDamage(damage)
        print(f"{self.name} lands a left hook onto {target.name} for {damageDealt} damage! It's extra painful!")
