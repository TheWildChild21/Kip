import os
import json
import glob
import platform
from datetime import datetime


MINT_SCHEME = {
  "name": "Mint Eclipse",
  "black": "#000000",
  "red": "#cc0000",
  "green": "#008f4c",
  "yellow": "#8a6f00",
  "blue": "#005f87",
  "purple": "#5f00af",
  "cyan": "#006b6b",
  "white": "#0D0D0D",
  "brightBlack": "#444444",
  "brightRed": "#ff3333",
  "brightGreen": "#00c853",
  "brightYellow": "#a88400",
  "brightBlue": "#1e90ff",
  "brightPurple": "#8a2be2",
  "brightCyan": "#008b8b",
  "brightWhite": "#0D0D0D",
  "background": "#d8fbe2",
  "foreground": "#000000",
  "selectionBackground": "#b2f2c9",
  "cursorColor": "#006d3c"
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


def apply_mint_theme():
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

    if not any(s["name"] == MINT_SCHEME["name"] for s in data["schemes"]):
        data["schemes"].append(MINT_SCHEME)

    if "profiles" not in data:
        data["profiles"] = {}

    if "defaults" not in data["profiles"]:
        data["profiles"]["defaults"] = {}

    data["profiles"]["defaults"]["colorScheme"] = MINT_SCHEME["name"]

    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("Mint Eclipse theme applied successfully.")
    print(f"Backup created at: {backup_path}")
    print("Restart Windows Terminal to see changes.")



def run(args=None):
    apply_mint_theme()