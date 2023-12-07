"""Advent of Code Day 7 Solution.

Source: https://adventofcode.com/2023/day/7

"""

from collections import defaultdict, Counter

from advent_of_code_2023.utils import read_text_file


INPUT_DATA = "data/day_7/input.txt"


def sum_ranked_bids(lines: list[str], joker: bool = False) -> int:
    """Calculat the sum of ranked bids.

    Parses out each hand and bid, and determines the rank of hand. Hands of
    the same rank are then sorted based on a highest card wins decision from
    first to last card. Then each hand's rank is multiplied by it's bid, then
    all summed together.

    Can also treat "J" as 'jokers' instead of 'jacks' using `jocker`. In the
    joker format of the game, these are the least value card & can take the
    form of any other card that gives the best possible hand.

    Parameters
    ----------
    lines : list[str]
        input hands/bid strings. expected in CCCCC <BID> format (space sep),
        where CCCCC are the cards of the hand, and <BID> is the bid value.
    joker : bool, optional
        treat "J" as a joker instead of a jack.

    Returns
    -------
    int
        Sum total of all hand's bids multiplied by their rank.

    """
    # create a hands/bids map, and a dict to store all hands with the same rank
    hands_to_bids = {}
    hand_ranks = {
        0: [],
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
    }
    for line in lines:
        # seperate the hand from the bid, update hands/bid map, get the rank of
        # the hand and add to the respective list in hand_ranks dict.
        hand, bid = line.split(" ")
        hands_to_bids[hand] = int(bid)
        hand_rank = get_hand_rank(hand, joker=joker)
        hand_ranks[hand_rank].append(hand)

    ranked_hands = []
    for hand_rank, equal_hands in hand_ranks.items():
        if equal_hands != []:
            # sort hands with an equal ranking, and add to ranked hands
            sorted_equal_hands = sort_hands(equal_hands, joker=joker)
            for hand in sorted_equal_hands:
                ranked_hands.append(hand)

    # get sum total off the sorted hands multiplied by their bids. Rank goes
    # from highest down to 1 (depending on the number of rows)
    total = 0
    for rank, hand in zip(range(len(lines), 0, -1), ranked_hands):
        total += rank * hands_to_bids[hand]

    return total


def get_hand_rank(cards: str, joker: bool = False) -> int:
    """Get the hand's rank.

    Returns zero-index rank based on hand type. "Five of a kind" = 0, down to
    'High card' = 6.

    Parameters
    ----------
    cards : str
        all the cards in the hand
    joker : bool, optional
        treat "J" as a joker instead of a jack.

    Returns
    -------
    int
        the rank of the hand.

    """
    # handle jocker cases upfront. The premise here is that the best hand will
    # always be given when any "J" take the value of the most common card that
    # isn't already a "J" (hence the replace inside the counter). Other case to
    # handle is all "J"s - so set it to the best possible hand of all.
    if joker & (cards == "JJJJJ"):
        cards = "AAAAA"
    elif joker & ("J" in cards):
        cards = cards.replace(
            "J", Counter(cards.replace("J", "")).most_common()[0][0]
        )

    # count card occurances and convert to list
    d = defaultdict(int)
    for card in cards:
        d[card] += 1
    card_counts = list(d.values())

    # determine card rank based on rules for each hand type
    if 5 in card_counts:  # five of a kind
        return 0
    elif 4 in card_counts:  # four of a kind
        return 1
    elif (3 in card_counts) & (2 in card_counts):  # full house
        return 2
    elif 3 in card_counts:  # three of a kind
        return 3
    elif Counter(card_counts)[2] == 2:  # two pair
        return 4
    elif 2 in card_counts:  # one pair
        return 5
    else:  # high card
        return 6


def sort_hands(hands: list[str], joker: bool = False) -> list[str]:
    """Sort the hands of equal rank in order.

    Highest card from first to last is used to resolve the equal ranked sort.

    Parameters
    ----------
    hands : list[str]
        list of equally ranked hands to sort
    joker : bool, optional
        treat "J" as a joker instead of a jack.

    Returns
    -------
    ranking : list[str]
        equally ranked hands sorted

    """
    # map each hand of cards onto letter (to allow alphabetical sorting only)
    hand_maps = {}
    for hand in hands:
        hand_maps[hand] = map_hand(hand, joker=joker)

    # sort by the alphabetical representation and get back the original hand
    sorted_hands = sorted(hand_maps.items(), key=lambda x: x[1])
    ranking = []
    for hand, _ in sorted_hands:
        ranking.append(hand)

    return ranking


def map_hand(hand: str, joker: bool = False) -> str:
    """Map cards in a hand into alphabetical characters only.

    Parameters
    ----------
    hand : str
        hand to map
    joker : bool, optional
        treat "J" as a joker instead of a jack.

    Returns
    -------
    str
        cards in the hand mapped to alphabetical characters only.

    """
    # card to letter lookup - ommit ACE since this is already A
    card_to_letter = {
        "K": "B",
        "Q": "C",
        "T": "E",
        "9": "F",
        "8": "G",
        "7": "H",
        "6": "I",
        "5": "L",
        "4": "M",
        "3": "N",
        "2": "O",
    }

    # conditionally rank "J" as between Q and T if Jack, or last if Joker
    if joker:
        card_to_letter["J"] = "P"
    else:
        card_to_letter["J"] = "D"

    # replace based on mapped values
    for k, v in card_to_letter.items():
        if k in hand:
            hand = hand.replace(k, v)

    return hand


if __name__ == "__main__":
    # prep inputs
    lines = read_text_file(INPUT_DATA)

    # part 1 solution
    total = sum_ranked_bids(lines)
    print(
        "Part 1: sum total of all bids multiplied by their ranks where J is a "
        f"jack: {total}"
    )

    # part 2 solution
    total = sum_ranked_bids(lines, joker=True)
    print(
        "Part 2: sum total of all bids multiplied by their ranks where J is a "
        f"joker: {total}"
    )
