#!python3

import sys

console_state = {
    "accumulator": 0,
    "ip": 1,
    "past_instructions": set(),
}


class InfiniteLoopException(Exception):
    pass


def nop(console_state: dict, arg: int):
    jmp(console_state, 1)

    
def acc(console_state: dict, arg: int):
    console_state["accumulator"] += arg
    jmp(console_state, 1)

    
def jmp(console_state: dict, arg: int):
    next_ip = console_state["ip"] + arg
    if is_past_instruction(console_state, next_ip):
        raise InfiniteLoopException(f"accumulator is set to: {console_state['accumulator']}.")
    console_state["ip"] = next_ip

                                    
def is_past_instruction(console_state: dict, next_instruction_ip: int) -> bool:
    return next_instruction_ip in console_state["past_instructions"]


def register_past_instruction(console_state: dict):
    console_state["past_instructions"].add(console_state["ip"])


def get_instruction(instructions, console_state: dict):
    return instructions[console_state["ip"]-1] if console_state["ip"] <= len(instructions) else None


instructions_map = {
    "nop": nop,
    "acc": acc,
    "jmp": jmp,
}

    
def run(instructions: dict):

    while True:
        i = get_instruction(instructions, console_state)
        if i is None:
            break
        instructions_map[i[0]](console_state, -1 * i[2] if i[1] == '-' else i[2])
        register_past_instruction(console_state)

    print(f"Answer: {console_state['accumulator']}.")
    

def main(args):

    if len(args) != 2:
        print(f"Cmd line: {args[0]} <input_file>")
        return 1

    instructions = []
    
    with open(args[1]) as inp:
        
        for l in map(str.strip, inp):
            op, arg = l.split(' ')
            instructions.append((op, arg[0], int(arg[1:])))

    run(instructions)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
