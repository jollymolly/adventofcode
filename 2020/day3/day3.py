#!python3

import sys
import functools

_TREE = '#'


def main():

    if len(sys.argv) != 2:
        print(f"cmd line: {sys.argv[0]} <input_file>")
        return 1

    tree_map = None
    
    with open(sys.argv[1]) as inp:
        tree_map = tuple(map(str.strip, inp))

    if not tree_map:
        print("No input found.")
        return 3

    x_max, y_max = len(tree_map[0]), len(tree_map)

    slopes_trees = (
        sum(
            tree_map[y][x % x_max] == _TREE
            for x, y in zip(range(x_steps, y_max//y_steps*x_steps, x_steps), range(y_steps, y_max, y_steps))
        ) for x_steps, y_steps in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2), )
    )
    tree_count = functools.reduce(lambda s1, s2: s1 * s2, slopes_trees, 1)

    print(f"Answer: {tree_count}.")

    return 0

if __name__ == "__main__":
    sys.exit(main())
