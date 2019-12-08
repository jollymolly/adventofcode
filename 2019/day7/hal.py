#!python

#!python3

import functools
import operator
import sys


class ComputingUnit:

    class WaitForInputError(Exception):
        pass

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

    def __init__(self, instructions):
        self.__input = list()
        self.__output = list()
        self.__instructions, self.__ip = instructions, 0
        self.completed = False

    def debug(self):
        #print(self.__instructions)
        #print(self.__instructions[28])
        print(f"{self.completed}; ip: {self.__ip};")
        
    @property
    def stdin(self):
        return self.__input.copy()

    @stdin.setter
    def stdin(self, values):
        self.__input += values

    @property
    def stdout(self):
        return self.__output.copy()
    
    def add(self, instructions, ip, mem_access_modes):
        arg1_idx, arg2_idx, output_idx = ComputingUnit.get_instruction_indexes(instructions, ip, mem_access_modes, 3)
        instructions[output_idx] = instructions[arg1_idx]+instructions[arg2_idx]
        return ip + 3

    def mul(self, instructions, ip, mem_access_modes):
        arg1_idx, arg2_idx, output_idx = ComputingUnit.get_instruction_indexes(instructions, ip, mem_access_modes, 3)
        instructions[output_idx] = instructions[arg1_idx]*instructions[arg2_idx]
        return ip + 3

    def input(self, instructions, ip, mem_access_modes):
        output_idx, = ComputingUnit.get_instruction_indexes(instructions, ip, mem_access_modes, 1)
        if not self.__input: raise ComputingUnit.WaitForInputError()
        instructions[output_idx] = int(self.__input.pop(0))
        return ip + 1

    def output(self, instructions, ip, mem_access_modes):
        print_value_idx, = ComputingUnit.get_instruction_indexes(instructions, ip, mem_access_modes, 1)
        self.__output.append(instructions[print_value_idx])
        return ip + 1

    def jump_if_true(self, instructions, ip, mem_access_modes):
        arg1_idx, arg2_idx = ComputingUnit.get_instruction_indexes(instructions, ip, mem_access_modes, 2)
        if instructions[arg1_idx] != 0: ip = instructions[arg2_idx]
        else: ip += 2
        return ip

    def jump_if_false(self, instructions, ip, mem_access_modes):
        arg1_idx, arg2_idx = ComputingUnit.get_instruction_indexes(instructions, ip, mem_access_modes, 2)
        if instructions[arg1_idx] == 0: ip = instructions[arg2_idx]
        else: ip += 2
        return ip

    def less_than(self, instructions, ip, mem_access_modes):
        arg1_idx, arg2_idx, output_idx = ComputingUnit.get_instruction_indexes(instructions, ip, mem_access_modes, 3)
        instructions[output_idx] = 1 if instructions[arg1_idx] < instructions[arg2_idx] else 0
        return ip + 3

    def equals(self, instructions, ip, mem_access_modes):
        arg1_idx, arg2_idx, output_idx = ComputingUnit.get_instruction_indexes(instructions, ip, mem_access_modes, 3)
        instructions[output_idx] = 1 if instructions[arg1_idx] == instructions[arg2_idx] else 0
        return ip + 3

    def halt(self):
        """stub to avoid unnecessary if checks in init handlers method"""
        pass

    def execute(self):

        while self.__instructions[self.__ip] != ComputingUnit.HALT_OPCODE:
            instruction = self.__instructions[self.__ip]
            instr_opcode, mem_access_modes = ComputingUnit.parse_instruction(instruction)
            if instr_opcode not in ComputingUnit.OPCODE_TO_INSTRUCTION_MAP:
                raise RuntimeError("Unsupported instruction {} at addr {}.".format(instr_opcode, self.__ip))

            self.__ip += 1

            executor = ComputingUnit.OPCODE_TO_INSTRUCTION_MAP[instr_opcode]["executor"]
            try:
                self.__ip = executor(self, self.__instructions, self.__ip, mem_access_modes)
            except ComputingUnit.WaitForInputError:
                self.__ip -= 1
                break

            
        self.completed = self.__instructions[self.__ip] == ComputingUnit.HALT_OPCODE


if __name__ == "__main__":

    instructions = []
    with open("input_test.txt") as f:
        instructions = [int(text_num) for line in f for text_num in line.split(',')]

    if len(instructions) < 2:
        print("Nothing to process, exiting.")

    ComputingUnit.init_instruction_handlers()
    ComputingUnit.execute(instructions)

