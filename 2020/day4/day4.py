#!python3

import sys

_REQUIRED_FIELDS = frozenset(("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", ))

_VALIDATORS = {
    "byr": lambda v: len(v) == 4 and v.isnumeric() and 1920 < int(v) <= 2002,
    "iyr": lambda v: len(v) == 4 and v.isnumeric() and 2010 <= int(v) <= 2020,
    "eyr": lambda v: len(v) == 4 and v.isnumeric() and 2020 <= int(v) <= 2030,
    "hgt": lambda v: v[-2:] in frozenset(("cm", "in", )) and (v[-2:] == "cm" and 150 <= int(v[:-2]) <= 193 or 59 <= int(v[:-2]) <= 76),
    "hcl": lambda v: v[0] == '#' and len(v[1:]) == 6 and all(ch in frozenset("abcdef0123456789") for ch in v[1:]),
    "ecl": lambda v: v in frozenset(("amb", "blu", "brn", "gry", "grn", "hzl", "oth")),
    "pid": lambda v: v.isnumeric() and len(v) == 9
}


def _is_valid_passport_data(data):
    return _REQUIRED_FIELDS - frozenset(data) == frozenset() \
        and all(_VALIDATORS[k](v.strip()) is True for k, v in data.items() if k in _VALIDATORS)

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
