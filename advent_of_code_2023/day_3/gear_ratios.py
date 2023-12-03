"""Advent of Code day 3 solution.

Source: https://adventofcode.com/2023/day/3

"""

import re

from advent_of_code_2023.utils import read_text_file

INPUT_FILE = "data/day_3/input.txt"


def get_part_numbers(lines: list[str]) -> list[int]:
    """Extract part numbers from a schematic.

    Part numbers are decoded by finding special characters surrounding (inc.
    diagonals) the number itself.

    Parameters
    ----------
    lines : list[str]
        lines of the schematic input

    Returns
    -------
    list[int]
        valid part numbers

    """
    # create variable to prevent reuse and initialise some empty lists
    num_lines = len(lines)
    num_cols = len(lines[0])
    part_nums = []

    for i in range(0, num_lines):
        # extract all the numbers and their start/end indcies
        # use finditer to go through all numbers in a line
        potential_part_nums_in_line = []
        for match in re.finditer("[0-9]+", lines[i]):
            potential_part_nums_in_line.append(
                (match.group(), match.start(), match.end())
            )

        # get index of row above + below, limiting top/bot out of bounds cases
        min_row = i - 1 if i != 0 else 0
        max_row = i + 1 if i != num_lines - 1 else num_lines - 1

        for potential_pn, start, end in potential_part_nums_in_line:
            # also limit column indices - to form a grid around the number
            min_col = start - 1 if start != 0 else 0
            max_col = end + 1 if end != num_cols else num_cols

            # flatten the grid surrounding the number into a single string
            char_search_string = []
            for row in range(min_row, max_row + 1):
                char_search_string.append(lines[row][min_col:max_col])
            char_search_string = "".join(char_search_string)

            # part number when anything other than a digit or . is present
            char_match = re.search(r"[^0-9\.]+", char_search_string)
            if char_match:
                part_nums.append(int(potential_pn))

    return part_nums


if __name__ == "__main__":
    # get schematic input
    lines = read_text_file(INPUT_FILE)

    # part 1 solution
    pns = get_part_numbers(lines)
    print(f"Part 1: Sum of found part number is {sum(pns)}")
