import sys
from pathlib import Path
import yaml

def help_msg():
    print("usage: peyc <option|files>\n")
    print("option:")
    print("    help         show help message")
    print("    version      show newest version\n")
    print("Note: <files> must be use .yaml configuration file!")

class Version:
    FILES = "CHANGELOG.txt"

    @staticmethod
    def get_latest(files: str):
        blocks = [
            b.strip()
            for b in files.strip().split("\n\n")
            if b.strip()
        ]

        if not blocks:
            return None

        latest = blocks[-1]
        return latest

    @staticmethod
    def version():
        try:
            with open(Version.FILES, "r") as file:
                content = file.read()
                print(Version.get_latest(content))
        except FileNotFoundError as e:
            print(f"{e}")

class Files:
    @staticmethod
    def is_yaml(file_path: str) -> bool:
        path = Path(file_path)
        if path.suffix.lower() not in [".yaml", ".yml"]:
            print(f"Error: '{file_path}' is not a .yaml or .yml file!")
            return False
        return True

    @staticmethod
    def is_exists(file_path: str) -> bool:
        path = Path(file_path)
        if not path.exists():
            print(f"Error: '{file_path}' does not exist!")
            return False
        return True

    @staticmethod
    def is_file(file_path: str) -> bool:
        path = Path(file_path)
        if not Files.is_exists(file_path):
            return False
            
        if not path.is_file():
            print(f"Error: '{file_path}' is not a file (might be a directory)!")
            return False
        return True

    @staticmethod
    def reading(file_path: str):
        if not Files.is_file(file_path):
            return None

        if not Files.is_yaml(file_path):
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            print(f"{e}")
            return None

def main():
    if len(sys.argv) < 2:
        help_msg()
        return 1

    cmd = sys.argv[1]

    if cmd == "help":
        help_msg()
        return 0
    elif cmd == "version":
        Version.version()
        return 0

    content = Files.reading(cmd)
    if content is None or not content:
        return 1

    try:
        config = yaml.safe_load(content)
        return config
    except yaml.YAMLError as e:
        print(f"{e}")

if __name__ == "__main__":
    main()