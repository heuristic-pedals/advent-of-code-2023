"""Advent of Code Day 10 Solution.

Source: https://adventofcode.com/2023/day/10

"""

from math import ceil

from advent_of_code_2023.utils import read_text_file

INPUT_FILEPATH = "data/day_10/input.txt"


def max_maze_distance(maze: list[str]) -> int:
    """Calculate the distance to the further point from the starting tile.

    Parameters
    ----------
    maze : list[str]
        input maze

    Returns
    -------
    int
        further distance from the starting location, in number of tiles.

    """
    # a maze symbol, entry point to next direction lookup
    maze_symbols_lup = {
        "|": {"t": "s", "b": "n"},
        "-": {"l": "e", "r": "w"},
        "L": {"t": "e", "r": "n"},
        "J": {"t": "w", "l": "n"},
        "7": {"l": "s", "b": "w"},
        "F": {"b": "e", "r": "s"},
    }

    # get starting config
    i, j = find_start(maze)
    direction = get_start_direction(maze, i, j)

    num_moves = 0
    while True:

        # increment the indecies and check if back at the start
        i, j = move_indecies(i, j, direction)
        num_moves += 1
        if maze[i][j] == "S":
            break

        # otherwise, translate direction to the next tile
        entry = get_tile_entry(direction)
        connector = maze[i][j]
        direction = maze_symbols_lup[connector][entry]

    return ceil(num_moves / 2)


def print_maze(maze: list[str]) -> None:
    """Display the maze - useful for debugging.

    Parameters
    ----------
    maze : list[str]
        maze input

    """
    for row in maze:
        print(row)


def find_start(maze: list[str]) -> tuple[int, int]:
    """Detect the starting location within the maze.

    Parameters
    ----------
    maze : list[str]
        input maze.

    Returns
    -------
    tuple[int, int]
        ith, jth indeces of the maze, corresponding to the start.

    """
    for i, maze_row in enumerate(maze):
        if "S" in maze_row:
            j = maze_row.index("S")
            break
    return i, j


def get_start_direction(maze: list[str], s_i: int, s_j: int) -> str:
    """Find a valid starting direction.

    Parameters
    ----------
    maze : list[str]
        inpt maze
    s_i : int
        ith starting row
    s_j : _type_
        jth starting column

    Returns
    -------
    str
        one of {"n", "e", "s", "w"} correspondiong to north, east, south and
        west respectively

    Raises
    ------
    Exception
        When unable to determine the next direction of travel

    """
    if maze[s_i][s_j - 1] in ["-", "L", "F"]:
        return "w"
    if maze[s_i + 1][s_j] in ["|", "J", "L"]:
        return "s"
    if maze[s_i][s_j + 1] in ["-", "7", "J"]:
        return "e"
    if maze[s_i - 1][s_j] in ["|", "7", "F"]:
        return "n"
    raise Exception("Unable to determine a starting direction.")


def move_indecies(i: int, j: int, direction: str) -> tuple[int, int]:
    """Increment indecies to the next tile depending on the direction.

    Parameters
    ----------
    i : int
        current ith row
    j : int
        current jth column
    direction : str
        direction to move in, must be one of {"n", "e", "s", "w"}.

    Returns
    -------
    tupe[int, int]
        the next tiles indeces; ith row and jth column.

    Raises
    ------
    ValueError
        When an invalid direction is provided.

    """
    if direction == "w":
        j -= 1
    elif direction == "s":
        i += 1
    elif direction == "e":
        j += 1
    elif direction == "n":
        i -= 1
    else:
        raise ValueError("Ubable to move indecies")

    return i, j


def get_tile_entry(direction: str) -> str:
    """Map directions of travel onto the next tiles entry direction.

    Parameters
    ----------
    direction : str
        direction of travel to next tile.

    Returns
    -------
    str
        one of {"t", "r", "b", "l"} which means the next tile will be entered
        from the top, right, bottom and left resprectively.

    Raises
    ------
    ValueError
        When an invalid direction is provided.

    """
    if direction == "w":
        return "r"
    elif direction == "s":
        return "t"
    elif direction == "e":
        return "l"
    elif direction == "n":
        return "b"
    else:
        raise ValueError("Unable to determine entry point")


if __name__ == "__main__":
    # prep input
    lines = read_text_file(INPUT_FILEPATH)

    # part 1 solution
    distance = max_maze_distance(lines)
    print(f"Part 1: Distance to travel from the start is {distance}")
