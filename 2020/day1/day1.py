#!python3

import sys

_TARGET_NUM = 2020

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(f"cmd: {sys.argv[0]} <filename>")
        sys.exit(1)

    with open(sys.argv[1]) as inp:
        nums = tuple(int(i) for i in inp)

    len_nums = len(nums)

    if len_nums < 2:
        print(f"Not enough input values: {len_nums}.")
        sys.exit(2)
        
    answer = next(
        (nums[n1] * nums[n2] * nums[n3]
         for n1 in range(len_nums-2)
         for n2 in range(n1+1, len_nums-1)
         for n3 in range(n2+1, len_nums)
         if nums[n1] + nums[n2] + nums[n3] == _TARGET_NUM),
        None
    )

    print(f"Answer: {answer}.")

