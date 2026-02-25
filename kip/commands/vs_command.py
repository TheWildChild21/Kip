import json


def run(args):
    with open("commands/version.json", encoding="utf-8") as f:
        version_info = json.load(f)
    print(f"Kip CLI Version: {version_info['version']}")