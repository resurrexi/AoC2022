from pathlib import Path


def find_packet_start(filepath):
    signal = Path(filepath).read_text()

    start = 0

    while True:
        potential_packet = signal[start : start + 4]

        if len(potential_packet) == len(set(potential_packet)):
            return start + 4

        start += 1


def find_message_start(filepath):
    signal = Path(filepath).read_text()

    start = 0

    while True:
        potential_message = signal[start : start + 14]

        if len(potential_message) == len(set(potential_message)):
            return start + 14

        start += 1


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
        print(find_packet_start(args.input_path))
    else:
        print(find_message_start(args.input_path))
