import advent_tools

CART_MARKERS = {
    "v": "|",
    "^": "|",
    ">": "-",
    "<": "-"
}

CART_STEP_MAP = {
    ("v", "|"): "v",
    ("v", "/"): "<",
    ("v", "\\"): ">",
    ("^", "|"): "^",
    ("^", "/"): ">",
    ("^", "\\"): "<",
    (">", "-"): ">",
    (">", "\\"): "v",
    (">", "/"): "^",
    ("<", "-"): "<",
    ("<", "/"): "v",
    ("<", "\\"): "^",
}

INTERSECTION_MAP = {
    ("v", 0): ">",
    ("v", 1): "v",
    ("v", 2): "<",
    (">", 0): "^",
    (">", 1): ">",
    (">", 2): "v",
    ("^", 0): "<",
    ("^", 1): "^",
    ("^", 2): ">",
    ("<", 0): "v",
    ("<", 1): "<",
    ("<", 2): "^",
}

DIRECTION_MAP = {
    "v": (0, 1),
    "^": (0, -1),
    ">": (1, 0),
    "<": (-1, 0),
}


def main():
    curr_map = advent_tools.read_input_no_strip()
    print('Part 1:', run_part_1(curr_map))
    print('Part 2:', run_part_2(curr_map))


def run_part_1(curr_map):
    underlying_map, carts = get_underlying_map(curr_map)
    crash = None
    while crash is None:
        crash, carts = take_one_step(underlying_map, carts)
    return crash


def get_underlying_map(start_pos):
    char_map = {char: char for char in r"/\|- +"}
    char_map.update(CART_MARKERS)
    map = []
    carts = {}
    for j, line in enumerate(start_pos):
        row = []
        for i, char in enumerate(line):
            row.append(char_map[char])
            if char in CART_MARKERS:
                carts[(i, j)] = (char, 0)
        map.append("".join(row))
    return map, carts


def take_one_step(underlying_map, old_carts):
    carts = old_carts.copy()
    crash = None
    for (i, j), (char, int_count) in sorted(old_carts.items()):
        if (i, j) in carts:
            delta_i, delta_j = DIRECTION_MAP[char]
            ii = i + delta_i
            jj = j + delta_j
            next_char = underlying_map[jj][ii]
            del carts[(i, j)]
            if (ii, jj) in carts:
                del carts[(ii, jj)]
                crash = (ii, jj)
            elif next_char == "+":
                fill_char = INTERSECTION_MAP[(char, int_count)]
                carts[(ii, jj)] = (fill_char, (int_count + 1) % 3)
            else:
                carts[(ii, jj)] = CART_STEP_MAP[(char, next_char)], int_count
    return crash, carts


def run_part_2(curr_map):
    underlying_map, carts = get_underlying_map(curr_map)
    while len(carts) > 1:
        _, carts = take_one_step(underlying_map, carts)
    return list(carts)[0]


if __name__ == '__main__':
    main()