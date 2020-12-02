#!python3

import sys


def parse(line: str):

    desc, pwd = line.split(':')
    rng, ch = desc.split(' ')
    min, max = rng.split('-')
    
    return int(min), int(max), ch, pwd.strip()


def validate(min: int, max: int, ch: str, pwd: str) -> int:
    
    ch_count = pwd.count(ch)
    return int(min <= ch_count and ch_count <= max)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(f"cmd line: {sys.argv[0]} <filename>")
        sys.exit(1)

    valid_pwd_count = 0

    with open(sys.argv[1]) as inp:
        for line in inp:
            min, max, ch, pwd = parse(line)
            valid_pwd_count += validate(min, max, ch, pwd)

    print(f"Answer: {valid_pwd_count}.")

