import os
import json
import glob
import platform
from datetime import datetime


NEON_SCHEME = {
  "name": "Neon",
  "black": "#000000",
  "red": "#ff3045",
  "green": "#5ffa74",
  "yellow": "#fffc7e",
  "blue": "#0208cb",
  "purple": "#f924e7",
  "cyan": "#00fffc",
  "white": "#c7c7c7",
  "brightBlack": "#686868",
  "brightRed": "#ff5a5a",
  "brightGreen": "#75ff88",
  "brightYellow": "#fffd96",
  "brightBlue": "#3c40cb",
  "brightPurple": "#f15be5",
  "brightCyan": "#88fffe",
  "brightWhite": "#ffffff",
  "background": "#14161a",
  "foreground": "#00fffc",
  "selectionBackground": "#0013ff",
  "cursorColor": "#c7c7c7"
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


def apply_neon_theme():
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

    if not any(s["name"] == NEON_SCHEME["name"] for s in data["schemes"]):
        data["schemes"].append(NEON_SCHEME)

    if "profiles" not in data:
        data["profiles"] = {}

    if "defaults" not in data["profiles"]:
        data["profiles"]["defaults"] = {}

    data["profiles"]["defaults"]["colorScheme"] = NEON_SCHEME["name"]

    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("Neon theme applied successfully.")
    print(f"Backup created at: {backup_path}")
    print("Restart Windows Terminal to see changes.")



def run(args=None):
    apply_neon_theme()