import os
import json
import glob
import platform
from datetime import datetime


MIDNIGHT_SCHEME = {
  "name": "Night City",
  "black": "#283034",
  "red": "#FF0000",
  "green": "#00FF80",
  "yellow": "#FFD400",
  "blue": "#E388FF",
  "purple": "#9900FF",
  "cyan": "#00E5FF",
  "white": "#6600FF",
  "brightBlack": "#FF1998",
  "brightRed": "#FF006E",
  "brightGreen": "#83FF52",
  "brightYellow": "#E5FF00",
  "brightBlue": "#42C6FF",
  "brightPurple": "#FF2AFC",
  "brightCyan": "#3DD8FF",
  "brightWhite": "#F4F6F9",
  "background": "#090819",
  "foreground": "#6600FF",
  "selectionBackground": "#4A7AFF",
  "cursorColor": "#00FFFF"
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


def apply_midnight_theme():
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

    if not any(s["name"] == MIDNIGHT_SCHEME["name"] for s in data["schemes"]):
        data["schemes"].append(MIDNIGHT_SCHEME)

    if "profiles" not in data:
        data["profiles"] = {}

    if "defaults" not in data["profiles"]:
        data["profiles"]["defaults"] = {}

    data["profiles"]["defaults"]["colorScheme"] = MIDNIGHT_SCHEME["name"]

    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("Neon theme applied successfully.")
    print(f"Backup created at: {backup_path}")
    print("Restart Windows Terminal to see changes.")



def run(args=None):
    apply_midnight_theme()