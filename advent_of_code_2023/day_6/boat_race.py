"""Advent of Code Day 6 Solution.

Source: https://adventofcode.com/2023/day/6

"""

import re

from collections import defaultdict
from math import prod, sqrt, ceil, floor

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


def real_quaradtic_roots(a: int, b: int, c: int) -> tuple[float, float]:
    """Get real roots of a quadratic equaton.

    Parameters
    ----------
    a : int
        Coefficient a.
    b : int
        Coefficient b.
    c : int
        Coeficient c.

    Returns
    -------
    tuple[float, float]
        Real roots of quadratice equation for provided a, b, c

    Raises
    ------
    ValueError
        When real roots do not exist.

    """
    # calculate the discriminant
    discriminant = b**2 - (4 * a * c)

    # handle case when no real roots exist
    if not discriminant > 0:
        raise ValueError(
            "Discriminant is not positive, therefore solutions are not real or"
            f" do not exist. Got discriminant = {discriminant}."
        )

    # get real solutions
    sol_1 = ((-1 * b) + sqrt(discriminant)) / (2 * a)
    sol_2 = ((-1 * b) - sqrt(discriminant)) / (2 * a)

    return sol_1, sol_2


def singlerace_winning_button_press_times(lines: list[str]) -> int:
    """Calculate the number of winning button press durations.

    Parameters
    ----------
    lines : list[str]
        Input contain race times and distance record.

    Returns
    -------
    int
        number of possible winning button pressing durations.

    """
    # split at : and take only the right hand side, repalce spaces and convert
    race_time = int(lines[0].split(":")[1].replace(" ", ""))
    record_dist = int(lines[1].split(":")[1].replace(" ", ""))

    # get roots to -t(b)**2 + t(r)t(b) - d(r) = 0
    # t(b): button press time, t(r): race time, d(r): race distance record
    solutions = real_quaradtic_roots(-1, race_time, -1 * record_dist)

    # get whole number of milliseonds that are still valid solutions
    min_button_time = ceil(solutions[0])
    max_button_time = floor(solutions[1])

    # add one since we need the number of combinations, not the range
    number_of_cases = max_button_time - min_button_time + 1

    return number_of_cases


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

    # part 2 solution
    num_scenarios = singlerace_winning_button_press_times(lines)
    print(
        "Part 2: Number of winning button press duration combinations is "
        f"{num_scenarios}"
    )
