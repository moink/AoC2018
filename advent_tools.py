"""Tools to help solve advent of code problems faster"""
import abc
import collections
import contextlib
import copy
import datetime
import hashlib
import itertools
import os
import re
import shutil
import urllib.request


import scipy
from matplotlib import pyplot as plt
import numpy as np


def set_up_directory(day):
    """Make a new directory for working on an advent of code problem

    Args:
        day: int
            day of the month to work on

    Returns:
        new_dir: str
            path to the directory for that day
    """
    this_dir = os.path.dirname(__file__)
    new_dir = os.path.join(this_dir, 'day' + str(day))
    with contextlib.suppress(FileExistsError):
        os.mkdir(new_dir)
    new_file_name = os.path.join(new_dir, 'day' + str(day) + '.py')
    template_file_name = os.path.join(this_dir, 'template.py')
    if not(os.path.exists(new_file_name)):
        shutil.copy(template_file_name, new_file_name)
    return new_dir


def download_input_data(day, new_dir):
    """Download input data for an advent of code problem

    Args:
        day: int
            day of the month to work on
        new_dir: str
            path to the directory for that day

    Returns:
        None
    """
    with open('session_cookie.txt') as cookie_file:
        session_cookie = cookie_file.read()
    url = f'https://adventofcode.com/2018/day/{day}/input'
    opener = urllib.request.build_opener()
    opener.addheaders = [('cookie', 'session=' + session_cookie)]
    urllib.request.install_opener(opener)
    input_file = os.path.join(new_dir, 'input.txt')
    urllib.request.urlretrieve(url, input_file)


def start_coding(day):
    """Prepare to code an advent of code problem

    Args:
        day: int
            day of the month to work on

    Returns:
        None
    """
    new_dir = set_up_directory(day)
    download_input_data(day, new_dir)


def start_coding_today():
    """Prepare to code today's advent of code problem"""
    day_of_month = datetime.datetime.today().day
    start_coding(day_of_month)


def read_input_lines():
    """Open today's input data and return it as a list of lines

    Returns:
        [str]
            Lines in 'input.txt'
    """
    with open('input.txt') as in_file:
        data = in_file.read().strip().splitlines()
    return data

def read_input_no_strip():
    """Open today's input data and return it as a list of lines

    Returns:
        [str]
            Lines in 'input.txt'
    """
    with open('input.txt') as in_file:
        data = in_file.read().splitlines()
    return data


def read_whole_input():
    """Open today's input data and return it as a single string

    Returns:
        str
            Contents of 'input.txt'
    """
    with open('input.txt') as in_file:
        data = in_file.read().strip()
    return data


def count_times_true(function):
    """Count the number of times some function is true for the input lines

    Args:
        function: callable
            A function that takes a string and returns a boolean

    Returns:
        count: int
            The number of times the function returns True, when evaluated
            over each line of the file 'input.txt'
    """
    strings = read_input_lines()
    valid = [function(string) for string in strings]
    return sum(valid)


def dict_from_input_file(sep = ' => ', key='left'):
    """Read today's input.txt as a dictionary

    Args:
        sep: str
            Separator between the key and value on each line
        key: str
            'left' or 'right' - which side of the separator is the key (the
            other side is the value)

    Returns:
        result: {str: str}
            Dictionary version of today's input.txt, with each line
            converted to a key value pair
    """
    result = {}
    lines = read_input_lines()
    for line in lines:
        left, right = line.split(sep)
        if key.lower() == 'left':
            result[left.strip()] = right.strip()
        else:
            result[right.strip()] = left.strip()
    return result


def dict_of_list_from_file(sep = ' => ', key='left'):
    """Read today's input.txt as a dictionary of lists

        Args:
            sep: str
                Separator between the key and value on each line
            key: str
                'left' or 'right' - which side of the separator is the key (the
                other side is one element of the value)

        Returns:
            result: {str: [str]}
                Dictionary version of today's input.txt, with the value from
                each line in the list with that key
        """
    result = collections.defaultdict(list)
    lines = read_input_lines()
    for line in lines:
        left, right = line.split(sep)
        if key.lower() == 'left':
            result[left.strip()].append(right.strip())
        else:
            result[right.strip()].append(left.strip())
    return dict(result)

class PlottingGrid:
    """A tool for maintaining and plotting a grid of numbers

    Not abstract, since it works on its own, but designed to be inherited
    with some methods added that manipulate self.grid between construction
    and showing

    One note, always use self.grid(y, x) to get and set values, with the
    column first and the row second. It's weird, but that's how numpy works
    with plotting
    """

    def __init__(self, shape):
        """Constructor

        Args:
            shape: (int, int)
                Number of rows and number of columns in the grid
        """
        self.grid = np.zeros(shape, dtype=int)

    def read_input_file(self, char_map):
        """Read and store the grid from today's input file

        Args:
            char_map: {str: int}
                Mapping of characters in the file to integers in the numpy
                array. For example {'.' : 0, '#' : 1} which is typical
                Topaz-notation for a maze with open areas and walls
        Returns:

        """
        lines = read_input_no_strip()
        for y_pos, line in enumerate(lines):
            for x_pos, char in enumerate(line):
                self.grid[y_pos, x_pos] = char_map[char]

    def show(self):
        """Show the grid in a new window

        Execution will be suspended until the window is closed

        Returns:
            None
        """
        plt.clf()
        plt.imshow(self.grid)
        plt.colorbar()
        plt.show()

    def draw(self, pause_time=0.01):
        """Draw the grid in a new window

        Execution will be paused for pause_time but not stopped. Note that
        the screen will close after the pause time. It is advised to use
        this method while animating but then to run show() at the end

        Args:
            pause_time: float
                Number of seconds to pause after drawing

        Returns:
            None
        """
        plt.clf()
        plt.imshow(self.grid)
        plt.colorbar()
        plt.draw()
        plt.pause(pause_time)

    def sum(self):
        """Returns the sum of the values in the grid

        Returns:
            sum : int
                Sum of the values stored in this object's grid
        """
        return np.sum(self.grid)

    def count(self):
        """Count of non-zero elements in the grid

        Returns:
            count : int
                Count of elements of this object's grid which are non-zero
        """
        return np.sum(self.grid != 0)


class GameOfLife(PlottingGrid):
    """Implementation of Conway's Game Of Life

    Works as is - you are most likely to want to change
    self.convolve_matrix, or walls_treated_as, or to overwrite
    evaluate_where_on

    In 2015 day 18 part 2 I also had to change read_input_file (inherited
    from PlottingGrid) to turn the corner lights on initially (they were
    stuck on in the problem description).
    """
    # This is all eight neighbours
    convolve_matrix = np.asarray([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    # If you wanted just four neighbours, do instead:
    # convolve_matrix = np.asarray([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    walls_treated_as = 0

    def count_neighbours(self):
        """Count the number of neighbours each grid point has"""
        count = scipy.signal.convolve2d(self.grid, self.convolve_matrix,
                                        mode='same', boundary='fill',
                                        fillvalue=self.walls_treated_as)
        return count

    def one_step(self):
        """Take one game of life step"""
        counts = self.count_neighbours()
        self.evaluate_where_on(counts)
        self.draw()

    def evaluate_where_on(self, counts):
        """Set the grid to the right setting based on the neighbour count

        Args:
            counts: np.ndarray
                Number of neighbours of each node that are on

        Returns:
            None
        """
        # For grid points that are on, if count is 2 or 3, keep on
        # Otherwise turn off
        self.grid = np.where(np.logical_and(self.grid == 1,
                                            np.logical_or(counts == 2,
                                                          counts == 3)), 1, 0)
        # For grid points that are off, if count is 3, turn on
        # Otherwise keep the same as grid calculated in previous step
        self.grid = np.where(np.logical_and(self.grid == 0, counts == 3), 1,
                             self.grid)

    def simulate_n_steps(self, num_steps):
        """Take a defined number of steps of the Game of Life

        Args:
            num_steps: int
                Number of steps to take

        Returns:
            None
        """
        for i in range(num_steps):
            self.one_step()
        self.show()

class StateForGraphs(abc.ABC):
    """A starter for a state class for use in graph traversal

    One requirement to make this work in number_of_bfs_steps, below, is to
    implement __hash__ and __eq__. What I have found is the simplest way to do
    that is to make a unique string representation of each step, and use
    that to hash and compare the object. That's what's used by default here,
    so that only __str__ must be implemented by the child object. But if
    that doesn't work, just override __hash__ and __eq__ directly.

    The second requirement is to implement possible_next_states,
    which provides the edges of the graphs connected to this node, or state.
    That's where the real meat of the problem will end up.

    The third requirement is to implement is_final, which tells the BFS
    search when it has reached the destination node.

    Notes for optimization of breadth-first searches:
        - If two states are equivalent in some way, as in the steps required
            don't depend on any differences between them, make their string
            representations the same, so that they compare as equal
        - Look for patterns in the best strategies. Don't return paths
            guaranteed to be suboptimal from possible_next_states
    """

    @abc.abstractmethod
    def __str__(self):
        """Return string representation. Used for hashing and comparing equal
        """
        pass

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)

    @abc.abstractmethod
    def is_final(self):
        """Whether this is the final, destination node in the search

        Returns:
            is_final_node : bool
        """
        return False

    @abc.abstractmethod
    def possible_next_states(self):
        """Create and return states reachable from this one in one step

        This is where the details of the problem go. This should return a
        set of valid states reachable from the current state in one step.

        For optimization reasons, it is best to reject steps known to be
        globally suboptimal in this method, by not returning them. The fewer
        states this method returns, the faster the search will go. But if
        the globally optimal next state is not contained in the result,
        the search will not find the minimum number of steps.

        Returns:
            Set of StateForGraphs
                States reachable from this state in one step
        """
        return set(copy.deepcopy(self))


def number_of_bfs_steps(current_state):
    """Perform a breadth-first search and return number of steps taken

    Args:
        current_state: StateForGraphs
            The state at the beginning of the search; the root of the tree.

    Returns:
        The number of steps required to get from current_state to
        a final state, using state.possible_next_states to find states
        reachable in one step from the current state

    See Also: StateForGraphs
        to understand the required methods for the states used in the graph.
        The states must implement __hash__, __eq__, possible_next_states,
        and is_final
    """
    queue = collections.deque()
    discovered = {current_state: 0}
    queue.append(current_state)
    while queue:
        state = queue.popleft()
        num_steps = discovered[state]
        new_states = state.possible_next_states()
        for new_state in new_states:
            if new_state.is_final():
                return num_steps + 1
            if new_state not in discovered:
                discovered[new_state] = num_steps + 1
                queue.append(new_state)


def number_of_reachable_in_steps(current_state, max_steps):
    """Find the number of states reachable from this one in max steps

    Use a breadth-first search to figure out how many states are reachable
    from the current state, with a maximum of max_steps steps, when each state
    can provide the states it can reach in one state.

    Args:
        current_state: StateForGraphs
            The state at the beginning of the search; the root of the tree.
        max_steps: int
            The maximum number of steps to take, using
            state.possible_next_states to find states reachable in one step
            from the current state

    Returns:
        number_reachable : int
            Number of distinct states reachable from current_state,
            with fewer or equal to max_steps steps.

    See Also: StateForGraphs
        to understand the required methods for the states used in the graph.
        The states must implement __hash__, __eq__, and possible_next_states
    """
    queue = collections.deque()
    discovered = {current_state: 0}
    queue.append(current_state)
    while queue:
        state = queue.popleft()
        num_steps = discovered[state]
        if num_steps < max_steps:
            new_states = state.possible_next_states()
            for new_state in new_states:
                if new_state not in discovered:
                    discovered[new_state] = num_steps + 1
                    queue.append(new_state)
    return len(discovered)


def longest_path(current_state):
    """Find longest possible path from the current state to the final state

    Args:
        current_state: StateForGraphs
            The state at the beginning of the search; the root of the tree.

    Returns:
        The maximum number of steps that can be used to get from
        current_state to a final state, using state.possible_next_states to
        find states reachable in one step from the current state

    See Also: StateForGraphs
        to understand the required methods for the states used in the graph.
        The states must implement __hash__, __eq__, possible_next_states,
        and is_final
    """
    queue = collections.deque()
    discovered = {current_state: 0}
    queue.append(current_state)
    lengths = set()
    while queue:
        state = queue.popleft()
        num_steps = discovered[state]
        new_states = state.possible_next_states()
        for new_state in new_states:
            if new_state.is_final():
                lengths.add(num_steps + 1)
            elif new_state not in discovered:
                queue.append(new_state)
            discovered[new_state] = num_steps + 1
    return max(lengths)


def find_final_state(current_state):
    """Return the final state found in shortest steps using a BFS search

    Args:
        current_state: StateForGraphs
            The state at the beginning of the search; the root of the tree.

    Returns:
        final_state: StateForGraphs
            The first state that returns true for its is_final method,
            when using a breadth-first search

    See Also: StateForGraphs
        to understand the required methods for the states used in the graph.
        The states must implement __hash__, __eq__, possible_next_states,
        and is_final
    """
    queue = collections.deque()
    discovered = {current_state: 0}
    queue.append(current_state)
    while queue:
        state = queue.popleft()
        num_steps = discovered[state]
        new_states = state.possible_next_states()
        for new_state in new_states:
            if new_state.is_final():
                return new_state
            if new_state not in discovered:
                discovered[new_state] = num_steps + 1
                queue.append(new_state)


class Computer(abc.ABC):
    """A virtual machine base class for running custom assembly languages

    Seems that Topaz likes to put problems that require virtual machines
    with registers that run his own small assembly languages. There was one
    in 2015 (day 23) and one in 2016 (day 12) and a much more complex one
    used on many days in 2019. This probably doesn't implement enough for
    the 2019 IntCode computer but it works for 2015 and 2016.

    To use this, inherit from this class. Include the following two lines at
    the start of the class:
        operation = advent_tools.Computer.operation
        return_register = 'a'
    (setting return_register to the register that the question requests) and
    then decorate all assembly commands with @operation('cmd') where cmd is
    the first word of the instruction to call that command. The operations
    can use self.registers to access the computer's registers
    """

    operation_map = {}

    def __init__(self):
        self.registers = collections.defaultdict(int)
        self.instruction_pointer = 0

    @property
    @abc.abstractmethod
    def return_register(self):
        """The register to return at the end of the program"""
        pass

    @classmethod
    def operation(cls, instruction_first_word):
        """Mark a method as an operation

        Args:
            instruction_first_word: str
                First word of the instruction, the part that indicates which
                operation to run

        Returns:
            A decorator which marks the method as an operation
        """
        def decorator(func):
            """Decorator to mark a method as an operation"""
            cls.operation_map[instruction_first_word] = func
            return func
        return decorator

    def run_instruction(self, instruction):
        """Run a single instruction

        Using the first word of the instruction, figure out what operation
        to run. Pass the rest of the words of the instruction as an argument.

        Args:
            instruction: str
                Instruction to run. Must start with a valid operation
                identifier (key of self.operation_map)

        Returns:
            None
        """
        words = instruction.split()
        func = self.operation_map[words[0]]
        func(self, *words[1:])

    def get_key_or_val(self, key_or_val):
        """Get either a register value or the value of an integer

        Args:
            key_or_val: str
                Name of the register to get, or explicit value (the string
                representation of an integer)

        Returns:
            val: int
                If key_or_val can be converted to an integer, that integer.
                Otherwise, the value in the register with that name
        """
        try:
            val = int(key_or_val)
        except ValueError:
            val = self.registers[key_or_val]
        return val

    def run_program(self, program):
        """Run a list of instructions through the virtual machine

        The program terminates when the instruction pointer moves past the
        end of the program

        Args:
            program: [str]
                Instructions, each of which starts with a valid operation
                identifier
        Returns:
            int
                Contents of the return register when the program terminates
        """
        while True:
            try:
                line = program[self.instruction_pointer]
            except IndexError:
                return self.registers[self.return_register]
            self.run_instruction(line)
            self.instruction_pointer = self.instruction_pointer + 1

    def run_input_file(self):
        """Run the contents of today's input file through the virtual machine

        Returns:
            int
                Contents of the return register when the program terminates
        """
        program = read_input_lines()
        return self.run_program(program)


def md5_increment(salt):
    """Append an increasing integer to the salt and run an md5 hash on it

    Args:
        salt: str
            First characters of the string to be hashed. The remaining
            characters are increasing integers starting at 0

    Yields:
        md5_hash : str
            An md5 hash of the salt prepended to an integer
    """
    for count in itertools.count():
        hashed = get_md5_hash(salt + str(count))
        yield count, hashed


def get_md5_hash(to_hash):
    """Calculate the md5 hash of a string

    Args:
        to_hash: str
            The string to hash

    Returns:
        md5_hash: str
            The hex value of the md5 hash
    """
    return hashlib.md5(to_hash.encode('utf-8')).hexdigest()


def chunk_iterable(iterable, chunk_size):
    """Break an iterable into chunks

    Args:
        iterable: iterable
            Iterable to break up
        chunk_size: int
            Size of chunks to break it into

    Yields:
        result: chunk_size-tuple
            Chunk of the data
    """
    for result in itertools.zip_longest(*[iter(iterable)] * chunk_size):
        yield result


def get_inside_outside_brackets(data, start_char, end_char, nested=True):
    """Split string into portions inside and outside delimiters

    Args:
        data: str
            The string to parse
        start_char: str
            Character indicating the beginning of a delimited string
        end_char: str
            Character indicating the end of a delimited string
        nested: bool
            Optional, default True. Whether delimited strings can be nested.
            If True, this method counts the number of start_char and end_char,
            and only ends the delimited string when the number of end_char
            reaches the number of start_char. If False, the first end_char
            ends the delimited string.

    Returns:
        inside, outside: ([str], [str])
            Lists of strings that appear inside and outside the delimiters,
            respectively
    """
    outside = ['']
    inside = []
    in_brackets = False
    count = 0
    for pos, char in enumerate(data):
        if in_brackets:
            if char == end_char:
                count = count - 1
                if count == 0 or not nested:
                    in_brackets = False
                    outside.append('')
                else:
                    inside[-1] = inside[-1] + (char)
            else:
                inside[-1] = inside[-1] + (char)
                if char == start_char:
                    count = count + 1
        elif char == start_char:
            count = 1
            in_brackets = True
            inside.append('')
        else:
            outside[-1] = outside[-1] + char
    outside = [item for item in outside if item]
    return inside, outside

def recursive_inside_outside(data, start_char, end_char):
    """Recursively break up nested delimited strings

    Args:
        data: str
            The string to parse
        start_char: str
            Character indicating the beginning of a delimited string
        end_char: str
            Character indicating the end of a delimited string

    Returns: {str: [Object]}
        Keys are 'inside' and 'outside'. Value of 'outside' is a list
        containing strings that appear outside the delimited portion. The
        'inside' key contains a list of mixed strings (strings that appear
        inside singly-delimited portions of text) and dictionaries,
        which are the result of calling this method on the portion of the
    """
    inside, outside = get_inside_outside_brackets(data, start_char, end_char)
    inside_full = []
    for inside_part in inside:
        if start_char in inside_part:
            inside_full.append(recursive_inside_outside(inside_part,
                                                        start_char, end_char))
        else:
            inside_full.append(inside_part)
    return {'outside': outside, 'inside': inside_full}


def read_all_integers():
    """Read all the integers on each line of the input file

    Returns:
        integers: [[int]]
            All integers on each line of today's input file
    """
    result = []
    for line in read_input_lines():
        num_strings = re.findall(r'-?[0-9]+', line)
        nums = [int(num_str) for num_str in num_strings]
        result.append(nums)
    return result


if __name__ == '__main__':
    # start_coding_today()
    today = 3
    start_coding(today)
