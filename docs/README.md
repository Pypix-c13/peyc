## peyc - Python Easy YAML Configuration
- Solves my problems in creating project templates in Bash.
- Makes project template creation much more efficient.
- Serves as a future portfolio.
- Builds useful system automation for the future.

## Design Syntax

### Basic

```yaml
- move:
    from: "$HOME/Downloads/downloads.txt"
    to: "$HOME/Desktop/downloads.txt"

- rename:
    from: "$HOME/Downloads/downloads.txt"
    to: "$HOME/Downloads/loads.txt"

- copy:
    from: "$HOME/Downloads/downloads.txt"
    to: "$HOME/Desktop/downloads.txt"

- run:
    source: "echo Hello, World"

- echo:
    message: "Hello, World"
```

### Variable

```yaml
- set:
    name: "project_dir"
    value: "$HOME/Projects/my_app"

- echo:
    message: "Current working directory is $PWD and Home is $HOME"
```

### Folder

```yaml
- mkdir:
    name: "my_folder"
    path: "$HOME/Desktop"

- rmdir:
    name: "old_folder"
    path: "$HOME/Desktop"
```

### File

```yaml
- touch:
    name: "config.json"
    path: "$HOME/Desktop"

- rmfile:
    name: "temp.txt"
    path: "$HOME/Desktop"

- write:
    path: "$HOME/Desktop/script.py"
    source: |
      def main():
          print("Hello from peyc!")
      if __name__ == "__main__":
          main()

- append:
    path: "$HOME/Desktop/log.txt"
    source: "Log line appended successfully."

- override:
    path: "$HOME/Desktop/script.py"
    source: "print('Overwritten content')"

- read:
    name: "config.json"
    path: "$HOME/Desktop"
```

### Directory

```yaml
- cd:
    path: "$HOME/Desktop"

- ls:
    path: "$HOME/Projects"
```

### Compression file

```yaml
- archive:
    name: "backup.zip"
    path: "$HOME/Desktop/my_project"

- extract:
    name: "backup.zip"
    path: "$HOME/Desktop/extracted"
```

### Control Flow

```yaml
- for:
    var: "i"
    count: 3
    do:
        # do whatever you want

- if: "$TRUE"
    do:
        # do whatever you want
```

### Sync

```yaml
- sync:
    # do whatever you want
```

## Version

```text
[10.23.2026:18.40] peyc 1 : Basic feature
    - added command line like help and version
    - added file reading
    - support .yaml or .yml files
```

```text
[10.23.2026:22.48] peyc 2 : Basic feature
    - added `move`, `rename`, `copy`, `run`, `exit`, `echo` keyword
    - fix help message
```

```text
[10.24.2026:18.53] peyc 3 : Folder feature
    - added `mkdir`, `rmdir` keyword
```

```text
[10.24.2026:19.43] peyc 4 : Some Files feature
    - added `touch`, `rmfile`, `read` keyword
```

```text
[10.24.2026:20.29] peyc 5 : Directory feature
    - added `cd`, `ls` keyword
```

```text
[10.24.2026:21.24] peyc 6 : Removing
    - removed `exit`, `search`
    - change pwd to $PWD
    - added $HOME
```

```text
[10.24.2026:21.50] peyc 7 : Placeholder
    - added $PWD and $HOME to global variable
```

```text
[10.24.2026:22.01] peyc 8 : Bug fixed
    - fix recursion error
```

```text
[10.25.2026:13.45] peyc 9 : Compression File
    - added `archive`, `extract` keyword
    - only work for .zip file
```

```text
[10.25.2026:14.01] peyc 10 : Variable feature
    - added `set` keyword
    - support variable access with $
```

```text
[10.25.2026:14.19] peyc 11 : File manipulation feature
    - added `write`, `append`, `override` keyword
```

```
[10.25.2026:14.39] peyc 12 : Prettier Update
    - polished README.md structure and formatting
    - added clean YAML examples for showcase
```

```
[10.26.2026:17.29] peyc 13 : UUID Update
    - added $UUID
```

```
[10.26.2026:22.21] peyc 14 : Control Flow Update
    - added for keyword
    - change some code structure
    - added argument input with $[] use zero-based indexing
```

```
[10.27.2026:17.31] peyc 15 : For key Update
    - Added `var`, `count`, and `do` properties to the `for` statement
    - Added support for array indexing use []
    - Changed code structure for better flow
    - Updated documentation
```

```
[10.27.2026:18.30] peyc 16 : Paralel Update
    - added sync keyword
    - added paralel system
    - changed some code structure
```

```
[10.28.2026:16.16] peyc 17 : Condition Update
    - added if keyword
    - added $TRUE, $FALSE, $NULL
    - expression support
```

```
[10.28.2026:22.02] peyc 18 : Version Update
    - changed versioning from `x.y` to `x`
    - `x` version just for development versioning
    - release versioning use `x.y.z`
```