import os
import sys
import json

BASE_DIR = os.path.dirname(__file__)
sys.path.append(BASE_DIR)

commands_path = os.path.join(BASE_DIR, "commands", "commands.json")
with open(commands_path, encoding="utf-8") as f:
    COMMANDS = json.load(f)


def main(): 
    print("Kip CLI is ready! Type the command \"welcome\" to get started.🐼")
    while True:
        user_input = input(">>> ").strip().split()
        if not user_input:
            continue
        command_name = user_input[0]
        args = user_input[1:]

        module_path = COMMANDS.get(command_name)

        if module_path == "exit":
            break
        elif module_path:
            try:
                module = __import__(module_path, fromlist=['run'])
                if hasattr(module, "run"):
                    module.run(args)
                else:
                    print("Command has no run() function.")
            except ModuleNotFoundError:
                print(f"Module {module_path} not found.")
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()