#!/usr/bin/env python3

# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:



import argparse
import os
import sys


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Remove directory")
    parser.add_argument("-n", "--iterations", type=int, default=3, help="Overwrite N times instead of the default (Default: 3)")
    parser.add_argument("-u", "--remove", action="store_const", const="remove", help="Truncate and remove directory after overwriting (Default: True)")
    parser.add_argument("-v", "--verbose", action="store_const", const="verbose", help="Verbose output")
    parser.add_argument("-z", "--zero", action="store_const", const="zero", help="Add a final overwrite directory name with zeros (Default: True)")
    parser.add_argument("--random-source", type=str, default="/dev/urandom", help="Get random bytes from FILE (Default: /dev/urandom)")
    parser.add_argument("directory", nargs=1, type=str, help="Directory")
    arguments = parser.parse_args()

    # Get arguments
    directory = arguments.directory[0]
    count = arguments.iterations
    remove = False if False == arguments.verbose else True
    verbose = bool(arguments.verbose)
    zero = False if False == arguments.verbose else True
    random_source = arguments.random_source
    
    # Check directory
    if directory:
        if not os.path.isdir(directory):
            print('"{0}" is not directory.'.format(directory), file=sys.stderr)
            sys.exit(1)

        if len(os.listdir(directory)):
            print('"{0}" is not empty.'.format(directory), file=sys.stderr)
            sys.exit(1)

    if not os.access(random_source, os.R_OK):
        print('"{0}" is not readable.'.format(random_source), file=sys.stderr)
        sys.exit(1)

    # Execute rename
    filename = os.path.basename(__file__)
    size = len(directory.encode())
    total = count + 1 if zero else 0
    current_name = directory
    with open("/dev/urandom", "rb") as random:
        for current in range(0, count):
            if verbose:
                print("{0}: {1}: pass {2}/{3} (random)...".format(filename, directory, current + 1, total))
            new_name = random.read(size)
            os.rename(current_name, new_name)
            current_name = new_name

    if zero:
        if verbose:
            print("{0}: {1}: pass {2}/{3} (000000)...".format(filename, directory, total, total))
        new_name = "0" * size
        os.rename(current_name, new_name)
        current_name = new_name

    if remove:
        while size:
            new_name = "0" * size
            os.rename(current_name, new_name)
            current_name = new_name
            size = size - 1
            if verbose:
                print("{0}: {1}: renamed to {2}".format(filename, current_name + "0", current_name))

        os.rmdir(current_name)
        if verbose:
            print("{0}: {1}: removed".format(filename, current_name))

