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
        
    n1, n2 = None, None

    try:
        for n1 in range(len_nums-1):
            n1_num = nums[n1]
            for n2 in range(n1+1, len_nums):
                if n1_num + nums[n2] == _TARGET_NUM:
                    raise StopIteration("Found target numbers.")
    except StopIteration:
        pass
    
    print(f"num1[{n1}]: {nums[n1]}; num2[{n2}]: {nums[n2]}.")
    print("result: {0}".format(nums[n1] * nums[n2] if n1 is not None and n2 is not None else None))

