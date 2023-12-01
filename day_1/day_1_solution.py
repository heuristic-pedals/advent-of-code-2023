"""Day 1 solution for advent of code 2023.

Source: https://adventofcode.com/2023/day/1

"""

import re


def read_calibration_file(path: str) -> list:
    """Read calibration file.

    Read in contents of a text file and strip out end of line characters.

    Parameters
    ----------
    path : str
        path to input calibration file

    Returns
    -------
    list
        list of file contents, each element is a line

    """
    with open(path, "r") as f:
        lines = f.readlines()

    lines = [line.strip("\n") for line in lines]

    return lines


def decode_lines(lines: list) -> list:
    """Decode lines to build calibration.

    Cleans inputs to only contains numerical digits. Then takes first and last
    digit to build calibration codes.

    Parameters
    ----------
    lines : list
        lines from input calibration file

    Returns
    -------
    list
        corresponding calibration output for each line in lines.

    """
    # strip out non numeric characters
    only_digits = [re.sub("[^0-9]+", "", line) for line in lines]

    # get first + last digit (or only digit)
    cal_vals = [int(digits[0] + digits[-1]) for digits in only_digits]

    return cal_vals


if __name__ == "__main__":
    # part 1 solution
    lines = read_calibration_file("data/day_1/calibration_input.txt")
    decoded_lines = decode_lines(lines)
    print(f"Part 1: Sum of decoded lines is {sum(decoded_lines)}")
