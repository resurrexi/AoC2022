from pathlib import Path


def get_all_overlap(filepath):
    total = 0

    with Path(filepath).open("r") as f:
        for line in f:
            values = line.strip()
            first, second = values.split(",")

            lower1, upper1 = map(int, first.split("-"))
            lower2, upper2 = map(int, second.split("-"))

            min_value = min(lower1, lower2)
            max_value = max(upper1, upper2)

            if (min_value == lower1 and max_value == upper1) or (
                min_value == lower2 and max_value == upper2
            ):
                total += 1

    return total


def get_any_overlap(filepath):
    total = 0

    with Path(filepath).open("r") as f:
        for line in f:
            values = line.strip()
            first, second = values.split(",")

            lower1, upper1 = map(int, first.split("-"))
            lower2, upper2 = map(int, second.split("-"))

            if lower1 >= lower2 and lower1 <= upper2:
                total += 1
            elif upper1 >= lower2 and upper1 <= upper2:
                total += 1
            elif lower2 >= lower1 and lower2 <= upper1:
                total += 1
            elif upper2 >= lower1 and upper2 <= upper1:
                total += 1

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
        print(get_all_overlap(args.input_path))
    else:
        print(get_any_overlap(args.input_path))
