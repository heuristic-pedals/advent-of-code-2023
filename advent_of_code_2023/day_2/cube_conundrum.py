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


def parse_game(game: str) -> Tuple[int, bool]:
    """Parse a game a determine plausability.

    Retrieves the game's id and determines its plausability considering ball
    counts by color across game sets. Plausability is defined by sets that
    have ball counts for all colors below (or equal to) the treshold for the
    color. If any count if above this theshold the whole game is deemed
    infeasible.

    Parameters
    ----------
    game : str
        Input game string (line from input file).

    Returns
    -------
    Tuple[int, bool]
        Game outcome. First element is the game id. The second element is the
        outcome - game is possible when this is True.

    """
    # find and extract the game id
    game_id_match = re.findall("Game [0-9]*:", game)[0]
    game_id = int(re.sub("[^0-9]", "", game_id_match))

    # take the game id section out of the string (not needed anymore) and
    # split into game sets at semi colons
    game_sets = game.replace(game_id_match, "").split(";")

    # collect possible ball colors
    colors = BALL_LIMITS.keys()

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
            return game_id, False

    return game_id, True


if __name__ == "__main__":
    # part 1 solution
    lines = read_text_file(INPUT_PATH)
    results = [parse_game(line) for line in lines]
    possible_games_id_sum = sum([result[0] for result in results if result[1]])
    print(f"Part 1: Sum of possible game ids is {possible_games_id_sum}.")
