"""Advent of Code Day 8 Solution.

Source: https://adventofcode.com/2023/day/8

"""

from functools import reduce
from math import gcd

from advent_of_code_2023.utils import read_text_file

INPUT_FILENAME = "data/day_8/input.txt"


def number_camel_steps(lines: list[str]) -> int:
    """Get the number of camel steps needed to reach node "ZZZ" from "AAA".

    Parameters
    ----------
    lines : list[str]
        input containing directions and current/next node information

    Returns
    -------
    int
        number of steps required to get from "AAA" to the "ZZZ" using the
        inputted commands

    """
    # map directions and get node maps
    commands = map_directions(lines[0])
    direction_map = get_node_map(lines[2:])

    # set up conditions and then keep moving through the map reaching "ZZZ"
    # needs to repeat whole sequence of instructions, so use outer while loop
    # to test the condition after applying all the direction commands
    num_steps = 0
    node = "AAA"
    while node != "ZZZ":
        for command in commands:
            node = direction_map[node][command]
            num_steps += 1

    return num_steps


def number_ghost_steps(lines: list[str]) -> int:
    """Calculate number of ghost steps needed to reach all nodes ending in "Z".

    'Simultaneous' are all locations ending in an "A". The number of steps for
    each starting location is calculated seperately. Then the number of steps
    when all locations would simultaneously end on a "Z" is the least common
    multiple.

    Parameters
    ----------
    lines : list[str]
        input containing directions and current/next node information

    Returns
    -------
    int
        number of steps required to get from a nodes ending in an "A" and to
        simultaneously arive at all respective nodes ending in a "Z"

    """
    # map directions and get node maps
    commands = map_directions(lines[0])
    direction_map = get_node_map(lines[2:])

    # get all the starting nodes, those ending in A
    starting_points = []
    for node in direction_map.keys():
        if node[-1] == "A":
            starting_points.append(node)

    starting_point_steps = []
    for starting_point in starting_points:
        # get the number of steps to reach a node ending in "Z" for each
        # starting point
        num_steps = 0
        node = starting_point
        while node[-1] != "Z":
            for command in commands:
                node = direction_map[node][command]
                num_steps += 1
        starting_point_steps.append(num_steps)

    # get the lowest common multiple - using reduce to apply the function
    # across all the elements in the list. Equivalent 'loopy' solution:
    # >>> lcm = 1
    # >>> for steps in starting_point_steps:
    # >>>    lcm = calculate_lcm(lcm, steps)
    lcm = reduce(calculate_lcm, starting_point_steps)

    return lcm


def map_directions(line: str) -> list[int]:
    """Map "L" and "R" directions to 0 and 1.

    This simplifies the indexing/selection of the next node.

    Parameters
    ----------
    line : str
        directions line of input file

    Returns
    -------
    list[int]
        directions mapped to 0 and 1 in order of occurance.

    """
    return [0 if direction == "L" else 1 for direction in line]


def get_node_map(lines: list[str]) -> dict[str, tuple[str, str]]:
    """Build a map between the current node to next nodes.

    Parses "<CURRENT_NODE> = (<NEXT_NODE_L>, <NEXT_NODE_R>)" into a map of
    current node (keys) and next nodes (values, tuple of L and R nodes).

    Parameters
    ----------
    lines : list[str]
        input lines, exluding the directions and empty rows.

    Returns
    -------
    dict
        current nodes (keys) mapped to their respective left and right nodes
        (values, as a tuple)

    """
    map_dict = {}
    for line in lines:
        loc, nodes = line.replace(" ", "").split("=")
        l_node, r_node = nodes.replace("(", "").replace(")", "").split(",")
        map_dict[loc] = (l_node, r_node)

    return map_dict


def calculate_lcm(x: int, y: int) -> int:
    """Calculate the Lowest Common Multiple.

    This is defined as x * y / GCD(x, y), where GCD is the greatest common
    denominator. See [1]_ for more details.

    Parameters
    ----------
    x : int
        input 1
    y : int
        input 2

    Returns
    -------
    int
        lowest common multiple between inputs x and y

    References
    ----------
    ..  [1] https://en.wikipedia.org/wiki/Least_common_multiple

    """
    # coherse to int type since / converts to float and output will be an int
    # needed when using reduce() since gcd() needs int input types
    return int((x * y) / gcd(x, y))


if __name__ == "__main__":
    # prep input
    lines = read_text_file(INPUT_FILENAME)

    # part 1 solution
    num_steps = number_camel_steps(lines)
    print(f"Part 1: Number of camel steps: {num_steps}")

    num_steps = number_ghost_steps(lines)
    print(f"Part 2: Number of ghost steps: {num_steps}")
