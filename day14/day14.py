import advent_tools


def main():
    part1, part2 = run_both_parts(advent_tools.read_all_integers()[0][0])
    print('Part 1:', part1)
    print('Part 2:', part2)


def run_both_parts(count):
    seq = [int(char) for char in str(count)]
    result = [3, 7]
    first_elf_pos = 0
    second_elf_pos = 1
    steps = count + 10
    part1_result = None
    while result[-len(seq):] != seq:
        new_recipe = result[first_elf_pos] + result[second_elf_pos]
        if new_recipe >= 10:
            result.append(new_recipe // 10)
            if len(result) >= steps and part1_result is None:
                part1_result = "".join(str(num) for num in result[-10:])
            if result[-len(seq):] == seq:
                break
        result.append(new_recipe % 10)
        if len(result) >= steps and part1_result is None:
            part1_result = "".join(str(num) for num in result[-10:])
        first_elf_pos = (first_elf_pos + 1 + result[first_elf_pos]) % len(result)
        second_elf_pos = (second_elf_pos + 1 + result[second_elf_pos]) % len(result)
    return int(part1_result), len(result) - len(seq)


if __name__ == '__main__':
    main()
