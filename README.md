# shredir.py
Truncate name and remove directory like "shred -u"

# Usage
```
usage: shredir.py [-h] [-c COUNT] [-u] [-v] [-z] directory

positional arguments:
  directory             Directory

optional arguments:
  -h, --help            show this help message and exit
  -n COUNT, --iterations COUNT
                        Overwrite count (Default: 3)
  -u, --remove          Truncate and remove directory after overwriting (Default: True)
  -v, --verbose         Verbose output
  -z, --zero            Add a final overwrite directory name with zeros (Default: True)
```

# Example
Remove directory
```bash
shredir.py /path/to/directory
```

Recurcive remove directories in current directory
```
# Before you need remove all files in directory
find . -type f -print0 | xargs -0 shred -uz

# Recursively remove directory
for DIRECTORY in `find . -type d | egrep -v '^\.$'`
do
shredir $DIRECTORY
done
```
