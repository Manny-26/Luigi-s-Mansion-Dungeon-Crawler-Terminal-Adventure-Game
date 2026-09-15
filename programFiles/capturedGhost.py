import item

class capturedGhost(item):
    def __init__(self, ghostName, ghostSkill):
        super().__init__(
            name=f"Captured {ghostName}",
            description=f"A captured {ghostName}. Use it to open the exit door.",
            itemType="capturedGhost",
            magnitude=ghostSkill
        )

    def use(self, player):
        print(f"{self.name} is needed to open the exit door!")