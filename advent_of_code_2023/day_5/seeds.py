"""Advent of code solution day 5.

Source: https://adventofcode.com/2023/day/5

"""

import re

from advent_of_code_2023.utils import read_text_file

INPUT_FILE = "data/day_5/input.txt"


def get_seed_location_lookup(lines: list[str]) -> dict:
    """Build a seed to location lookup.

    Constructs a lookup by parsing the input almanac. Parses the first line to
    find the seed numbers. Constructs maps defining the minimum and maximum
    limits of map sources and destinations. These are used to check and
    translate values through sequential layers of maps. If the value does not
    lie within any of the limits then the previous value is passed through that
    map 'layer' to the next. Outputs a soil to location map, based on order of
    occurance in the almanac spec. See the advent of code source for more
    details.

    Parameters
    ----------
    lines : list[str]
        input almanac lines

    Returns
    -------
    dict
        a seed (keys) to location (values) lookup.

    """
    # knife and fork seed numbers out of first line
    seeds = get_seeds(lines[0])

    # record all the maps to build (also used to search for map in lines)
    # instanstiate a maps and lookup dictionary
    map_names = [
        "seed-to-soil map:",
        "soil-to-fertilizer map:",
        "fertilizer-to-water map:",
        "water-to-light map:",
        "light-to-temperature map:",
        "temperature-to-humidity map:",
        "humidity-to-location map:",
    ]
    maps = {}
    seed_location_lookup = {}

    # build the map for each map defined in the input
    for map_name in map_names:
        maps[map_name] = build_map(lines, map_name)

    for seed in seeds:
        # start by setting previous value to the seed number
        previous = seed
        for map_name, map_limits_list in maps.items():
            # default current to none to know when a map has worked. When going
            # over all the maps, if it's between the source limits then update
            # current with a new value that's equi-distance from the dest min
            # use break to speed up loop after current has been updated
            current = None
            for map_limits in map_limits_list:
                if (previous >= map_limits[0]) & (previous <= map_limits[1]):
                    current = map_limits[2] + (previous - map_limits[0])
                    break

            # handle case if current wasn't set (pass through the result)
            if current is None:
                current = previous
            previous = current

        # update the lookup with the last value
        seed_location_lookup[seed] = previous

    return seed_location_lookup


def get_seeds(seeds_line: str) -> list[int]:
    """Get seed numbers (helper function).

    Parameters
    ----------
    seeds_line : str
        line containing seed numbers

    Returns
    -------
    list[int]
        list of seed numbers

    """
    return [int(num.group()) for num in re.finditer("[0-9]+", seeds_line)]


def build_map(lines: list[str], map_name: str) -> list[tuple[int, int, int]]:
    """Build a map 'layer' by parsing almanac lines.

    Initially detects the map name in the almanac. From this point onwards, it
    parses each line noting all the source, destination and range values. Each
    value is translated into a set of limits (min_source, max_source,
    min_destination) such that they can be used to translate values through a
    sequence of maps (without storing a whole lookup, which would be slow to
    use and memory intensive). Note: max_destination is not needed, since the
    'distance' from the min_source value is all that's needed during
    translation. Parsing stops once a blank line or EOF is reached.

    Parameters
    ----------
    lines : list[str]
        input almanac
    map_name : str
        name of map to build (within almanac)

    Returns
    -------
    list[tuple[int, int, int]]
        list of translation limits, in order min_source, max_source,
        min_destionation.

    Raises
    ------
    ValueError
        When parsing the source, destination and range value fails.

    """
    # get EOF index and get index of first valid line in map
    maps = []
    max_idx = len(lines)
    try:
        idx = lines.index(map_name) + 1
    except ValueError:
        raise ValueError(f"Unable to find {map_name} in almanac.")

    while True:
        # break when an empty line is reach
        if lines[idx] == "":
            break

        # knife and fork source, destination, and range (asserting length)
        limits = [
            int(limit.group()) for limit in re.finditer("[0-9]+", lines[idx])
        ]
        if len(limits) != 3:
            raise ValueError(
                "Unable to parse limits into 3 variables when building "
                f"{map_name} and lines index {idx}"
            )
        # translate values to limits and add to maps
        maps.append(
            (
                limits[1],
                limits[1] + limits[2] - 1,
                limits[0],
            )
        )

        # increment and break if EOF is next
        idx += 1
        if idx == max_idx:
            break

    return maps


if __name__ == "__main__":
    # prep input
    lines = read_text_file(INPUT_FILE)

    # part 1 solution
    seed_location_lup = get_seed_location_lookup(lines)
    min_location = min(seed_location_lup.values())
    print(f"Part 1: Minimum location is {min_location}")
