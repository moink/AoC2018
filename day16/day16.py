import contextlib
import collections

import advent_tools


def main():
    examples, instructions = process_input(advent_tools.read_input_line_groups())
    print('Part 1:', run_part_1(examples))
    print('Part 2:', run_part_2(examples, instructions))


def process_input(data):
    examples = [advent_tools.read_all_integers(example) for example in data[:-1]]
    examples = [example for example in examples if example]
    instructions = advent_tools.read_all_integers(data[-1])
    return examples, instructions


class TimeComputer(advent_tools.Computer):

    return_register = 0
    operation = advent_tools.Computer.operation

    @operation(0)
    def addr(self, a_reg, b_reg, c_reg):
        self.registers[c_reg] = self.registers[a_reg] + self.registers[b_reg]

    @operation(1)
    def addi(self, a_reg, b_val, c_reg):
        self.registers[c_reg] = self.registers[a_reg] + b_val

    @operation(2)
    def mulr(self, a_reg, b_reg, c_reg):
        self.registers[c_reg] = self.registers[a_reg] * self.registers[b_reg]

    @operation(3)
    def muli(self, a_reg, b_val, c_reg):
        self.registers[c_reg] = self.registers[a_reg] * b_val

    @operation(4)
    def banr(self, a_reg, b_reg, c_reg):
        self.registers[c_reg] = self.registers[a_reg] & self.registers[b_reg]

    @operation(5)
    def bani(self, a_reg, b_val, c_reg):
        self.registers[c_reg] = self.registers[a_reg] & b_val

    @operation(6)
    def borr(self, a_reg, b_reg, c_reg):
        self.registers[c_reg] = self.registers[a_reg] | self.registers[b_reg]

    @operation(7)
    def bori(self, a_reg, b_val, c_reg):
        self.registers[c_reg] = self.registers[a_reg] | b_val

    @operation(8)
    def setr(self, a_reg, _, c_reg):
        self.registers[c_reg] = self.registers[a_reg]

    @operation(9)
    def seti(self, a_val, _, c_reg):
        self.registers[c_reg] = a_val

    @operation(10)
    def gtir(self, a_val, b_reg, c_reg):
        self.registers[c_reg] = int(a_val > self.registers[b_reg])

    @operation(11)
    def gtri(self, a_reg, b_val, c_reg):
        self.registers[c_reg] = int(self.registers[a_reg] > b_val)

    @operation(12)
    def gtrr(self, a_reg, b_reg, c_reg):
        self.registers[c_reg] = int(self.registers[a_reg] > self.registers[b_reg])

    @operation(13)
    def eqir(self,  a_val, b_reg, c_reg):
        self.registers[c_reg] = int(a_val == self.registers[b_reg])

    @operation(14)
    def eqri(self, a_reg, b_val, c_reg):
        self.registers[c_reg] = int(self.registers[a_reg] == b_val)

    @operation(15)
    def eqrr(self, a_reg, b_reg, c_reg):
        self.registers[c_reg] = int(self.registers[a_reg] == self.registers[b_reg])

    def run_instruction(self, instruction):
        self.operation_map[instruction[0]](self, *instruction[1:])


def run_part_1(examples):
    computer = TimeComputer()
    three_count = 0
    for register_start, instruction, register_end in examples:
        count = 0
        for op_num, function in computer.operation_map.items():
            computer.registers = register_list_to_dict(register_start)
            function(computer, *instruction[1:])
            if computer.registers == register_list_to_dict(register_end):
                count += 1
        if count >= 3:
            three_count += 1
    return three_count


def register_list_to_dict(register_start):
    return {i: val for i, val in enumerate(register_start)}


def run_part_2(examples, instructions):
    computer = TimeComputer()
    computer.operation_map = {
        new_op_code: computer.operation_map[old_op_code]
        for old_op_code, new_op_code in map_op_codes(examples).items()
    }
    return computer.run_program(instructions)


def map_op_codes(examples):
    possibilities = get_possibilities(examples)
    definites = {}
    while any(possibilities.values()):
        for op_code, fun_nums in possibilities.items():
            if len(fun_nums) == 1:
                fun_num = list(fun_nums)[0]
                definites[op_code] = fun_num
                for other_funs in possibilities.values():
                    with contextlib.suppress(KeyError):
                        other_funs.remove(fun_num)
    return definites


def get_possibilities(examples):
    computer = TimeComputer()
    possibilities = collections.defaultdict(set)
    for register_start, instruction, register_end in examples:
        for op_num, function in computer.operation_map.items():
            computer.registers = {i: val for i, val in enumerate(register_start)}
            function(computer, *instruction[1:])
            if computer.registers == {i: val for i, val in enumerate(register_end)}:
                possibilities[op_num].add(instruction[0])
    return possibilities


if __name__ == '__main__':
    main()
