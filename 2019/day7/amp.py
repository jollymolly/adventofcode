#!python3

import functools
import multiprocessing

import hal

LOWEST_PHASE_VALUE=5
PHASES_VALUES_PORTION_SIZE=1000


def amplifiers_phases(amplifiers_count):

    amplifiers_phases_seq, phases_max_num  = [LOWEST_PHASE_VALUE] * amplifiers_count, 10**amplifiers_count

    amplifiers_phases_num = int("".join(map(str, amplifiers_phases_seq)))

    while amplifiers_phases_num < phases_max_num:

        next_phases_num, i = amplifiers_phases_num, amplifiers_count-1

        while next_phases_num:
            next_phases_num, phase_num = next_phases_num // 10, next_phases_num % 10
            if phase_num < LOWEST_PHASE_VALUE: continue
            amplifiers_phases_seq[i] = phase_num
            i -= 1

        amplifiers_phases_num += 1

        if len(set(amplifiers_phases_seq)) != amplifiers_count: continue

        yield tuple(amplifiers_phases_seq)

    return

def calculate_signal(instructions, phases):
    
    hal.ComputingUnit.init_instruction_handlers()
    
    amplifiers = tuple(hal.ComputingUnit(instructions.copy()) for i in range(len(phases)))

    signal, first_iteration = 0, True
        
    while not any(a.completed for a in amplifiers):

        for idx, amplifier in enumerate(amplifiers):
            amplifier.stdin = (phases[idx], signal) if first_iteration else (signal, )
            amplifier.execute()
            signal = amplifier.stdout[-1]

        first_iteration = False

    return signal


if __name__ == "__main__":

    instructions = []
    with open("input.txt") as f:
        instructions = [int(text_num) for line in f for text_num in line.split(',')]

    amplifiers_count = 5

    output_signal_calculator = functools.partial(calculate_signal, instructions)

    with multiprocessing.Pool() as p:
        
        phases_gen, max_signal = amplifiers_phases(amplifiers_count), 0
        
        while True:
            phases = []
            try:
                for i in range(PHASES_VALUES_PORTION_SIZE):
                    phases.append(next(phases_gen))
            except:
                pass
            if not phases: break
            signal = max(p.map(output_signal_calculator, phases))
            if signal > max_signal:
                max_signal = signal

        print(f"max signal: {max_signal}.")


    
        
