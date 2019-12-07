#python3

import functools
import operator


class ComputingUnit:

    MEMORY_ACCESS_POSITION_MODE = 0
    MEMORY_ACCESS_IMMEDIATE_MODE = 1
    MEMORY_ACCESS_MODES_ARG1_POS = 0
    MEMORY_ACCESS_MODES_ARG2_POS = 1
    MEMORY_ACCESS_MODES_OUTP_POS = 2

    HALT_OPCODE=99

    INSTRUCTIONS = (
        dict(desc="ADD", opcode=1, executor=None),
        dict(desc="MUL", opcode=2, executor=None),
        dict(desc="INPUT",  opcode=3, executor=None),
        dict(desc="OUTPUT", opcode=4, executor=None),
        dict(desc="JUMP_IF_TRUE", opcode=5, executor=None),
        dict(desc="JUMP_IF_FALSE", opcode=6, executor=None),
        dict(desc="LESS_THAN", opcode=7, executor=None),
        dict(desc="EQUALS", opcode=8, executor=None),
        dict(desc="HALT", opcode=HALT_OPCODE, executor=None),
    )
    OPCODE_TO_INSTRUCTION_MAP = dict(
        (instr["opcode"], instr) for instr in INSTRUCTIONS
    )

    @staticmethod
    def init_instruction_handlers():
        for handler_description in ComputingUnit.INSTRUCTIONS:
            handler_description["executor"] = getattr(ComputingUnit, handler_description["desc"].lower())

    @staticmethod
    def parse_instruction(instruction):

        codes, divisor = [], 100

        while instruction:
            instruction, code, divisor = instruction // divisor, instruction % divisor, 10
            codes.append(code)

        while len(codes) != 4:
            codes.append(0)

        return (codes[0], tuple(codes[1:]))

    @staticmethod
    def get_arg_idx_based_on_access_mode(instructions, ip, mode):
        return ip if mode == ComputingUnit.MEMORY_ACCESS_IMMEDIATE_MODE else instructions[ip]

    @staticmethod
    def get_instruction_indexes(instructions, ip, mem_access_modes, args_count):
        return tuple(
            ComputingUnit.get_arg_idx_based_on_access_mode(instructions, ip+arg_num, mem_access_modes[arg_num])
            for arg_num in range(args_count)
        )

    @staticmethod
    def add(instructions, ip, mem_access_modes):
        arg1_idx, arg2_idx, output_idx = ComputingUnit.get_instruction_indexes(instructions, ip, mem_access_modes, 3)
        instructions[output_idx] = instructions[arg1_idx]+instructions[arg2_idx]
        return ip + 3

    @staticmethod
    def mul(instructions, ip, mem_access_modes):
        arg1_idx, arg2_idx, output_idx = ComputingUnit.get_instruction_indexes(instructions, ip, mem_access_modes, 3)
        instructions[output_idx] = instructions[arg1_idx]*instructions[arg2_idx]
        return ip + 3

    @staticmethod
    def input(instructions, ip, mem_access_modes):
        output_idx, = ComputingUnit.get_instruction_indexes(instructions, ip, mem_access_modes, 1)
        instructions[output_idx] = int(input("input: "))
        return ip + 1

    @staticmethod
    def output(instructions, ip, mem_access_modes):
        print_value_idx, = ComputingUnit.get_instruction_indexes(instructions, ip, mem_access_modes, 1)
        print(instructions[print_value_idx])
        return ip + 1

    @staticmethod
    def jump_if_true(instructions, ip, mem_access_modes):
        arg1_idx, arg2_idx = ComputingUnit.get_instruction_indexes(instructions, ip, mem_access_modes, 2)
        if instructions[arg1_idx] != 0: ip = instructions[arg2_idx]
        else: ip += 2
        return ip

    @staticmethod
    def jump_if_false(instructions, ip, mem_access_modes):
        arg1_idx, arg2_idx = ComputingUnit.get_instruction_indexes(instructions, ip, mem_access_modes, 2)
        if instructions[arg1_idx] == 0: ip = instructions[arg2_idx]
        else: ip += 2
        return ip

    @staticmethod
    def less_than(instructions, ip, mem_access_modes):
        arg1_idx, arg2_idx, output_idx = ComputingUnit.get_instruction_indexes(instructions, ip, mem_access_modes, 3)
        instructions[output_idx] = 1 if instructions[arg1_idx] < instructions[arg2_idx] else 0
        return ip + 3

    @staticmethod
    def equals(instructions, ip, mem_access_modes):
        arg1_idx, arg2_idx, output_idx = ComputingUnit.get_instruction_indexes(instructions, ip, mem_access_modes, 3)
        instructions[output_idx] = 1 if instructions[arg1_idx] == instructions[arg2_idx] else 0
        return ip + 3


    @staticmethod
    def halt():
        """stub to avoid unnecessary if checks in init handlers method"""
        pass

    def execute(instructions):

        ip = 0
        
        while instructions[ip] != ComputingUnit.HALT_OPCODE:
            start_ip = ip
            instruction = instructions[ip]
            instr_opcode, mem_access_modes = ComputingUnit.parse_instruction(instruction)
            if instr_opcode not in ComputingUnit.OPCODE_TO_INSTRUCTION_MAP:
                raise RuntimeError("Unsupported instruction {} at addr {}.".format(instr_opcode, ip))

            ip += 1

            executor = ComputingUnit.OPCODE_TO_INSTRUCTION_MAP[instr_opcode]["executor"]
            ip = executor(instructions, ip, mem_access_modes)

            
if __name__ == "__main__":

    instructions = []
    with open("input.txt") as f:
        instructions = [int(text_num) for line in f for text_num in line.split(',')]

    if len(instructions) < 2:
        print("Nothing to process, exiting.")

    ComputingUnit.init_instruction_handlers()
    ComputingUnit.execute(instructions)
