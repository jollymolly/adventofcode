#!python3

import sys


def parse(line: str):

    desc, pwd = line.split(':')
    rng, ch = desc.split(' ')
    pos1, pos2 = rng.split('-')
    
    return int(pos1)-1, int(pos2)-1, ch, pwd.strip()


def validate(pos1: int, pos2: int, ch: str, pwd: str) -> int:
    
    pos1_ch, pos2_ch = pwd[pos1], pwd[pos2]
    return int(pos1_ch != pos2_ch and (pos1_ch == ch or pos2_ch == ch))


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(f"cmd line: {sys.argv[0]} <filename>")
        sys.exit(1)

    valid_pwd_count = 0

    with open(sys.argv[1]) as inp:
        for line in inp:
            pos1, pos2, ch, pwd = parse(line)
            valid_pwd_count += validate(pos1, pos2, ch, pwd)

    print(f"Answer: {valid_pwd_count}.")

