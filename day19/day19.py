import math

import advent_tools


def main():
    data = advent_tools.read_input_lines()
    data = process_input(data)
    # print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


class TimeComputer(advent_tools.Computer):

    return_register = 0
    operation = advent_tools.Computer.operation
    debugging = False

    def __init__(self):
        super().__init__()
        self.count = 0

    def print_if_debugging(self, *args, **kwargs):
        if self.debugging:
            print(*args, **kwargs)

    @operation("addr")
    def addr(self, a_reg, b_reg, c_reg):
        if self.count < 1000:
            self.print_if_debugging(
                f"Add value in register {a_reg} to value in register {b_reg} and store"
                f" in register {c_reg}", end=","
            )
        self.registers[c_reg] = self.registers[a_reg] + self.registers[b_reg]

    @operation("addi")
    def addi(self, a_reg, b_val, c_reg):
        if self.count < 1000:
            self.print_if_debugging(
                f"Add value in register {a_reg} to value {b_val} and store in register"
                f" {c_reg}", end=","
            )
        self.registers[c_reg] = self.registers[a_reg] + b_val

    @operation("mulr")
    def mulr(self, a_reg, b_reg, c_reg):
        if self.count < 1000:
            self.print_if_debugging(
                f"Multiply value in register {a_reg} by value in register {b_reg} and"
                f" store in register {c_reg}", end=","
            )
        self.registers[c_reg] = self.registers[a_reg] * self.registers[b_reg]

    @operation("muli")
    def muli(self, a_reg, b_val, c_reg):
        if self.count < 1000:
            self.print_if_debugging(
                f"Multiply value in register {a_reg} by value {b_val} and store in"
                f" register {c_reg}", end=","
            )
        self.registers[c_reg] = self.registers[a_reg] * b_val

    @operation("banr")
    def banr(self, a_reg, b_reg, c_reg):
        if self.count < 1000:
            self.print_if_debugging(
                f"Binary AND register {a_reg} with register {b_reg} and store in"
                f" register {c_reg}", end=","
            )
        self.registers[c_reg] = self.registers[a_reg] & self.registers[b_reg]

    @operation("bani")
    def bani(self, a_reg, b_val, c_reg):
        self.registers[c_reg] = self.registers[a_reg] & b_val

    @operation("borr")
    def borr(self, a_reg, b_reg, c_reg):
        if self.count < 1000:
            self.print_if_debugging(
                f"Binary OR register {a_reg} with register {b_reg} and store in"
                f" register {c_reg}", end=","
            )
        self.registers[c_reg] = self.registers[a_reg] | self.registers[b_reg]

    @operation("bori")
    def bori(self, a_reg, b_val, c_reg):
        self.registers[c_reg] = self.registers[a_reg] | b_val

    @operation("setr"
            )
    def setr(self, a_reg, _, c_reg):
        if self.count < 1000:
            self.print_if_debugging(
                f"Set register {c_reg} to value in register {a_reg}", end=","
            )
        self.registers[c_reg] = self.registers[a_reg]

    @operation("seti")
    def seti(self, a_val, _, c_reg):
        if self.count < 1000:
            self.print_if_debugging(f"Set register {c_reg} to value {a_val}", end=",")
        self.registers[c_reg] = a_val

    @operation("gtir")
    def gtir(self, a_val, b_reg, c_reg):
        self.registers[c_reg] = int(a_val > self.registers[b_reg])

    @operation("gtri")
    def gtri(self, a_reg, b_val, c_reg):
        self.registers[c_reg] = int(self.registers[a_reg] > b_val)

    @operation("gtrr")
    def gtrr(self, a_reg, b_reg, c_reg):
        if self.count < 1000:
            self.print_if_debugging(
                f"Set register {c_reg} to 0 or 1 depending on whether register {a_reg}"
                f" is greater than {b_reg}", end=","
            )
        self.registers[c_reg] = int(self.registers[a_reg] > self.registers[b_reg])

    @operation("eqir")
    def eqir(self,  a_val, b_reg, c_reg):
        self.registers[c_reg] = int(a_val == self.registers[b_reg])

    @operation("eqri")
    def eqri(self, a_reg, b_val, c_reg):
        self.registers[c_reg] = int(self.registers[a_reg] == b_val)

    @operation("eqrr")
    def eqrr(self, a_reg, b_reg, c_reg):
        if self.count < 1000:
            self.print_if_debugging(
                f"Set register {c_reg} to 0 or 1 depending on whether register {a_reg}"
                f" equals register {b_reg}", end=","
            )
        self.registers[c_reg] = int(self.registers[a_reg] == self.registers[b_reg])

    def run_instruction(self, instruction):
        self.registers[2] = self.instruction_pointer
        self.operation_map[instruction[0]](self, *instruction[1:])
        self.count += 1
        self.print_if_debugging(
            f"Step {self.count}, instruction {self.instruction_pointer},"
            f" {instruction[0]}, registers",
            end=" "
        )
        for i in range(6):
            self.print_if_debugging(self.registers[i], end=',')
        self.print_if_debugging("")
        self.instruction_pointer = self.registers[2]


class TimeComputerPartTwo(TimeComputer):

    return_register = 1
    debugging = True

    def run_program(self, program):
        # line 4 is where the very long loop is
        while self.instruction_pointer != 4:
            try:
                line = program[self.instruction_pointer]
            except IndexError:
                return self.registers[self.return_register]
            self.run_instruction(line)
            self.instruction_pointer = self.instruction_pointer + 1
        return self.registers[self.return_register]


def process_input(data):
    result = []
    for line in data[1:]:
        words = line.split()
        result.append((words[0], *(int(num) for num in words[1:])))
    return result


def run_part_1(data):
    computer = TimeComputer()
    return computer.run_program(data)


def run_part_2(data):
    computer = TimeComputerPartTwo()
    computer.registers[0] = 1
    reg1_value = computer.run_program(data)
    max_factor = int(round(math.sqrt(reg1_value)))
    # rewrite the very long loop on lines 3-11 of the program
    sum = 0
    for i in range(1, max_factor+1):
        if reg1_value % i == 0:
            sum += i + reg1_value // i
    return sum


if __name__ == '__main__':
    main()
