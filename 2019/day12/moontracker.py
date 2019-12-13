#!python3

TIME_STEPS=1000

POS_IDX = 0
VEL_IDX = 1
X_POS = 0
Y_POS = 1
Z_POS = 2


def debug(planets_params):

    for planet in planets_params:
        print(planet)
    input()


def simulate(planets_params, steps):

    planets_num = len(planets_params)

    states = set()

    iteration = 0

    while True:
        compared = dict(
            (planet_idx, set((planet_idx,))) for planet_idx in range(planets_num)
        )

        for planet_idx in range(planets_num):
            for other_idx in range(planets_num):
                if other_idx in compared[planet_idx]: continue

                for pos in (X_POS, Y_POS, Z_POS):
                    planet_pos_value, other_pos_value = planets_params[planet_idx][POS_IDX][pos], planets_params[other_idx][POS_IDX][pos]
                    if planet_pos_value == other_pos_value: continue
                    step = 1 if other_pos_value > planet_pos_value else -1
                    planets_params[planet_idx][VEL_IDX][pos] += step
                    planets_params[other_idx][VEL_IDX][pos] += -1*step

                compared[planet_idx].add(other_idx)
                compared[other_idx].add(planet_idx)

        for planet_params in planets_params:
            for idx, planet_vel in enumerate(planet_params[VEL_IDX]):
                planet_params[POS_IDX][idx] += planet_vel

        state = frozenset(val for planet_params in planets_params for val in planet_params[POS_IDX]+planet_params[VEL_IDX])
        if state in states:
            print(f"same state found on iteration: {iteration}.")
            print(repr(planets_params))
            break

        states.add(state)
        if iteration % 10**6 == 0:
            print(f"Iteration: {iteration}; states len: {len(_states)}.")

        iteration += 1


def optimized_simulate(planets_params):

    planets_num, planets_params_flat = len(planets_params), [
        v for planet_params in planets_params for v in planet_params[POS_IDX]+planet_params[VEL_IDX]]

    states = set()

    iteration = 0

    idx_step = 6
    idx_max = planets_num * idx_step

    outer_seq = tuple(range(0, idx_max, idx_step))
    target_params = planets_params_flat.copy()

    while True:

        for i in outer_seq:
            for j in range(i+6, idx_max, idx_step):
                
                planet_pos_value, other_pos_value = planets_params_flat[i], planets_params_flat[j]
                if planet_pos_value != other_pos_value:
                    step = 1 if other_pos_value > planet_pos_value else -1
                    planets_params_flat[i+3] += step
                    planets_params_flat[j+3] += -1*step

                planet_pos_value, other_pos_value = planets_params_flat[i+1], planets_params_flat[j+1]
                if planet_pos_value != other_pos_value: 
                    step = 1 if other_pos_value > planet_pos_value else -1
                    planets_params_flat[i+4] += step
                    planets_params_flat[j+4] += -1*step

                planet_pos_value, other_pos_value = planets_params_flat[i+2], planets_params_flat[j+2]
                if planet_pos_value != other_pos_value: 
                    step = 1 if other_pos_value > planet_pos_value else -1
                    planets_params_flat[i+5] += step
                    planets_params_flat[j+5] += -1*step

            else:
                planets_params_flat[i] += planets_params_flat[i+3]
                planets_params_flat[i+1] += planets_params_flat[i+4]
                planets_params_flat[i+2] += planets_params_flat[i+5]

        iteration += 1

        if iteration % 10**6 == 0:
            print(f"iteration: {iteration}.")

        if planets_params_flat[3] or planets_params_flat[4] or planets_params_flat[5] \
           or planets_params_flat[9] or planets_params_flat[10] or planets_params_flat[11] \
           or planets_params_flat[15] or planets_params_flat[16] or planets_params_flat[17] \
           or planets_params_flat[21] or planets_params_flat[22] or planets_params_flat[23]:
            continue

        if planets_params_flat == target_params:
            print(f"iteration: {iteration}; state: {planets_params_flat}.")
            break


def calculate_energy(planets_params):
    total_energy = 0
    for planet_params in planets_params:
        planet_energy = sum(map(abs, planet_params[POS_IDX])) * sum(map(abs, planet_params[VEL_IDX]))
        print(f"planet_energy: {planet_energy}.")
        total_energy += planet_energy

    print(f"total_energy: {total_energy}.")
    return total_energy


def optimized_calculate_energy(planets_params_flat):
    total_energy = 0
    planets_params_flat = list(map(abs, planets_params_flat))
    for i in range(0, 4*6, 6):
        print(planets_params_flat)
        planet_energy = sum(map(abs, planets_params_flat[i: i+3])) * sum(map(abs, planets_params_flat[i+3: i+6]))
        print(f"planet_energy: {planet_energy}.")
        total_energy += planet_energy

    print(f"total_energy: {total_energy}.")
    return total_energy


def optimized2_simulate(planets_params):

    planets_num, planets_params_flat = len(planets_params), [
        v for planet_params in planets_params for v in planet_params[POS_IDX]+planet_params[VEL_IDX]]

    iteration = 0

    idx_step = 6
    idx_half_step = idx_step // 2
    idx_max = planets_num * idx_step

    outer_seq = tuple(range(0, idx_max, idx_step))
    target_params = planets_params_flat.copy()
    x_target, x_found = tuple(target_params[i] for i in range(0, idx_max, idx_half_step)), False
    y_target, y_found = tuple(target_params[i] for i in range(1, idx_max, idx_half_step)), False
    z_target, z_found = tuple(target_params[i] for i in range(2, idx_max, idx_half_step)), False

    coordinates_target_iterations = []

    while not (x_found and y_found and z_found):

        for i in outer_seq:
            for j in range(i+6, idx_max, idx_step):
                
                planet_pos_value, other_pos_value = planets_params_flat[i], planets_params_flat[j]
                if planet_pos_value != other_pos_value:
                    step = 1 if other_pos_value > planet_pos_value else -1
                    planets_params_flat[i+3] += step
                    planets_params_flat[j+3] += -1*step

                planet_pos_value, other_pos_value = planets_params_flat[i+1], planets_params_flat[j+1]
                if planet_pos_value != other_pos_value: 
                    step = 1 if other_pos_value > planet_pos_value else -1
                    planets_params_flat[i+4] += step
                    planets_params_flat[j+4] += -1*step

                planet_pos_value, other_pos_value = planets_params_flat[i+2], planets_params_flat[j+2]
                if planet_pos_value != other_pos_value: 
                    step = 1 if other_pos_value > planet_pos_value else -1
                    planets_params_flat[i+5] += step
                    planets_params_flat[j+5] += -1*step

            else:
                planets_params_flat[i] += planets_params_flat[i+3]
                planets_params_flat[i+1] += planets_params_flat[i+4]
                planets_params_flat[i+2] += planets_params_flat[i+5]

        iteration += 1

        if iteration % 10**6 == 0:
            print(f"iteration: {iteration}.")

        if not x_found and x_target == tuple(planets_params_flat[i] for i in range(0, idx_max, idx_half_step)):
            coordinates_target_iterations.append(iteration)
            x_found = True
            continue
        if not y_found and y_target == tuple(planets_params_flat[i] for i in range(1, idx_max, idx_half_step)):
            coordinates_target_iterations.append(iteration)
            y_found = True
            continue
        if not z_found and z_target == tuple(planets_params_flat[i] for i in range(2, idx_max, idx_half_step)):
            coordinates_target_iterations.append(iteration)
            z_found = True

    print(f"coordinates_target_iterations: {coordinates_target_iterations}.")

    def greatest_common_div(a, b):
        while b:
            a, b = b, a%b
        return a

    ret_val = None
    while len(coordinates_target_iterations) > 1:
        iter1, iter2 = coordinates_target_iterations.pop(), coordinates_target_iterations.pop()
        coordinates_target_iterations.append(iter1*iter2 // greatest_common_div(iter1, iter2))
    print(f"projected iteration: {coordinates_target_iterations}.")
    

if __name__ == "__main__":

    planets_params = []
    
    with open("input.txt") as f:
        for l in f:
            planets_params.append([])
            planets_params[-1].append(
                [int(pos.split("=")[1]) for pos in l.strip()[1:-1].split(",")]
            )
            planets_params[-1].append([0, 0, 0])

    if not planets_params:
        print("No planets to simulate.")

    params = optimized2_simulate(planets_params)

    #optimized_calculate_energy(params)
