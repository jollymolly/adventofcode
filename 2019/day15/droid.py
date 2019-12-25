#!python3

import hal
import random


NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

WALL = 0
STEP = 1
OXYGEN = 2

direction_loop = (NORTH, EAST, SOUTH, WEST)
direction_desc = {1: "NORTH", 2: "SOUTH", 3: "WEST", 4: "EAST"}

if __name__ == "__main__":

    instructions = None
    
    with open("input.txt") as f:
        instructions = list(map(int, f.readline().strip().split(',')))

    if not instructions:
        print("No insturctions to run.")
        
    hal.ComputingUnit.init_instruction_handlers()

    cu = hal.ComputingUnit(instructions)

    width, height = 100, 100
    screen = [ [' '] * width for _ in range(height)]
    droid_y, droid_x, background = height // 2, width // 2, ' '
    start_y, start_x = droid_y, droid_x

    screen[droid_y][droid_x] = 'D'

    paths = dict()

    possible_droid_steps = list(
        (
            (droid_y-1, droid_x),
            (droid_y+1, droid_x),
            (droid_y, droid_x-1),
            (droid_y, droid_x+1)
        )
    )

    oxygen_y, oxygen_x = None, None

    while True:

        list_idx = next((idx for idx, (y, x) in enumerate(possible_droid_steps) if screen[y][x] == ' '), -1)
        if list_idx == -1:
            list_idx = round(random.random() * 100) % (len(possible_droid_steps) - (1 if len(possible_droid_steps) > 1 else 0))

        where_to_y, where_to_x = possible_droid_steps.pop(list_idx)

        direction = -1
        direction = WEST if where_to_x < droid_x else EAST if where_to_x > droid_x else direction
        direction = NORTH if where_to_y < droid_y else SOUTH if where_to_y > droid_y else direction

        cu.stdin = (str(direction), )
        cu.execute()
        if cu.completed:
            break
        result = cu.stdout[-1]

        if result == WALL:
            screen[where_to_y][where_to_x] = '#'
        elif result == STEP:
            screen[where_to_y][where_to_x] = 'D'
            screen[droid_y][droid_x] = '.'

            if where_to_y not in paths:
                paths.setdefault((where_to_y, where_to_x), dict())[droid_y, droid_x] = 1
                paths.setdefault((droid_y, droid_x), dict())[where_to_y, where_to_x] = 1
            
            possible_droid_steps = [(droid_y, droid_x), ]

            for y, x in (
                    (where_to_y-1, where_to_x),
                    (where_to_y+1, where_to_x),
                    (where_to_y, where_to_x-1),
                    (where_to_y, where_to_x+1),
            ):
                if (y, x) == (droid_y, droid_x): continue
                possible_droid_steps.insert(0, (y, x))

            droid_y, droid_x = where_to_y, where_to_x
            
        elif result == OXYGEN:
            screen[where_to_y][where_to_x] = 'O'
            oxygen_y, oxygen_x = where_to_y, where_to_x
            paths[where_to_y, where_to_x] = { (droid_y, droid_x): 1 }
            paths[droid_y, droid_x] = { (where_to_y, where_to_x): 1 }
            break

    for l in screen:
        print_line = "".join(l)
        if print_line.count(' ') == len(print_line): continue
        print(print_line)

    print(f"oxygen_y, oxygen_x: ({oxygen_y}, {oxygen_x}); droid_y, droid_x: ({droid_y}, {droid_x}).")

    places = list(((start_y, start_x, 0),))
    measured_points = set()

    while places:

        y, x, steps_count = places.pop(0)

        for neighbor_y, neighbor_x in paths[y, x]:

            if (neighbor_y, neighbor_x) in measured_points:
                continue
            
            steps = steps_count + 1

            paths[neighbor_y, neighbor_x][y, x] = steps
            paths[y, x][neighbor_y, neighbor_x] = steps
            places.append((neighbor_y, neighbor_x, steps))
            
        measured_points.add((y, x))

    min_path_steps = paths[oxygen_y, oxygen_x] # take min value

    minutes_counter = 0
    o_points = [(oxygen_y, oxygen_x), ]
    o_points_visited = set()
    
    while True:

        o_points_visited |= set(o_points)

        if len(o_points_visited) == len(paths):
            break
        
        o_points = list(
            point
            for o_point in o_points
            for point in paths[o_point]
            if point not in o_points_visited
        )
            
        minutes_counter += 1

    print(f"y, x: {droid_y}, {droid_x}. steps: {min_path_steps}. oxygen fill time: {minutes_counter}.")
