"""Advent of code day 9 Solution.

Source: https://adventofcode.com/2023/day/9

"""

from advent_of_code_2023.utils import read_text_file

INPUT_FILEPATH = "data/day_9/input.txt"


def next_number(line: str) -> int:
    """Get the next number of the sequence using a 'diff to zero' type method.

    Continually get the difference between consequetive numbers until all the
    differences are zero. The next number in the sequence is then the sum of
    all the last differences.

    Parameters
    ----------
    line : str
        input line containing the sequence (space separated ints).

    Returns
    -------
    int
        Next number in the sequence.

    """
    # get the sequence digits and check if they are all zero
    i = 0
    arrs = [parse_line(line)]
    all_diffs = [x == 0 for x in arrs[i]]

    # continue to get the difference between consequitive numbers until all the
    # differences are zero
    while not all(all_diffs):
        arrs.append(get_diffs(arrs[i]))
        i += 1
        all_diffs = [x == 0 for x in arrs[i]]

    # get the sum of all the last values
    sum_last_vals = sum([arr[-1] for arr in arrs])

    return sum_last_vals


def get_diffs(nums: list[int]) -> list[int]:
    """Get the differences between sconsecuitive numbers.

    Note: list will have 1 element less than the input

    Parameters
    ----------
    nums : list[int]
        seqeunence of numbers

    Returns
    -------
    list[int]
        differences between consequtive sequence numbers

    """
    return [nums[i + 1] - nums[i] for i in range(0, len(nums) - 1)]


def parse_line(line: str) -> list[int]:
    """Parse an input line into a list of integers.

    Parameters
    ----------
    line : str
        input line

    Returns
    -------
    list[int]
        input line split at spaces and all digits converts to ints.

    """
    return [int(x) for x in line.split(" ")]


if __name__ == "__main__":
    # prep data
    lines = read_text_file(INPUT_FILEPATH)

    # part 1 solution
    sum_next_nums = sum([next_number(line) for line in lines])
    print(f"Part 1: Sum of next numbers is {sum_next_nums}")
