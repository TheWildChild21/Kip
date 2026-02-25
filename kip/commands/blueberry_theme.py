import os
import json
import glob
import platform
from datetime import datetime


BLUEBERRY_SCHEME =     {
  "name": "Banana Blueberry",
  "black": "#17141f",
  "red": "#ff6b7f",
  "green": "#00bd9c",
  "yellow": "#e6c62f",
  "blue": "#22e8df",
  "purple": "#dc396a",
  "cyan": "#56b6c2",
  "white": "#f1f1f1",
  "brightBlack": "#495162",
  "brightRed": "#fe9ea1",
  "brightGreen": "#98c379",
  "brightYellow": "#f9e46b",
  "brightBlue": "#91fff4",
  "brightPurple": "#da70d6",
  "brightCyan": "#bcf3ff",
  "brightWhite": "#ffffff",
  "background": "#191323",
  "foreground": "#cccccc",
  "selectionBackground": "#220525",
  "cursorColor": "#e07d13"
}


def find_windows_terminal_settings():
    base = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Packages")
    pattern = os.path.join(
        base,
        "Microsoft.WindowsTerminal*",
        "LocalState",
        "settings.json"
    )
    matches = glob.glob(pattern)
    return matches[0] if matches else None


def backup_settings(path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = path.replace("settings.json", f"settings_backup_{timestamp}.json")
    with open(path, "r", encoding="utf-8") as original:
        with open(backup_path, "w", encoding="utf-8") as backup:
            backup.write(original.read())
    return backup_path


def apply_blueberry_theme():
    if platform.system() != "Windows":
        print("This theme command only supports Windows.")
        return

    settings_path = find_windows_terminal_settings()

    if not settings_path:
        print("Windows Terminal not found.")
        return

    with open(settings_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    backup_path = backup_settings(settings_path)

    if "schemes" not in data:
        data["schemes"] = []

    if not any(s["name"] == BLUEBERRY_SCHEME["name"] for s in data["schemes"]):
        data["schemes"].append(BLUEBERRY_SCHEME)

    if "profiles" not in data:
        data["profiles"] = {}

    if "defaults" not in data["profiles"]:
        data["profiles"]["defaults"] = {}

    data["profiles"]["defaults"]["colorScheme"] = BLUEBERRY_SCHEME["name"]

    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("Blueberry theme applied successfully.")   
    print(f"Backup created at: {backup_path}")
    print("Restart Windows Terminal to see changes.")



def run(args=None):
    apply_blueberry_theme()