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


# Only these game classes may be reconstructed from JSON.  This explicit list
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
    """Rebuild values produced by :func:`_serialize`."""

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


def _get_save_name(record):
    """Return a saved name, including a fallback for older save records."""
    save_name = record.get("save_name")
    if isinstance(save_name, str) and save_name.strip():
        return save_name.strip()

    character_name = record.get("character", "Unknown")
    save_id = record.get("save_id", "?")
    return f"{character_name} Save #{save_id}"


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

    # Accept a plain list as a small compatibility convenience for early save
    # files, but always write the documented object format from this module.
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
    """Append a game save, or update one when ``save_id`` is supplied.

    The numeric ID of the newly created or updated save is returned.
    """

    if not isinstance(game_instance, game):
        raise TypeError("save_game expects a game instance.")

    document = _read_save_document(file_path)
    saves = document["saves"]
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    if save_id is None:
        used_ids = {
            record.get("save_id")
            for record in saves
            if isinstance(record, dict)
            and isinstance(record.get("save_id"), int)
        }
        save_id = 1
        while save_id in used_ids:
            save_id += 1

        game_instance.saveId = save_id
        save_name = getattr(game_instance, "saveName", None)
        if not isinstance(save_name, str) or not save_name.strip():
            save_name = f"{game_instance.player.name} Save #{save_id}"
        game_instance.saveName = save_name.strip()
        record = {
            "save_id": save_id,
            "save_name": game_instance.saveName,
            "character": game_instance.player.name,
            "level": game_instance.currentLevelNumber,
            "created_at": now,
            "updated_at": now,
            "game": _serialize(game_instance),
        }
        saves.append(record)
    else:
        record = next(
            (
                saved_record
                for saved_record in saves
                if isinstance(saved_record, dict)
                and saved_record.get("save_id") == save_id
            ),
            None,
        )
        if record is None:
            raise SaveFileError(f"Save #{save_id} does not exist.")

        game_instance.saveId = save_id
        save_name = getattr(game_instance, "saveName", None)
        if not isinstance(save_name, str) or not save_name.strip():
            save_name = _get_save_name(record)
        game_instance.saveName = save_name.strip()
        record.update(
            {
                "save_name": game_instance.saveName,
                "character": game_instance.player.name,
                "level": game_instance.currentLevelNumber,
                "updated_at": now,
                "game": _serialize(game_instance),
            }
        )

    _write_save_document(document, file_path)
    return save_id


def delete_save(save_id, file_path=None):
    """Delete a save record and return its display name."""
    document = _read_save_document(file_path)
    saves = document["saves"]

    for index, record in enumerate(saves):
        if isinstance(record, dict) and record.get("save_id") == save_id:
            save_name = _get_save_name(record)
            del saves[index]
            _write_save_document(document, file_path)
            return save_name

    raise SaveFileError(f"Save #{save_id} does not exist.")


def list_saves(file_path=None):
    """Return menu-friendly information about every available save."""

    records = _read_save_document(file_path)["saves"]
    summaries = []
    for record in records:
        if not isinstance(record, dict) or "save_id" not in record or "game" not in record:
            raise SaveFileError("A save record is missing required information.")
        summaries.append(
            {
                "save_id": record["save_id"],
                "save_name": _get_save_name(record),
                "character": record.get("character", "Unknown"),
                "level": record.get("level", "Unknown"),
                "updated_at": record.get("updated_at", "Unknown"),
            }
        )
    return summaries


def load_game(save_id, file_path=None):
    """Reconstruct and return the game instance stored under ``save_id``."""

    records = _read_save_document(file_path)["saves"]
    record = next(
        (
            saved_record
            for saved_record in records
            if isinstance(saved_record, dict)
            and saved_record.get("save_id") == save_id
        ),
        None,
    )
    if record is None:
        raise SaveFileError(f"Save #{save_id} does not exist.")

    restored_game = _deserialize(record.get("game"))
    if not isinstance(restored_game, game):
        raise SaveFileError(f"Save #{save_id} does not contain a game instance.")

    restored_game.saveId = save_id
    restored_game.saveName = _get_save_name(record)

    # Bring saves from versions before the shared player class up to date.
    restored_player = restored_game.player
    if isinstance(restored_player, mario):
        restored_player.vacuumBaseDamage = getattr(
            restored_player, "vacuumBaseDamage", 25
        )
        restored_player.vacuumMaxScale = getattr(
            restored_player, "vacuumMaxScale", 3
        )
    elif isinstance(restored_player, luigi):
        restored_player.vacuumBaseDamage = getattr(
            restored_player, "vacuumBaseDamage", 10
        )
        restored_player.vacuumMaxScale = getattr(
            restored_player, "vacuumMaxScale", 15
        )

    inventory = getattr(restored_player, "inventory", None)
    if isinstance(inventory, dict):
        inventory.setdefault("ghosts", {"capturedGhosts": []})
        inventory["ghosts"].setdefault("capturedGhosts", [])

    # Serialization stores objects by value. Relink an in-progress encounter
    # to the ghost in its room so saving during combat preserves one shared
    # source of health and encounter state.
    if restored_game.state == "COMBAT":
        room_name = getattr(restored_game, "currentRoomName", None)
        object_name = getattr(restored_game, "activeGhostObjectName", None)
        current_level = getattr(restored_game, "currentLevel", None)
        if current_level is not None and room_name in current_level.rooms:
            current_room = current_level.rooms[room_name]
            object_data = current_room.interactableObjects.get(object_name)
            if object_data is not None and isinstance(object_data.get("outcome"), ghost):
                restored_game.activeGhost = object_data["outcome"]

    return restored_game


def _choose_character():
    while True:
        print("\nChoose your main character:")
        print()
        print("1) Mario")
        print("2) Luigi")
        choice = input("\nSelect an option: ").strip().lower()

        if choice in {"1", "m", "mario"}:
            return mario()
        if choice in {"2", "l", "luigi"}:
            return luigi()
        print("Invalid choice. Enter 1 for Mario or 2 for Luigi.")


def _choose_save_name():
    """Ask for a non-empty name for a new save."""
    while True:
        save_name = input("\nEnter a name for this save: ").strip()
        if save_name:
            return save_name
        print("Save names cannot be empty.")


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
    print()
    for menu_number, save in enumerate(saves, start=1):
        print(
            f"{menu_number}) {save['save_name']} - {save['character']} - "
            f"Floor {save['level']} - Last saved {save['updated_at']}"
        )
    print("B) Back")

    while True:
        choice = input("\nSelect a save: ").strip().lower()
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


def _delete_save_menu():
    """Let the player select and confirm a save-file deletion."""
    try:
        saves = list_saves()
    except SaveFileError as error:
        print(f"Unable to open the save file: {error}")
        return

    if not saves:
        print("\nNo saved games were found.")
        return

    print("\nDelete a save:")
    print()
    for menu_number, save in enumerate(saves, start=1):
        print(
            f"{menu_number}) {save['save_name']} - {save['character']} - "
            f"Floor {save['level']}"
        )
    print("B) Back")

    while True:
        choice = input("\nSelect a save to delete: ").strip().lower()
        if choice in {"b", "back"}:
            return

        try:
            menu_number = int(choice)
        except ValueError:
            print("Invalid choice. Enter a save number or B to go back.")
            continue

        if not 1 <= menu_number <= len(saves):
            print("Invalid choice. Enter one of the displayed save numbers.")
            continue

        selected_save = saves[menu_number - 1]
        confirmation = input(
            f"Delete '{selected_save['save_name']}' permanently? (y/n): "
        ).strip().lower()

        if confirmation not in {"y", "yes"}:
            print("Save deletion cancelled.")
            return

        try:
            deleted_name = delete_save(selected_save["save_id"])
        except SaveFileError as error:
            print(f"Unable to delete that save: {error}")
            return

        print(f"\nDeleted save '{deleted_name}'.")
        return


def menu():
    """Display the startup menu and return the chosen game instance.

    A new game is immediately recorded in ``game_saves.json``.  Selecting an
    existing save reconstructs the same object graph that was stored. Saves can
    also be deleted after an explicit confirmation. Choosing Exit raises
    ``SystemExit`` so the program ends even if a caller ignores the return value.
    """

    while True:
        print("\n==================================================")
        print("      LUIGI'S MANSION: TERMINAL ADVENTURE")
        print("==================================================")
        print()
        print("1) New Save")
        print("2) Select Save")
        print("3) Delete Save")
        print("4) Exit")

        choice = input("\nSelect an option: ").strip().lower()

        if choice in {"1", "new", "new save"}:
            new_game = game(player=_choose_character())
            new_game.saveName = _choose_save_name()
            try:
                save_id = save_game(new_game)
            except SaveFileError as error:
                print(f"Unable to create the save: {error}")
                continue
            new_game.saveId = save_id
            print(
                f"\nCreated save '{new_game.saveName}' "
                f"for {new_game.player.name}."
            )
            return new_game

        if choice in {"2", "select", "select save"}:
            selected_game = _select_save()
            if selected_game is not None:
                print(
                    f"\nLoaded '{selected_game.saveName}' "
                    f"for {selected_game.player.name}."
                )
                return selected_game
            continue

        if choice in {"3", "delete", "delete save"}:
            _delete_save_menu()
            continue

        if choice in {"4", "exit", "quit"}:
            print("\nGoodbye!\n")
            raise SystemExit(0)

        print("Invalid choice. Enter 1, 2, 3, or 4.")
