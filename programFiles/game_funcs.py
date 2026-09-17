"""Menu and JSON save-file helpers for the terminal adventure game."""

from datetime import datetime, timezone
import json
from pathlib import Path

from game import game
from character import character
from player import player
from luigi import luigi
from mario import mario
from level import level
from room import room
from ghost import ghost
from goldGhost import goldGhost
from purplePuncher import purplePuncher
from item import item
from capturedGhost import capturedGhost
from smallHeart import smallHeart
from largeHeart import largeHeart
from smallArmor import smallArmor
from largeArmor import largeArmor


SAVE_FILE = Path(__file__).with_name("game_saves.json")


class SaveFileError(Exception):
    """Raised when game_saves.json is present but cannot be used."""


# Only these game classes may be reconstructed from JSON. This explicit list
# avoids importing or executing arbitrary classes named inside a save file.
_CLASS_REGISTRY = {
    cls.__name__: cls
    for cls in (
        game,
        character,
        player,
        luigi,
        mario,
        level,
        room,
        ghost,
        goldGhost,
        purplePuncher,
        item,
        capturedGhost,
        smallHeart,
        largeHeart,
        smallArmor,
        largeArmor,
    )
}


def _serialize(value):
    """Convert a game value into data that Python's JSON encoder accepts."""
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, list):
        return [_serialize(entry) for entry in value]
    if isinstance(value, tuple):
        return {"__type__": "tuple", "items": [_serialize(entry) for entry in value]}
    if isinstance(value, dict):
        return {str(key): _serialize(entry) for key, entry in value.items()}

    class_name = type(value).__name__
    if class_name not in _CLASS_REGISTRY:
        raise TypeError(f"Cannot save objects of type {class_name!r}.")

    return {
        "__type__": class_name,
        "attributes": {
            name: _serialize(attribute)
            for name, attribute in vars(value).items()
        },
    }


def _deserialize(value):
    """Rebuild values produced by _serialize."""
    if isinstance(value, list):
        return [_deserialize(entry) for entry in value]
    if not isinstance(value, dict):
        return value

    value_type = value.get("__type__")
    if value_type == "tuple":
        return tuple(_deserialize(entry) for entry in value.get("items", []))
    if value_type is None:
        return {key: _deserialize(entry) for key, entry in value.items()}
    if value_type not in _CLASS_REGISTRY:
        raise SaveFileError(f"Save file contains unknown object type {value_type!r}.")

    attributes = value.get("attributes")
    if not isinstance(attributes, dict):
        raise SaveFileError(f"Saved {value_type!r} object has invalid attributes.")

    cls = _CLASS_REGISTRY[value_type]
    restored_object = cls.__new__(cls)
    for name, attribute in attributes.items():
        setattr(restored_object, name, _deserialize(attribute))
    return restored_object


def _empty_save_document():
    return {"version": 1, "saves": []}


def _read_save_document(file_path=None):
    path = Path(SAVE_FILE if file_path is None else file_path)
    if not path.exists():
        return _empty_save_document()

    try:
        with path.open("r", encoding="utf-8") as save_file:
            document = json.load(save_file)
    except json.JSONDecodeError as error:
        raise SaveFileError(f"{path.name} does not contain valid JSON.") from error
    except OSError as error:
        raise SaveFileError(f"Could not read {path.name}: {error}") from error

    if isinstance(document, list):
        document = {"version": 1, "saves": document}

    if not isinstance(document, dict) or not isinstance(document.get("saves"), list):
        raise SaveFileError(f"{path.name} does not have a valid save-file structure.")
    return document


def _write_save_document(document, file_path=None):
    path = Path(SAVE_FILE if file_path is None else file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")

    try:
        with temporary_path.open("w", encoding="utf-8") as save_file:
            json.dump(document, save_file, indent=4)
            save_file.write("\n")
        temporary_path.replace(path)
    except OSError as error:
        raise SaveFileError(f"Could not write {path.name}: {error}") from error


def save_game(game_instance, save_id=None, file_path=None):
    """Append a game save, or update one when save_id is supplied."""
    if not isinstance(game_instance, game):
        raise TypeError("save_game expects a game instance.")

    document = _read_save_document(file_path)
    saves = document["saves"]
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    if save_id is None:
        used_ids = {
            record.get("save_id")
            for record in saves
            if isinstance(record, dict) and isinstance(record.get("save_id"), int)
        }
        save_id = 1
        while save_id in used_ids:
            save_id += 1

        record = {
            "save_id": save_id,
            "character": game_instance.player.name,
            "level": game_instance.currentLevelNumber,
            "created_at": now,
            "updated_at": now,
            "game": _serialize(game_instance),
        }
        saves.append(record)
    else:
        record = next(
            (r for r in saves if isinstance(r, dict) and r.get("save_id") == save_id),
            None,
        )
        if record is None:
            raise SaveFileError(f"Save #{save_id} does not exist.")

        record.update({
            "character": game_instance.player.name,
            "level": game_instance.currentLevelNumber,
            "updated_at": now,
            "game": _serialize(game_instance),
        })

    _write_save_document(document, file_path)
    return save_id


def list_saves(file_path=None):
    """Return menu-friendly information about every available save."""
    records = _read_save_document(file_path)["saves"]
    summaries = []
    for record in records:
        if not isinstance(record, dict) or "save_id" not in record or "game" not in record:
            raise SaveFileError("A save record is missing required information.")
        summaries.append({
            "save_id":    record["save_id"],
            "character":  record.get("character", "Unknown"),
            "level":      record.get("level", "Unknown"),
            "updated_at": record.get("updated_at", "Unknown"),
        })
    return summaries


def load_game(save_id, file_path=None):
    """Reconstruct and return the game instance stored under save_id."""
    records = _read_save_document(file_path)["saves"]
    record = next(
        (r for r in records if isinstance(r, dict) and r.get("save_id") == save_id),
        None,
    )
    if record is None:
        raise SaveFileError(f"Save #{save_id} does not exist.")

    restored_game = _deserialize(record.get("game"))
    if not isinstance(restored_game, game):
        raise SaveFileError(f"Save #{save_id} does not contain a game instance.")
    return restored_game


def _choose_character():
    while True:
        print("\nChoose your character:")
        print("1) Mario — 5 armor slots, high base damage, consistent hits")
        print("2) Luigi — 3 armor slots, low base damage, but can hit massive")
        choice = input("Select an option: ").strip().lower()

        if choice in {"1", "m", "mario"}:
            from mario import mario as Mario
            return Mario()
        if choice in {"2", "l", "luigi"}:
            from luigi import luigi as Luigi
            return Luigi()
        print("Invalid choice. Enter 1 for Mario or 2 for Luigi.")


def _select_save():
    try:
        saves = list_saves()
    except SaveFileError as error:
        print(f"Unable to open the save file: {error}")
        return None

    if not saves:
        print("\nNo saved games were found.")
        return None

    print("\nSelect a save:")
    for menu_number, save in enumerate(saves, start=1):
        print(
            f"{menu_number}) {save['character']} - "
            f"Floor {save['level']} - Last saved {save['updated_at']}"
        )
    print("B) Back")

    while True:
        choice = input("Select a save: ").strip().lower()
        if choice in {"b", "back"}:
            return None

        try:
            menu_number = int(choice)
        except ValueError:
            print("Invalid choice. Enter a save number or B to go back.")
            continue

        if not 1 <= menu_number <= len(saves):
            print("Invalid choice. Enter one of the displayed save numbers.")
            continue

        try:
            return load_game(saves[menu_number - 1]["save_id"])
        except SaveFileError as error:
            print(f"Unable to load that save: {error}")
            return None


def menu():
    """Display the startup menu and return the chosen game instance."""
    while True:
        print("\n==================================================")
        print("      LUIGI'S MANSION: TERMINAL ADVENTURE")
        print("==================================================")
        print("1) New Save")
        print("2) Select Save")
        print("3) Exit")

        choice = input("Select an option: ").strip().lower()

        if choice in {"1", "new", "new save"}:
            new_game = game(player=_choose_character())
            try:
                save_id = save_game(new_game)
            except SaveFileError as error:
                print(f"Unable to create the save: {error}")
                continue
            print(f"\nCreated save #{save_id} for {new_game.player.name}.")
            return new_game

        if choice in {"2", "select", "select save"}:
            selected_game = _select_save()
            if selected_game is not None:
                print(f"\nLoaded {selected_game.player.name}'s save.")
                return selected_game
            continue

        if choice in {"3", "exit", "quit"}:
            print("Goodbye!")
            raise SystemExit(0)

        print("Invalid choice. Enter 1, 2, or 3.")
