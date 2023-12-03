"""Advent of Code day 3 solution.

Source: https://adventofcode.com/2023/day/3

"""

import re

from advent_of_code_2023.utils import read_text_file

INPUT_FILE = "data/day_3/input.txt"


def get_part_numbers_and_gear_ratios(lines: list[str]) -> list[int]:
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
    # create variable to prevent reuse and initialise some empty lists and
    # start a log of gear positions
    num_lines = len(lines)
    num_cols = len(lines[0])
    part_nums = []
    gears_log = {}

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

                # update gear records
                gears_log = update_gears_log(
                    gears_log,
                    potential_pn,
                    char_search_string,
                    max_col,
                    min_col,
                    min_row,
                )

    gear_powers = calculate_gear_ratios(gears_log)

    return part_nums, gear_powers


def update_gears_log(
    log: dict,
    pn: str,
    search_string: str,
    max_col: int,
    min_col: int,
    min_row: int,
) -> dict:
    """Update the gear position logs.

    This updates the records of gear positions if the part number is next to a
    gear symbol. A gear's symbol is an asterix (*). If one is found, it's
    coordinates are translated to row/col format and the part number is logged
    against that gear.

    Parameters
    ----------
    log : dict
        record of gear positions and neighbouring part numbers
    pn : str
        part number to check and update
    search_string : str
        string to search for gears
    max_col : int
        max possible gear column position index
    min_col : int
        min possible gear column position index
    min_row : int
        min possible gear row position

    Returns
    -------
    dict
        gear records, updated with the gear/pn pair if a gear is detected.

    """
    pn_by_gear = re.search(r"\*", search_string)
    if pn_by_gear:
        # get it's index and translate to row/column coordinates
        gear_idx = pn_by_gear.start()
        gear_col = (gear_idx % (max_col - min_col)) + min_col
        gear_row = min_row + int(gear_idx / (max_col - min_col))

        # update the logs with the part number
        gear_id = (gear_row, gear_col)
        if gear_id not in log.keys():
            log[gear_id] = []
        log[gear_id].append(int(pn))

    return log


def calculate_gear_ratios(gear_log: dict) -> dict:
    """Calculate the gear ratios.

    Take the gear logs and calculate its power only when 2 part numbers are in
    its proximity.

    Parameters
    ----------
    gear_log : dict
        gear position and neighbouring part number logs.

    Returns
    -------
    gear_powers : dict
        records of gear powers. keys are the row/col index of the input data
        (same as gear log)

    """
    gear_powers = {}
    for gear_id, pns in gear_log.items():
        if len(pns) == 2:
            gear_powers[gear_id] = pns[0] * pns[1]
    return gear_powers


if __name__ == "__main__":
    # get schematic input
    lines = read_text_file(INPUT_FILE)
    pns, gear_powers = get_part_numbers_and_gear_ratios(lines)

    # part 1 solution
    print(f"Part 1: Sum of found part number is {sum(pns)}")

    # part 2 solution
    print(f"Part 2: Sum of gear powers is {sum(list(gear_powers.values()))}")
