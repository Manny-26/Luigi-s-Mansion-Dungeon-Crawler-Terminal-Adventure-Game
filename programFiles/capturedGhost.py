from item import item


class capturedGhost(item):
    def __init__(self, ghostName, ghostSkill):
        super().__init__(
            f"Captured {ghostName}",
            f"The captured spirit of a {ghostName}.",
            "capturedGhost",
            ghostSkill,
        )

    def use(self, player):
        print(f"{self.name} is part of your permanent ghost collection.")
        return False
