#!python3

import sys


def main(args):

    if len(args) != 2:
        print(f"Cmd line: {args[0]} <input_file>")
        return 1

    with open(args[1]) as inp:
        pass
    
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
