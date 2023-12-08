"""Advent of Code Day 8 Solution.

Source: https://adventofcode.com/2023/day/8

"""

from advent_of_code_2023.utils import read_text_file

INPUT_FILENAME = "data/day_8/input.txt"


def number_steps(lines: list[str]) -> int:
    """Get the number of steps needed to reach node "ZZZ" from "AAA".

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

    # set up conditions, knowing at least 1 step is required
    num_steps = 1
    current_node = "AAA"
    for command in commands:
        # get the next node and end when "ZZZ" is found
        next_node = direction_map[current_node][command]
        if next_node == "ZZZ":
            break
        else:
            # continue searching, adding this direction back to the end of the
            # direction commands. Increment to cound the number of steps
            current_node = next_node
            num_steps += 1
            commands.append(command)

    return num_steps


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


if __name__ == "__main__":
    # prep input
    lines = read_text_file(INPUT_FILENAME)

    # part 1 solution
    num_steps = number_steps(lines)
    print(f"Part 1: Number of steps: {num_steps}")
