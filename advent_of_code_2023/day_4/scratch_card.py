"""Advent of Code Day 4 solution.

Source: https://adventofcode.com/2023/day/4

"""

import re

from typing import Tuple

from advent_of_code_2023.utils import read_text_file

INPUT_FILE = "data/day_4/input.txt"


def calculate_game_score(line: str) -> Tuple[int, int]:
    """Calculate the scratch card game score.

    The input game string is of the expected format:
    'Game <ID>: X X X X X | Y Y Y Y Y Y Y Y'. This is firstly parsed for the
    <ID>. The wining numbers (X) and the elf's scratch card numbers (Y) are
    then parsed, and checked for consistency. Score is calculated based on the
    number of matches (n): 2 ** (n-1) (if n > 0, else 0). See the notes section
    for more details.

    Parameters
    ----------
    line : str
        an input game string

    Returns
    -------
    Tuple[int, int]
        the game id (index 0) and the game's score (index 1).

    Raises
    ------
    ValueError
        Raises a value error if:
        - unable to detect a game id
        - the number of winning/scratch card numbers detected is different from
        the expected value.
        - when duplicate values are detected within the set winning numbers or
        scratch card numbers.

    Notes
    -----
    The number of X's and Y's vary between the test and actual inputs. This is
    handled using "test" in the input file name. If this is absent, the actual
    input's expected number of X's and Y's is used.

    """
    # split out card name and number segments either side of the :
    card_name, card_numbers = line.split(":")

    # parse out the card id, raising an error if it could not detect one
    card_id_match = re.search("[0-9]+", card_name)
    if card_id_match:
        card_id = card_id_match.group()
    else:
        ValueError("Unable to find a card id.")

    # split out the winning numbers and the elf's scratch card numbers at |
    winning_inputs, elf_inputs = card_numbers.split("|")

    # knife and fork the numbers out of each segment using finditer - no real
    # reason other than re.findall() is dead to me after yesterday...
    winning_numbers = [
        int(num.group()) for num in re.finditer("[0-9]+", winning_inputs)
    ]
    elf_numbers = [
        int(num.group()) for num in re.finditer("[0-9]+", elf_inputs)
    ]

    # check if the number of numbers detected matches expectations
    if "test" in INPUT_FILE:
        checks = [5, 8]
    else:
        checks = [10, 25]
    if len(winning_numbers) != checks[0]:
        raise ValueError(
            f"Detected {len(winning_numbers)} winning numbers. Should be 10."
        )
    if len(elf_numbers) != checks[1]:
        raise ValueError(
            f"Detected {len(elf_numbers)} elf numbers. Should be 25."
        )

    # also check the case where duplicates are within the winning or elfs
    # subset of numbers - don't trust advent of code after yesterday!
    distinct_win_nums = set(winning_numbers)
    if len(distinct_win_nums) != len(winning_numbers):
        raise ValueError("Duplicate number detected in winning numbers")
    distinct_elf_nums = set(elf_numbers)
    if len(distinct_elf_nums) != len(elf_numbers):
        raise ValueError("Duplicate number detected in elf numbers.")

    # get the common numbers and calculate the score.
    common_nums = distinct_win_nums.intersection(distinct_elf_nums)
    if len(common_nums) > 0:
        points = 2 ** (len(common_nums) - 1)
    else:
        points = 0

    return card_id, points


if __name__ == "__main__":
    # get input
    lines = read_text_file(INPUT_FILE)

    # part 1 solution
    game_scores = [calculate_game_score(line) for line in lines]
    total_game_scores = sum([game[1] for game in game_scores])
    print(f"Part 1: Sum of game scores is {total_game_scores}")
