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


def text_to_digit(line: str) -> str:
    """Convert test representations of numbers into digits.

    Detects instances of digits in text form and converts them. Conversion
    preserves the order of text occurances. Also handles the case where the
    last character is used as the start of the next digit.

    Parameters
    ----------
    line : str
        line from input file to convert

    Returns
    -------
    str
        line after text to digit conversion

    """
    # record text to digit lookup
    TEXT_DIGIT = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    # record the occurance index for each possible text value (-1 if absent)
    start_positions = {}
    for text in TEXT_DIGIT.keys():
        start_idx = line.find(text)
        if start_idx != -1:
            start_positions[text] = line.find(text)

    # if text is found, sort the occurances and replace them in order
    # preserving the last character incase it's reused for the next text
    if start_positions != {}:
        sorted_texts = sorted(start_positions.items(), key=lambda x: x[1])
        for sorted_text, _ in sorted_texts:
            line = line.replace(sorted_text[:-1], TEXT_DIGIT[sorted_text])

    return line


if __name__ == "__main__":
    # part 1 solution
    # read in file and decode directly
    lines = read_calibration_file("data/day_1/calibration_input.txt")
    decoded_lines = decode_lines(lines)
    print(f"Part 1: Sum of decoded lines is {sum(decoded_lines)}")

    # part 2 solution
    # read in file, convert text to digits, then decode
    lines = read_calibration_file("data/day_1/calibration_input.txt")
    lines = [text_to_digit(line) for line in lines]
    decoded_lines = decode_lines(lines)
    print(f"Part 2: Sum of decoded lines is {sum(decoded_lines)}")
