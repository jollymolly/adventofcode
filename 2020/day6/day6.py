#!python3

import sys


def main(args):

    if len(args) != 2:
        print(f"Cmd line: {args[0]} <input_file>")
        return 1

    yes_count = 0

    with open(args[1]) as inp:
        
        group_answers, group_start = set(), True
        
        for line in inp:

            if line == '\n':
                yes_count += len(group_answers)
                group_answers, group_start = set(), True
            else:
                person_answers = set(line.strip())
                if group_start is True and not group_answers:
                    group_answers = person_answers
                else:
                    group_answers &= person_answers
                group_start = False

        yes_count += len(group_answers)

    print(f"Answer: {yes_count}.")
            
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
