"""Advent of Code Day 4 solution.

Source: https://adventofcode.com/2023/day/4

"""

import re

from collections import defaultdict
from typing import Tuple, Type

from advent_of_code_2023.utils import read_text_file

INPUT_FILE = "data/day_4/input.txt"


def calculate_game_score(line: str) -> Tuple[int, int, int]:
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
    Tuple[int, int, int]
        the game id (index 0), the game's score (index 1), and the number of
        matching numbers (index 2).

    Raises
    ------
    ValueError
        Raises a value error if:
        - unable to detect a game id
        - the number of winning/scratch card numbers detected is different from
        the expected value.
        - when duplicate values are detected within the set winning numbers or
        scratch card numbers.

    See Also
    --------
    advent_of_code_2023.day_4.calculate_number_of_cards, which calculates the
    number of card occurances (including copies of subsiquent wins).

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
        card_id = int(card_id_match.group())
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

    return card_id, points, len(common_nums)


def get_copies(id: int, num_match: int) -> list:
    """Calculate ids of scratch card copies.

    Parameters
    ----------
    id : int
        card id
    num_match : int
        number to name (after the id)

    Returns
    -------
    list
        ids the following num_match number of card ids.

    """
    return list(range(id + 1, id + num_match + 1))


def calculate_number_of_cards(lines: list[str]) -> Type[defaultdict[int]]:
    """Calculate the number of occurances of each card.

    Recursively calculates the number of scratch card occurances, including
    those that are 'copies' of previous scratch cards 'wins' up to the point
    where no further scratch cards are won.

    Parameters
    ----------
    lines : list[str]
        input corresponding to all the scratch card game strings.

    Returns
    -------
    Type[defaultdict[int]]
        counts of scratch card occurances (values) per card id (keys).

    See Also
    --------
    advent_of_code_2023.day_4.calculate_game_score, which calculates the scores
    per game.

    Notes
    -----
    This method is based off the number of matching numbers, not the scratch
    card scores.

    """
    # create record of number of matches (values) for each game id (keys)
    game_scores = [calculate_game_score(line) for line in lines]
    matching_nums = {game[0]: game[2] for game in game_scores}

    # instantiate a default dict - faster than normal dicts + don't need to
    # initially check if the key is present
    counts = defaultdict(int)

    for id, num_matches in matching_nums.items():

        # add one for the original card and get it's copies
        counts[id] += 1
        copies_ids = get_copies(id, num_matches)

        for copy_id in copies_ids:
            # get the it's copies and append them to the original copies list
            # this means all future copies will also be analysed in this way
            copy_copies_ids = get_copies(copy_id, matching_nums[copy_id])
            for copy_copies_id in copy_copies_ids:
                copies_ids.append(copy_copies_id)

        # add counts of each copy
        for copy in copies_ids:
            counts[copy] += 1

    return counts


if __name__ == "__main__":
    # get input
    lines = read_text_file(INPUT_FILE)

    # part 1 solution
    game_scores = [calculate_game_score(line) for line in lines]
    total_game_scores = sum([game[1] for game in game_scores])
    print(f"Part 1: Sum of game scores is {total_game_scores}")

    # part 2 solution
    card_counts = calculate_number_of_cards(lines)
    total_number_cards = sum([v for v in card_counts.values()])
    print(f"Part 2: Total number of scratch cards is {total_number_cards}")
