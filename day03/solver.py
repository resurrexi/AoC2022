from pathlib import Path

ITEM_TYPES = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
ITEM_PRIORITIES = dict(
    (x, y) for x, y in zip(ITEM_TYPES, range(1, len(ITEM_TYPES) + 2))
)


def sum_priorities(filepath):
    total = 0

    with Path(filepath).open("r") as f:
        for line in f:
            values = line.strip()
            midpoint = len(values) // 2

            half1 = set(values[:midpoint])
            half2 = set(values[midpoint:])
            intersection = list(half1.intersection(half2))[0]

            total += ITEM_PRIORITIES[intersection]

    return total


def sum_badge_priorities(filepath):
    total = 0
    common_badge = None

    with Path(filepath).open("r") as f:
        for idx, line in enumerate(f, start=1):
            values = line.strip()

            if idx % 3 == 1:
                common_badge = set(values)
            else:
                common_badge = common_badge.intersection(set(values))

            if idx % 3 == 0:
                common_badge = list(common_badge)[0]
                total += ITEM_PRIORITIES[common_badge]

    return total


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_path",
        help="Path to input file",
    )
    parser.add_argument(
        "part",
        choices=["1", "2"],
        help="Part 1 or 2",
    )
    args = parser.parse_args()

    if args.part == "1":
        print(sum_priorities(args.input_path))
    else:
        print(sum_badge_priorities(args.input_path))
