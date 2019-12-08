#!python3

import math


def mass_fuel(mass):
    return math.floor(mass/3)-2

def mass_seq(mass):
    while True:
        fuel_inc = mass_fuel(mass)
        if fuel_inc <= 0:
            break
        yield fuel_inc
        mass = fuel_inc

def count_fuel(mass):
    return sum(mass_seq(mass))

if __name__ == "__main__":
    with open("input.txt") as f:
        print(sum(map(count_fuel, map(int, f))))
