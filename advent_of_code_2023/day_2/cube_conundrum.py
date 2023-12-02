"""Solution for Advent of Code Day 2.

Source: https://adventofcode.com/2023/day/2

"""

import re

from typing import Tuple

from advent_of_code_2023.utils import read_text_file

# input file path
INPUT_PATH = "data/day_2/input.txt"

# limits which when exceeded make a game impossible
BALL_LIMITS = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def parse_game(game: str) -> Tuple[int, bool, int]:
    """Parse a game to determine plausability and power.

    Retrieves the game's id and determines its plausability and power
    considering ball counts by color across game sets.

    Plausability is defined by sets that have ball counts for all colors below
    (or equal to) the treshold for the color. If any count is above this
    theshold the whole game is deemed infeasible.

    Power is defined as the multiplcation of minimum possible ball counts by
    color. The minimum possible ball count for each color refers to be the
    maximum number of balls observed within a set, across all sets for that
    color.

    Parameters
    ----------
    game : str
        Input game string (line from input file).

    Returns
    -------
    Tuple[int, bool, int]
        Game outcome. First element is the game id. The second element is the
        outcome - game is possible when this is True.

    """
    # default assumption is game is possible
    possible = True

    # find and extract the game id
    game_id_match = re.findall("Game [0-9]*:", game)[0]
    game_id = int(re.sub("[^0-9]", "", game_id_match))

    # take the game id section out of the string (not needed anymore) and
    # split into game sets at semi colons
    game_sets = game.replace(game_id_match, "").split(";")

    # collect possible ball colors and instantiate minimum occurance records
    colors = BALL_LIMITS.keys()
    min_possible_balls = {k: 0 for k in colors}

    for game_set in game_sets:
        # get rid of the initial space and split balls at commas
        game_set = [re.sub("^ ", "", x) for x in game_set.split(",")]

        # initialise a counter
        set_color_counts = {k: 0 for k in colors}

        # extract number of balls, by color, for each ball in the game's set
        for ball in game_set:
            for color in colors:
                if color in ball:
                    count = int(re.sub("[^0-9]", "", ball))
                    set_color_counts[color] = count

        # impossible game when any ball count > the threshold for its color
        impossible = any(
            [set_color_counts[color] > BALL_LIMITS[color] for color in colors]
        )
        if impossible:
            possible = False

        # update the minimum possible ball count for each color after this set
        # if previous minimum is 0 and this set it's not zero, then update
        # also update if this set has and non zero count greater than what
        # has been seen previuosly
        for color in colors:
            if (
                (min_possible_balls[color] == 0)
                & (set_color_counts[color] > 0)
            ) | (
                (set_color_counts[color] > 0)
                & (set_color_counts[color] > min_possible_balls[color])
            ):
                min_possible_balls[color] = set_color_counts[color]

    # calculate the power - multiply all minium possible counts together
    power = 1
    for minimum_count in min_possible_balls.values():
        power *= minimum_count

    return game_id, possible, power


if __name__ == "__main__":
    # prep inputs and parse
    lines = read_text_file(INPUT_PATH)
    results = [parse_game(line) for line in lines]

    # part 1 solution
    possible_games_id_sum = sum([result[0] for result in results if result[1]])
    print(f"Part 1: Sum of possible game ids is {possible_games_id_sum}.")

    # part 2 solution
    sum_of_power = sum([result[2] for result in results])
    print(f"Part 2: Sum of power is {sum_of_power}.")
