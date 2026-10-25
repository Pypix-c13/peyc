## peyc - Python Easy YAML Configuration
- Solves my problems in creating project templates in Bash.
- Makes project template creation much more efficient.
- Serves as a future portfolio.
- Builds useful system automation for the future.

## Design Syntax
### Basic
- move => from, to
- rename => from, to
- copy => from, to
- run => source
- echo => message

### Variable
- set => name, value
- $ -> argument access
- $PWD
- $HOME

### Folder
- mkdir => name, path?
- rmdir => name, path?

### File
- touch => name, path?
- rmfile => name, path?
- write => name, source, path?
- append => name, source, path?
- override => name, source, path?
- read => name, path?

### Directory
- cd => path
- ls => path

### Compression file
- archive => name, path?
- extract => name, path?

## Version
```
[10.23.2026:18.40] peyc 1.0 : Basic feature
    - added command line like help and version
    - added file reading
    - support .yaml or .yml files
```

```
[10.23.2026:22.48] peyc 2.0 : Basic feature
    - added `move`, `rename`, `copy`, `run`, `exit`, `echo` keyword
    - fix help message
```

```
[10.24.2026:18.53] peyc 3.0 : Folder feature
    - added `mkdir`, `rmdir` keyword
```

```
[10.24.2026:19.43] peyc 4.0 : Some Files feature
    - added `touch`, `rmfile`, `read` keyword
```

```
[10.24.2026:20.29] peyc 5.0 : Directory feature
    - added `cd`, `ls` keyword
```

```
[10.24.2026:21.24] peyc 6.0 : Removing
    - removed `exit`, `search`
    - change pwd to $PWD
    - added $HOME
```

```
[10.24.2026:21.50] peyc 7.0 : Placeholder
    - added $PWD and $HOME to global variable
```

```
[10.24.2026:22.01] peyc 8.0 : Bug fixed
    - fix recursion error
```

```
[10.25.2026:13.45] peyc 9.0 : Compression File
    - added `archive`, `extract` keyword
    - only work for .zip file
```

```
[10.25.2026:14.01] peyc 10 : Variable feature
    - added `set` keyword
    - support variable access with $
```