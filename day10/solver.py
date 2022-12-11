from pathlib import Path


def sum_signal_strengths(filepath, cycles):
    summed = 0
    register = 1
    cycle = 0

    with Path(filepath).open("r") as f:
        for line in f:
            values = line.strip()

            cycle += 1

            if cycle in cycles:
                summed += register * cycle

            if values.startswith("addx"):
                cycle += 1

                if cycle in cycles:
                    summed += register * cycle

                register += int(values.split()[1])

    return summed


def draw_signal(filepath):
    # because drawing starts at position 1 instead of 0,
    # set sprite midpoint to 2
    sprite_midpoint = 2
    cycle = 0
    signal = ""

    with Path(filepath).open("r") as f:
        for line in f:
            values = line.strip()

            cycle += 1
            signal += (
                "#"
                if max(sprite_midpoint - 1, 1) <= cycle % 40
                and min(sprite_midpoint + 1, 40) >= cycle % 40
                else "."
            )

            if cycle % 40 == 0:
                signal += "\n"

            if values.startswith("addx"):
                cycle += 1
                signal += (
                    "#"
                    if max(sprite_midpoint - 1, 1) <= cycle % 40
                    and min(sprite_midpoint + 1, 40) >= cycle % 40
                    else "."
                )

                if cycle % 40 == 0:
                    signal += "\n"

                sprite_midpoint += int(values.split()[1])

    return signal


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
        print(
            sum_signal_strengths(args.input_path, [20, 60, 100, 140, 180, 220])
        )
    else:
        print(draw_signal(args.input_path))
