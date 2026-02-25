import os
import json
import glob
import platform
from datetime import datetime


MATRIX_SCHEME =    {
  "name": "matrix",
  "black": "#0f191c",
  "red": "#23755a",
  "green": "#82d967",
  "yellow": "#ffd700",
  "blue": "#3f5242",
  "purple": "#409931",
  "cyan": "#50b45a",
  "white": "#507350",
  "brightBlack": "#688060",
  "brightRed": "#2fc079",
  "brightGreen": "#90d762",
  "brightYellow": "#faff00",
  "brightBlue": "#4f7e7e",
  "brightPurple": "#11ff25",
  "brightCyan": "#c1ff8a",
  "brightWhite": "#678c61",
  "background": "#0f191c",
  "foreground": "#426644",
  "selectionBackground": "#18282e",
  "cursorColor": "#384545"
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


def apply_matrix_theme():
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

    if not any(s["name"] == MATRIX_SCHEME["name"] for s in data["schemes"]):
        data["schemes"].append(MATRIX_SCHEME)

    if "profiles" not in data:
        data["profiles"] = {}

    if "defaults" not in data["profiles"]:
        data["profiles"]["defaults"] = {}

    data["profiles"]["defaults"]["colorScheme"] = MATRIX_SCHEME["name"]

    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("Matrix theme applied successfully.")     
    print(f"Backup created at: {backup_path}")
    print("Restart Windows Terminal to see changes.")



def run(args=None):
    apply_matrix_theme()