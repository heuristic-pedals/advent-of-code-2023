"""Advent of code day 9 Solution.

Source: https://adventofcode.com/2023/day/9

"""

from advent_of_code_2023.utils import read_text_file

INPUT_FILEPATH = "data/day_9/input.txt"


def extrapolate_sequence(line: str, extrapolate_back=False) -> int:
    """Extrapolate the sequence using a 'diff to zero' type method.

    Continually get the difference between consequetive numbers until all the
    differences are zero. Then extrapolate to get the past or future number of
    the original sequence.

    Parameters
    ----------
    line : str
        Input line containing the sequence (space separated ints).
    extrapolate_back : bool, optional
        Used to control whether to calculate the past of future number. By
        default False, meaning the future number will be extrapolated. Set to
        True when extrapolating to the past number is desired.

    Returns
    -------
    int
        Next number in the sequence.

    """
    # get the sequence digits and check if they are all zero
    i = 0
    arrs = [parse_line(line, extrapolate_back=extrapolate_back)]
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


def parse_line(line: str, extrapolate_back=False) -> list[int]:
    """Parse an input line into a list of integers.

    When extrapolated_back is True, the sequence is reversed so that the past
    number can be extrapolated using the same methods.

    Parameters
    ----------
    line : str
        input line
    extrapolate_back : bool, optional
        Used to reverse the sequence of numbers when extrapolating backwards.

    Returns
    -------
    list[int]
        input line split at spaces and all digits converts to ints.

    """
    nums = [int(x) for x in line.split(" ")]
    if extrapolate_back:
        nums.reverse()
    return nums


if __name__ == "__main__":
    # prep data
    lines = read_text_file(INPUT_FILEPATH)

    # part 1 solution
    sum_next_nums = sum([extrapolate_sequence(line) for line in lines])
    print(f"Part 1: Sum of next numbers is {sum_next_nums}")

    # part 2 solution
    sum_first_nums = sum(
        [extrapolate_sequence(line, extrapolate_back=True) for line in lines]
    )
    print(f"Part 2: Sum of first numbers is {sum_first_nums}")
