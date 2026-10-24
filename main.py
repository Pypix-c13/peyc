import sys
from pathlib import Path
import shutil
import os
import subprocess
import yaml

def help_msg():
    print("usage: peyc <option|files>\n")
    print("option:")
    print("    help         show help message")
    print("    version      show newest version\n")
    print("Note: <files> must be use .yaml configuration file!")

class Version:
    FILES = "docs/CHANGELOG.txt"

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

class Basic:
    @staticmethod
    def move(args):
        shutil.move(Path(args["from"]), Path(args["to"]))
        return 0
    
    @staticmethod
    def rename(args):
        os.rename(args["from"], args["to"])
        return 0

    @staticmethod
    def copy(args):
        source = Path(args["from"])
        destination = args["to"]

        if source.is_dir():
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)

        return 0

    @staticmethod
    def run(args):
        result = subprocess.run(args["source"], shell=True)
        return result.returncode

    @staticmethod
    def exit(args):
        status = args["status"]

        if status < 0:
            print("'status' must be non-negative!")
            return 1

        sys.exit(int(status))

    @staticmethod
    def echo(args):
        print(args["message"])
        return 0

class Folder:
    @staticmethod
    def makedirs(args):
        path = Path(args.get("path", "."))
        source = path / args["name"]
        source.mkdir(parents=True, exist_ok=True)
        return 0

    @staticmethod
    def removedirs(args):
        path = Path(args.get("path", "."))
        source = path / args["name"]
        shutil.rmtree(source)
        return 0

# some
class File:
    @staticmethod
    def touch(args):
        source = Path(args.get("path", ".")) / args["name"]
        try:
            with open(source, "x") as file:
                file.close()
        except Exception as e:
            print(f"{e}")
        return 0

    @staticmethod
    def rmfile(args):
        source = Path(args.get("path", ".")) / args["name"]
        source.unlink()
        return 0

    @staticmethod
    def read(args):
        source = Path(args.get("path", ".")) / args["name"]
        try:
            with open(source, "r") as file:
                print(file.read())
        except Exception as e:
            print(f"{e}")
        return 0

class Directory:
    @staticmethod
    def cd(args):
        os.chdir(args["path"])
        print(os.getcwd())
        return 0

    @staticmethod
    def ls(args):
        for i in os.listdir(args["path"]):
            print(i)

commands = {
    "move": Basic.move,
    "rename": Basic.rename,
    "copy": Basic.copy,
    "run": Basic.run,
    "exit": Basic.exit,
    "echo": Basic.echo,
    "mkdir": Folder.makedirs,
    "rmdir": Folder.removedirs,
    "touch": File.touch,
    "rmfile": File.rmfile,
    "read": File.read,
    "cd": Directory.cd,
    "ls": Directory.ls
}

def execute(config):
    for items in config:
        if not isinstance(items, dict):
            raise ValueError(f"invalid command format: {items}")

        command, args = next(iter(items.items()))
        if command not in commands:
            raise ValueError(f"Unknown command '{command}'")

        if not isinstance(args, dict):
            raise ValueError(
                f"arguments for '{command}' must be a mapping!"
            )

        commands[command](args)

    return 0

def main():
    if len(sys.argv) < 2:
        print("usage: peyc <option|files>")
        print("use 'peyc help' for more information")
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
        return execute(config)
    
    except yaml.YAMLError as e:
        print(f"{e}")
        return 1

    except (KeyError, TypeError, ValueError, OSError,
            subprocess.SubprocessError) as e:
        print(f"{e}")
        return 1

if __name__ == "__main__":
    main()