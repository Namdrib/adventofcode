import unittest

from src.main._2024 import day17

class TestThreeBitComputer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Do this as a class attribute so we can verify that the registers and
        # program can be reset multiple times
        cls.tbc = day17.ThreeBitComputer([0, 0, 0], [0, 0])

    def test_A729(self):
        registers: list = [729, 0, 0]
        program: list = [0, 1, 5, 4, 3, 0]

        self.tbc.registers=registers
        output = self.tbc.execute(program)

        self.assertEqual(output, [4, 6, 3, 5, 6, 3, 5, 2, 1, 0])

    def test_C9(self):
        # If register C contains 9,
        # the program 2,6 would
        # set register B to 1.
        registers: list = [0, 0, 9]
        program: list = [2, 6]

        self.tbc.registers=registers
        _ = self.tbc.execute(program)

        self.assertEqual(self.tbc.registers[1], 1)

    def test_A10(self):
        # If register A contains 10,
        # the program 5,0,5,1,5,4 would
        # output 0,1,2.
        registers: list = [10, 0, 0]
        program: list = [5, 0, 5, 1, 5, 4]

        self.tbc.registers=registers
        output = self.tbc.execute(program)

        self.assertEqual(output, [0, 1, 2])
        
    def test_A2024(self):
        # If register A contains 2024,
        # the program 0,1,5,4,3,0 would
        # output 4,2,5,6,7,7,7,7,3,1,0 and
        # leave 0 in register A.
        registers: list = [2024, 0, 0]
        program: list = [0, 1, 5, 4, 3, 0]

        self.tbc.registers=registers
        output = self.tbc.execute(program)

        self.assertEqual(output, [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0])
        self.assertEqual(self.tbc.registers[0], 0)

    def test_B29(self):
        # If register B contains 29,
        # the program 1,7 would
        # set register B to 26.
        registers: list = [0, 29, 0]
        program: list = [1, 7]

        self.tbc.registers=registers
        _ = self.tbc.execute(program)

        self.assertEqual(self.tbc.registers[1], 26)

    def test_B2024_C43690(self):
        # If register B contains 2024 and register C contains 43690,
        # the program 4,0 would
        # set register B to 44354.
        registers: list = [0, 2024, 43690]
        program: list = [4, 0]
        self.tbc.registers=registers
        _ = self.tbc.execute(program)

        self.assertEqual(self.tbc.registers[1], 44354)
