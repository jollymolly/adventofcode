#!python3

import sys

_REQUIRED_FIELDS = frozenset(("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", ))


def _is_valid_passport_data(data):
    return _REQUIRED_FIELDS - frozenset(data) == frozenset()


def validate(filename: str):

    valid_entries = 0

    with open(filename) as inp:

        entry = {}
        
        for line in map(str.strip, inp):
            
            if line == '':
                if entry:
                    valid_entries += 1 if _is_valid_passport_data(entry) else 0
                    entry.clear()
                continue

            entry.update(dict(p.strip().split(':') for p in line.split(' ')))

        valid_entries += 1 if entry and _is_valid_passport_data(entry) else 0

    return valid_entries


def main(args):

    if len(args) != 2:
        print(f"Cmd line: {args[0]} <input_file>")
        return 1

    answer = validate(args[1])
    print(f"Answer: {answer}.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
