from pathlib import Path

BLOCKS = [
    [
        "####",
    ],
    [
        " # ",
        "###",
        " # ",
    ],
    [
        "  #",
        "  #",
        "###",
    ],
    [
        "#",
        "#",
        "#",
        "#",
    ],
    [
        "##",
        "##",
    ],
]


def get_controls(filepath):
    controls = Path(filepath).read_text().strip()

    return controls


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

    controls = get_controls(args.input_path)

    if args.part == "1":
        print(controls)
    else:
        pass
