#!python3

import datetime
import multiprocessing


def calculate(signal, offset, len, signal_len):

    s = 0
    por = offset+1
    inc = por*2
    m = 1
    for i in range(offset, signal_len, inc):
        s = sum(signal[i: inc]) * m
        m *= -1
    s = abs(s)
    for i in range(offset, signal_len):
        signal[i], s = s % 10, s-signal[i]

        
if __name__ == "__main__":

    signal = None
    with open("input.txt") as f:
        signal = list(map(int, f.readline().strip()))

    if not signal:
        print("No signal.")

    phase = 1

    offset = int("".join(map(str, signal[:7])))
    signal = signal * 10**4
    signal_len = len(signal)

    while True:

        calculate(signal, offset, 8, signal_len)

        if phase % 10 == 0: print(f"{datetime.datetime.now()}")
        if phase == 100:
            break

        phase += 1

    print(f"First eight: {signal[offset:offset+8]}.")
                
