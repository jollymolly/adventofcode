#python3

import operator

ADD_OPCODE = 1
MUL_OPCODE = 2
HALT_OPCODE = 99

def process(instructions):

    idx, final_idx, op = 0, len(instructions), None

    while idx < final_idx and instructions[idx] != HALT_OPCODE:

        if instructions[idx] == ADD_OPCODE: 
            op = operator.add
        elif instructions[idx] == MUL_OPCODE:
            op = operator.mul
        else:
            print("Invalid opcode {} at idx {}, skipping.".format(instructions[idx], idx))
            idx += 1
            continue

        instructions[instructions[idx+3]] = op(
            instructions[instructions[idx+1]], instructions[instructions[idx+2]]
        )

        idx += 4

    return instructions

class FoundAnswerError(Exception):
    pass


if __name__ == "__main__":

    instructions = []
    with open("input.txt") as f:
        instructions = [int(text_num) for line in f for text_num in line.split(',')]

    if len(instructions) < 2:
        print("Nothing to process, exiting.")

    try:
        
        for noun in range(100):
            for verb in range(100):
                instructions_copy = instructions[:]    
                instructions_copy[1], instructions_copy[2] = noun, verb

                instructions_copy = process(instructions_copy)

                if instructions_copy[0] == 19690720:
                    instructions = instructions_copy
                    raise FoundAnswerError()

    except FoundAnswerError:
        #print("Debug: instructions: {}".format(instructions))
        print("Result: {}; 100*noun+verb: {}".format(instructions[0], 100*noun+verb))

    else:
        print("Nothing has been found (noun:{}, verb:{})".format(noun, verb))
