import sys
from pathlib import Path
import shutil
import os
import subprocess
import yaml
import zipfile
import uuid
import re
import concurrent.futures

GLOBAL_ENV = {
    "$HOME": str(Path.home()) if "Path" in globals() else os.path.expanduser("~"),
    "$PWD": os.getcwd(),
    "$UUID": lambda: str(uuid.uuid4()),
    "$TRUE": True,
    "$FALSE": False,
    "$NULL": None
}

def arg_array(content: str, cli_args: list, loop_args: list = None) -> str:
    if loop_args is None:
        loop_args = []

    def replacer(match):
        has_dollar = match.group(1)
        index = int(match.group(2))
        
        if has_dollar:
            if 1 <= index <= len(cli_args):
                return str(cli_args[index - 1])
        else:
            if 1 <= index <= len(loop_args):
                return str(loop_args[index - 1])
        return match.group(0)

    pattern = r"(\$)?\[(\d+)\]"
    return re.sub(pattern, replacer, content)

def expand(value, cli_args=None):
    if cli_args is None:
        cli_args = []

    if isinstance(value, str):
        GLOBAL_ENV["$PWD"] = os.getcwd()

        for key, variable in GLOBAL_ENV.items():
            if callable(variable):
                while key in value:
                    value = value.replace(key, str(variable()), 1)
            else:
                value = value.replace(key, str(variable))        
        value = arg_array(value, cli_args)
        return value

    if isinstance(value, list):
        return [expand(item, cli_args) for item in value]

    if isinstance(value, dict):
        return {
            key: expand(item, cli_args)
            for key, item in value.items()
        }

    return value

def help_msg():
    print("usage: peyc <option|files> [args...]\n")
    print("option:")
    print("    help         show help message")
    print("    version      show newest version\n")
    print("Note: <files> must be use .yaml configuration file!")

class Version:
    scripts = os.path.dirname(os.path.abspath(__file__))
    FILES = os.path.join(scripts, "docs/CHANGELOG.txt")

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
    def move(args, cli_args):
        shutil.move(expand(args["from"], cli_args), expand(args["to"], cli_args))
        return 0
    
    @staticmethod
    def rename(args, cli_args):
        os.rename(expand(args["from"], cli_args), expand(args["to"], cli_args))
        return 0

    @staticmethod
    def copy(args, cli_args):
        source = Path(expand(args["from"], cli_args))
        destination = expand(args["to"], cli_args)

        if source.is_dir():
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)

        return 0

    @staticmethod
    def run(args, cli_args):
        cmd_str = expand(args["source"], cli_args)
        result = subprocess.run(cmd_str, shell=True)
        return result.returncode

    @staticmethod
    def echo(args, cli_args):
        print(expand(args["message"], cli_args))
        return 0

class Folder:
    @staticmethod
    def makedirs(args, cli_args):
        path = Path(expand(args.get("path", "."), cli_args))
        source = path / expand(args["name"], cli_args)
        source.mkdir(parents=True, exist_ok=True)
        return 0

    @staticmethod
    def removedirs(args, cli_args):
        path = Path(expand(args.get("path", "."), cli_args))
        source = path / expand(args["name"], cli_args)
        shutil.rmtree(source)
        return 0

class File:
    @staticmethod
    def touch(args, cli_args):
        source = Path(expand(args.get("path", "."), cli_args)) / expand(args["name"], cli_args)
        try:
            with open(source, "x", encoding="utf-8"):
                pass
        except Exception as e:
            print(f"{e}")
        return 0

    @staticmethod
    def rmfile(args, cli_args):
        source = Path(expand(args.get("path", "."), cli_args)) / expand(args["name"], cli_args)
        source.unlink()
        return 0

    @staticmethod
    def write(args, cli_args):
        path = Path(expand(args["path"], cli_args))
        source = expand(args.get("source", ""), cli_args)

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source, encoding='utf-8')
        return 0

    @staticmethod
    def append(args, cli_args):
        path = Path(expand(args["path"], cli_args))
        source = expand(args.get("source", ""), cli_args)

        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as file:
            file.write(source + "\n")
        return 0

    @staticmethod
    def override(args, cli_args):
        path = Path(expand(args["path"], cli_args))
        source = expand(args.get("source", ""), cli_args)

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source, encoding='utf-8')
        return 0

    @staticmethod
    def read(args, cli_args):
        source = Path(expand(args.get("path", "."), cli_args)) / expand(args["name"], cli_args)
        try:
            with open(source, "r", encoding="utf-8") as file:
                print(file.read())
        except Exception as e:
            print(f"{e}")
        return 0

class Directory:
    @staticmethod
    def cd(args, cli_args):
        os.chdir(expand(args["path"], cli_args))
        GLOBAL_ENV["$PWD"] = os.getcwd()
        print(os.getcwd())
        return 0

    @staticmethod
    def ls(args, cli_args):
        for i in os.listdir(expand(args["path"], cli_args)):
            print(i)
        return 0

class Wrapper:
    @staticmethod
    def archive(args, cli_args):
        root = expand(args.get("path", "."), cli_args)
        base = os.path.splitext(expand(args["name"], cli_args))[0]
        shutil.make_archive(base, 'zip', root)
        return 0

    @staticmethod
    def extract(args, cli_args):
        root = expand(args.get("path", "."), cli_args)
        base = expand(args["name"], cli_args)

        with zipfile.ZipFile(base, "r") as zip:
            zip.extractall(root)
        return 0

class Variable:
    @staticmethod
    def variable(args, cli_args):
        name = expand(args["name"], cli_args)
        key = name if name.startswith("$") else f"${name}"
        GLOBAL_ENV[key] = expand(args["value"], cli_args)
        return 0

class Flow:
    @staticmethod
    def loops(args, cli_args):
        if not isinstance(args, dict):
            print("Error: 'for' arguments must be a mapping (dict)!")
            return 1

        var_name = args.get("var", "i")
        count = args.get("count")
        steps = args.get("do", [])

        if isinstance(steps, dict):
            steps = [steps]

        if not isinstance(steps, list):
            print("Error: 'do' inside 'for' must be a list of commands!")
            return 1

        try:
            c = int(expand(count, cli_args))
        except (TypeError, ValueError):
            print("Error: 'count' must be a valid integer")
            return 1

        def replacer(obj, var_name, value):
            target = f"[{var_name}]"
            if isinstance(obj, str):
                return obj.replace(target, str(value))
            elif isinstance(obj, list):
                return [replacer(item, var_name, value) for item in obj]
            elif isinstance(obj, dict):
                return {k: replacer(v, var_name, value) for k, v in obj.items()}
            return obj

        for i in range(1, c + 1):
            process = replacer(steps, var_name, i)
            execute(process, cli_args)

        return 0

    @staticmethod
    def sync(args, cli_args):
        if not isinstance(args, dict):
            print("Error: 'sync' block must contain command mappings!")
            return 1

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            
            for cmd_name, cmd_val in args.items():
                single_task = [{cmd_name: cmd_val}]
                futures.append(executor.submit(execute, single_task, cli_args))
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error in sync task: {e}")

        return 0
    
    def condition(args, cli_args):
        if not isinstance(args, dict):
            print("Error: 'if' block must contain command mappings!")
            return 1

        condition_expr = args.get("if")
        steps = args.get("do", [])

        if isinstance(steps, dict):
            steps = [steps]

        if not isinstance(steps, list):
            print("Error: 'do' inside 'if' must be a list or mapping of commands!")
            return 1

        expanded = expand(str(condition_expr), cli_args)

        try:
            is_true = eval(expanded, {"__builtins__": {}}, GLOBAL_ENV)
        except Exception as e:
            print(f"{e}")

        if is_true:
            execute(steps, cli_args)

commands = {
    "move": Basic.move,
    "rename": Basic.rename,
    "copy": Basic.copy,
    "run": Basic.run,
    "echo": Basic.echo,
    "mkdir": Folder.makedirs,
    "rmdir": Folder.removedirs,
    "touch": File.touch,
    "rmfile": File.rmfile,
    "read": File.read,
    "cd": Directory.cd,
    "ls": Directory.ls,
    "archive": Wrapper.archive,
    "extract": Wrapper.extract,
    "set": Variable.variable,
    "write": File.write,
    "append": File.append,
    "override": File.override,
    "for": Flow.loops,
    "sync": Flow.sync,
    "if": Flow.condition
}

def execute(config, cli_args):
    for items in config:
        if not isinstance(items, dict):
            raise ValueError(f"invalid command format: {items}")

        for command, args in items.items():
            if command not in commands:
                raise ValueError(f"Unknown command '{command}'")

            if command != "for" and not isinstance(args, dict):
                raise ValueError(
                    f"arguments for '{command}' must be a mapping!"
                )

            args = expand(args, cli_args)
            commands[command](args, cli_args)

    return 0

def main():
    if len(sys.argv) < 2:
        print("usage: peyc <option|files> [args...]")
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

    cli_args = sys.argv[2:]

    try:
        config = yaml.safe_load(content)
        return execute(config, cli_args)
    
    except yaml.YAMLError as e:
        print(f"{e}")
        return 1

    except (KeyError, TypeError, ValueError, OSError,
            subprocess.SubprocessError) as e:
        print(f"{e}")
        return 1

if __name__ == "__main__":
    main()