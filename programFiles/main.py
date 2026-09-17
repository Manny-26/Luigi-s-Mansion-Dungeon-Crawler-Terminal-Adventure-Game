"""Main startup file for the video game. Run this file to play the game"""

from game_funcs import menu


def main():
    """Open the main menu and return the game selected by the player."""
    active_game = menu()

    if active_game is None:
        return None

    if active_game.currentLevel is None:
        active_game.start()

    active_game.runGameLoop()
    return active_game
    



if __name__ == "__main__":
    # A new or restored game is now available for the future gamSeeplay startup.
    # If the player exits from the menu, menu() returns None instead.
    active_game = main()
