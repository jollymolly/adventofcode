#!python3

import sys

_TREE = '#'


def main():

    if len(sys.argv) != 2:
        print(f"cmd line: {sys.argv[0]} <input_file>")
        return 1

    tree_count = None
    
    with open(sys.argv[1]) as inp:
        x_max = len(inp.readline().strip())
        tree_count = sum(int(l[y * 3 % x_max] == _TREE) for y, l in enumerate(map(str.strip, inp), 1))

    print(f"Answer: {tree_count}.")

    return 0

if __name__ == "__main__":
    sys.exit(main())
