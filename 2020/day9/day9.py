#!python3

import sys

_PREAMBLE = 25


def main(args):

    if len(args) != 2:
        print(f"Cmd line: {args[0]} <input_file>")
        return 1

    numbers = None 
    with open(args[1]) as inp:
        numbers = tuple(map(int, map(str.strip, inp)))

    for i in range(_PREAMBLE + 1, len(numbers)):
        n = next(
            (
                1
                for k in range(i - _PREAMBLE, i-1)
                for m in range(k + 1, i)
                if numbers[i] == numbers[k] + numbers[m]
            ),
            None
        )
        if n is None:
            break

    num = numbers[i]

    try:
        for i in range(len(numbers) - 1):
            for j in range(i + 1, len(numbers)):
                seq = numbers[i:j]
                s = sum(seq)

                if s == num:
                    m, x = min(seq), max(seq)
                    raise StopIteration
                elif s > num:
                    break
                
    except StopIteration:
        print(f"Answer: {m + x}.")
        
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
