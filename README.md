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
- exit => status
- echo => message

### Variable
- set => name, value
- $ -> argument access

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
- pwd

### Pattern Search
- search => keyword, from

### Compression file
- archive => name, path
- extract => name, path?