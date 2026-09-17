


# This class represents a character.
# Each character contains within it a name, a health level, and a skill.
# Name and health are self explanatory (I hope...)
# Skill represents a number that is used to determine the amount of damage one can do. 
class character:
    def __init__(self, name, health, skill):
        self.name = name
        self.health = health
        self.skill = skill

    def setName(self, name):
        self.name = name

    def setHealth(self, hp):
        self.health = hp

    def setSkill(self, skill):
        self.skill = skill

    def getName(self):
        return self.name

    def getHealth(self):
        return self.health

    def getSkill(self):
        return self.skill

    def takeDamage(self, amount):
        """Remove health without allowing it to fall below zero."""
        previousHealth = self.health
        self.health = max(0, self.health - amount)
        return previousHealth - self.health

    def attack(self, target):
        """Attack a target using the move supplied by a subclass."""
        raise NotImplementedError(
            f"{type(self).__name__} must implement the attack() method."
        )
