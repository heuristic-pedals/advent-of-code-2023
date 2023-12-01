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

    # keep going until all text instances have been converted
    while True:
        # record the occurance index for each possible text value (-1 if not
        # present)
        start_positions = {}
        for text in TEXT_DIGIT.keys():
            start_positions[text] = line.find(text)

        # drop cases where the text isn't present
        start_positions = {k: v for k, v in start_positions.items() if v != -1}

        # if text is found, get the text that starts earliest and replace
        # preserving the last character
        if start_positions != {}:
            earliest_text = min(start_positions, key=start_positions.get)
            line = line.replace(earliest_text[:-1], TEXT_DIGIT[earliest_text])
        else:
            break

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
