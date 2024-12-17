#!/usr/bin/python3
import copy
import os
import re
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

class ThreeBitComputer:
    def __init__(self, registers: list) -> None:
        self.registers = registers

    def get_combo(self, operand: int) -> int:
        """
        If operand is between 0-3 (inclusive), treat the operand as a literal
        If operand is between 4-6 (inclusive), return the value of the matching
        register (4: A, 5: B, 6: C)
        Operand 7 is unused

        :param operand: A number between 0 and 7 (inclusive)
        :type operand: int
        :return: The value of the operand after translation
        :rtype: int
        """
        if 0 <= operand <= 3:
            return operand
        if 4 <= operand <= 6:
            return self.registers[operand-4]
        if operand == 7:
            return 0

        return 0

    def execute_instruction(self, opcode: int, operand: int, output: list) -> int:
        """
        Execute an opcode instruction with its operand as data

        Any output is appended to output

        :param opcode: The opcode to execute
        :type opcode: int
        :param operand: The operand of the opcode
        :type operand: int
        :param output: The program output storage
        :type output: list
        :return: An offset for the instruction pointer, if it is set, -1 otherwise
        :rtype: int
        """
        jump_address: int = -1

        combo: int = self.get_combo(operand)

        match opcode:
            case 0:
                # adv: Bit-shift A right by combo bits, store into A
                res: int = self.registers[0] >> combo
                self.registers[0] = res

            case 1:
                # bxl: Bitwise XOR B and combo, store into B
                res: int = self.registers[1] ^ operand
                self.registers[1] = res

            case 2:
                # bst: Combo % 8, store into B
                res: int = combo % 8
                self.registers[1] = res

            case 3:
                # jnz: Set the instruction pointer to the value of the arg if
                # register A is non-zero
                if self.registers[0] != 0:
                    jump_address = operand

            case 4:
                # bxc: Bitwise XOR B and C, store into B
                res: int = self.registers[1] ^ self.registers[2]
                self.registers[1] = res

            case 5:
                # out: Output the last 3 bits
                res: int = combo % 8
                output.append(res)

            case 6:
                # bdv: Bit-shift A right by combo bits, store into B
                res: int = self.registers[0] >> combo
                self.registers[1] = res

            case 7:
                # cdv: Bit-shift A right by combo bits, store into C
                res: int = self.registers[0] >> combo
                self.registers[2] = res

        return jump_address

    def execute(self, program: str) -> list:
        """
        Execute a program consisting of instructions and return the output

        :param program: A list of numbers (from 0-7)
        :type program: str
        :return: The output of the program (numbers form 0-7)
        :rtype: list
        """
        # Instruction pointer
        ip: int = 0

        # Store any output from this program execution
        # This is modified in-place in execute()
        output = []

        while ip < len(program):
            jump = self.execute_instruction(program[ip], program[ip+1], output)

            # Do we go to the next instruction or adhere to a jump?
            if jump == -1:
                ip += 2
            else:
                ip = jump

        print(f'{output=}')
        return output

class Day17:
    """
    Solution for https://adventofcode.com/2024/day/17
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.input: list = None

        self.registers: list = None
        self.program: list = None
        self.cp: int = 0

    def read_input(self) -> None:
        """
        Read input from stdin and parse it into a useful data structure
        In this case, each line ...
        """
        raw_input = sys.stdin.read()
        self.input = raw_input.splitlines()

        self.registers = []
        for i, item in enumerate(self.input):
            if i < 3:
                register_value: int = int(re.findall(r'\d+', item)[0])
                self.registers.append(register_value)
            elif i == 4:
                self.program = list(map(int, re.findall(r'\d+', item)))

        print(f'{self.registers=}')
        print(f'{self.program=}')

    def part_one(self) -> int:
        """
        Return the output after executing the program
        """
        comp: ThreeBitComputer = ThreeBitComputer(copy.deepcopy(self.registers))
        output: list = comp.execute(self.program)
        if output:
            return ','.join([str(x) for x in output])
        return ''

    def part_two(self) -> int:
        """
        Return the ...
        """
        target: list = self.program
        print(len(target))
        comp: ThreeBitComputer = ThreeBitComputer(copy.deepcopy(self.registers))

        # len(target) == 16
        # Every iteration of the loop, A is shifted right 3 bits, and one number
        # is printed
        # So A must, in the end, be 16*3 bits long to output exactly 16 numbers

        # However, we don't know the values of A that are required to output
        # each number in the output

        # Starting value of A large enough to get the right number of outputs
        # A: int = 0
        # A = 24
        # A += 1 << 47
        # A = 1<<48 - 1

        # 24 was calculate by hand to output the last two digits of the program
        known_a: int = 24 << 3

        # while known_a < 1<<48:
        for bit in range(2, len(self.program * 3)+1):
            print(f'Looking at {bit=}')
            # Work in from the least-significant bit
            output: list = []

            # The numbers covered in least-significant 3 bits
            for ls3b in range(0, 8):
                try_a: int = known_a + ls3b
                print(f'Trying {try_a=}')
                comp.registers = [try_a, 0, 0]
                output = comp.execute(self.program)

                if output == target:
                    return try_a

                list_index: int = bit
                print(f'Position at -{list_index}: {output[:-list_index]}, {target[:-list_index]}')
                if output[:-bit] == target[:-bit]:
                    known_a <<= 3
                    known_a += try_a
                    break

        # while len(output) <= len(target):
        #     A <<= 3
        #     executions: int = 0
        #     for offset in range(0, 8):
        #     # while len(output) <= len(target):
        #         comp.registers = [A+offset, 0, 0]
        #         output = comp.execute_instructions()
        #         print(f'{A+offset=}: {len(output)=}')

        #         if output == target:
        #             return A+offset
        #         # A += 1
        #         # A += 2**executions
        #         # A += executions * 8
        #         executions += 1

def main() -> None:
    """
    Main
    """
    solver = Day17()
    solver.read_input()

    # Register A: 2024
    # Register B: 0
    # Register C: 0

    # Program: 0,3,5,4,3,0

    # Pseudocode
    # // 3, 0
    # while A:
    #     // 0, 3
    #     A >> 3

    #     // 5, 4
    #     print(A%8)
    print(f'Part 1: {solver.part_one()}')

    # Register A: 46187030
    # Register B: 0
    # Register C: 0

    # Program: 2,4,1,5,7,5,0,3,4,0,1,6,5,5,3,0

    # Translation
    # while A != 0:
    #     // 2, 4
    #     B = A%8

    #     // 1, 5
    #     B ^= 5

    #     // 7, 5
    #     C = A >> B

    #     // 0, 3
    #     A >> 3

    #     // 4, 0
    #     B ^= C

    #     // 1, 6
    #     B ^= 6

    #     // 5, 5
    #     print(B%8)
    print(f'Part 2: {solver.part_two()}')

if __name__ == '__main__':
    main()
