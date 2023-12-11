"""Advent of Code Day 11 Solution.

Source: https://adventofcode.com/2023/day/11

"""
import itertools
import re

from advent_of_code_2023.utils import read_text_file

INPUT_FILEPATH = "data/day_11/input.txt"


def total_galaxy_distances_fill_expansions(image: list[str]) -> int:
    """Get total distances between all galaxy combinations."""
    expanded_image = expand_universe(image)
    galaxy_dict = find_galaxies(expanded_image)

    total = 0
    for id_1, id_2 in itertools.combinations(galaxy_dict.keys(), 2):
        total += manhattan_distance(galaxy_dict[id_1], galaxy_dict[id_2])

    return total


def total_galaxy_distances_calculated_expansions(
    image: list[str], expansion_factor: int = 2
) -> int:
    """Calculate the total galaxy distances considering an expansion factor.

    Calculates the sum total of all distances between every combination of
    galaxy. The manhattan distance is used to calculate the distances between
    pairs of galaxies. The method use does not rely on 'filling spaces', but
    instead calculates the expansion dynamically, making it more suited for
    'gaps' in space (where no galaxy lies in an image row or column).

    Parameters
    ----------
    image : list[str]
        input image, where # denotes a galaxy's location
    expansion_factor : int, optional
        how much to expand 'gaps' by, by default 2 (spaces doubled in size).

    Returns
    -------
    int
        sum total of all distances across all galaxy combinations.

    Raises
    ------
    ValueError
        When `expansion_factor` is less than 2 (to ensure an expansion).
    TypeError
        When `expansion_factor` is not an integer.

    """
    # handle invalid cases of expansion factor - minimum is to double the space
    if expansion_factor < 2:
        raise ValueError("Expansion factor must be greater than 2.")

    # Ensure expansion factor is an integer to ensure whole number of spaces
    if not isinstance(expansion_factor, int):
        raise TypeError(
            f"`expansion factor must be an int, got {type(expansion_factor)}"
        )

    # subtract one to calculate how many 'spaces' to add
    expansion_factor -= 1

    # get the galaxy locations and determine rows + cols to expand
    unexpanded_galaxy_dict = find_galaxies(image)
    expansion_rows, expansion_cols = expansion_points(image)

    # add the number of required expansions to the x and y coordinates. This is
    # set by 'how many expansions occur before the galaxies row/col index'.
    expanded_galaxy_dict = {}
    for id, (x, y) in unexpanded_galaxy_dict.items():
        x_expansion = sum(x > i for i in expansion_rows) * expansion_factor
        y_expansion = sum(y > j for j in expansion_cols) * expansion_factor
        expanded_galaxy_dict[id] = (x + x_expansion, y + y_expansion)

    # calculate the total of all manhattan distances between all combinations
    total = 0
    for id_1, id_2 in itertools.combinations(expanded_galaxy_dict.keys(), 2):
        total += manhattan_distance(
            expanded_galaxy_dict[id_1], expanded_galaxy_dict[id_2]
        )

    return total


def display_image(image: list[str]) -> None:
    """Display an imgage to help visualisation."""
    for line in image:
        print(line)


def expand_universe(input_image: list[str]) -> list[str]:
    """Expand the universe when no galaxies are present."""
    temp_image = []
    galaxy_cols = set()
    all_cols = set(range(0, len(input_image[0])))
    for row in input_image:
        temp_image.append(row)
        if "#" not in row:
            temp_image.append(row)

        galaxy_positions = [x.start() for x in re.finditer(r"#", row)]
        for position in galaxy_positions:
            galaxy_cols.add(position)

    empty_columns = sorted(all_cols.difference(galaxy_cols), reverse=True)

    output_image = []
    for row in temp_image:
        expanded_row = row
        for col in empty_columns:
            expanded_row = expanded_row[:col] + "." + expanded_row[col:]
        output_image.append(expanded_row)

    return output_image


def find_galaxies(image: list[str]) -> dict:
    """Find galaxies and create a lookup."""
    galaxy_cordinates = []
    for i, row in enumerate(image):
        galaxy_cols = [x.start() for x in re.finditer(r"#", row)]
        for galaxy_col in galaxy_cols:
            galaxy_cordinates.append((i, galaxy_col))

    galaxy_lup = {
        id: coords
        for id, coords in zip(
            range(0, len(galaxy_cordinates)), galaxy_cordinates
        )
    }

    return galaxy_lup


def manhattan_distance(a, b):
    """Calculate manhattan distance."""
    return sum(abs(val1 - val2) for val1, val2 in zip(a, b))


def expansion_points(input_image):
    """Get expansion points."""
    galaxy_cols = set()
    all_cols = set(range(0, len(input_image[0])))
    expansion_rows = []
    for i, row in enumerate(input_image):
        if "#" not in row:
            expansion_rows.append(i)

        galaxy_positions = [x.start() for x in re.finditer(r"#", row)]
        for position in galaxy_positions:
            galaxy_cols.add(position)

    expansion_cols = sorted(all_cols.difference(galaxy_cols))

    return expansion_rows, expansion_cols


if __name__ == "__main__":
    # prep input
    lines = read_text_file(INPUT_FILEPATH)

    # part 1 solution
    output = total_galaxy_distances_fill_expansions(lines)
    assert (output == 9681886) | (output == 374)
    print(f"Part 1: Sum of galaxy distance {output}")

    # part 2 solution
    expansion_factor = 1000000
    output = total_galaxy_distances_calculated_expansions(
        lines, expansion_factor=expansion_factor
    )
    assert output == 791134099634
    print(
        "Part 2: Sum of galaxy distances with an expansion factor of "
        f"{expansion_factor:,} is {output}"
    )
