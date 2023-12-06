"""Advent of Code Day 6 Solution.

Source: https://adventofcode.com/2023/day/6

"""

import re

from collections import defaultdict
from math import prod

from advent_of_code_2023.utils import read_text_file

INPUT_PATH = "data/day_6/input.txt"


def multirace_winning_button_press_times(lines: list[str]) -> defaultdict(int):
    """Calculate the number of winning button press combinations.

    This is done over all races. Each race has a time limit and a record
    distance. All possible button pressinng combinations are explored to
    determine if the distance record can be broken. The number of these
    possibilities is calcualted for each race independently.

    Parameters
    ----------
    lines : list[str]
        _description_

    Returns
    -------
    defaultdict(int)
        a defaul dict of race time limits (keys) and number of possible button
        press durations that break the distance record (values)

    """
    # split at : and take only the right hand side
    time_strs = lines[0].split(":")[1]
    dist_strs = lines[1].split(":")[1]

    # parse the strings and knife and fork out the integers
    times = [int(num.group()) for num in re.finditer("[0-9]+", time_strs)]
    dists = [int(num.group()) for num in re.finditer("[0-9]+", dist_strs)]

    # record number of scenarios which break records in this dict. Use a
    # default dict to avoid having to create keys and for speed.
    broken_records = defaultdict(int)

    # go through each race and every possible button pressing duration
    for race_time, record_dist in zip(times, dists):
        for button_time in range(0, race_time + 1):
            # move_time - time remaining after pressing the button
            # move_speed - same magnitude as the button press duration
            # move_distance - speed * time
            move_time = race_time - button_time
            move_speed = button_time
            move_dist = move_speed * move_time

            # if the record is broken, add one to no. possible combinations
            if move_dist > record_dist:
                broken_records[race_time] += 1

    return broken_records


if __name__ == "__main__":
    # prep input
    lines = read_text_file(INPUT_PATH)

    # part 1 solution
    winning_presses = multirace_winning_button_press_times(lines)
    winning_prod = prod([v for v in winning_presses.values()])
    print(
        "Part 1: Product of the number of winning pressing combinations is "
        f"{winning_prod}"
    )
