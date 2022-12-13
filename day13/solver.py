import json
from pathlib import Path


def compare(list1, list2, remaining1=[], remaining2=[]):
    try:
        first = list1.pop(0)
    except IndexError:
        first = None

    try:
        second = list2.pop(0)
    except IndexError:
        second = None

    if first is not None and second is None:
        return False

    if first is None and second is not None:
        return True

    if first is None and second is None:
        if len(remaining1) > 0 or len(remaining2) > 0:
            return compare(remaining1, remaining2)
        return True

    if isinstance(first, list) and isinstance(second, list):
        return compare(first, second, remaining1=list1, remaining2=list2)
    if isinstance(first, list) and isinstance(second, int):
        return compare(first, [second], remaining1=list1, remaining2=list2)
    if isinstance(first, int) and isinstance(second, list):
        return compare([first], second, remaining1=list1, remaining2=list2)

    if first > second:
        return False

    if first < second:
        return True

    return compare(list1, list2, remaining1=remaining1, remaining2=remaining2)


def get_sorted_indices(filepath):
    idx = 1
    packet_L = []
    packet_R = []
    ordered_idx = []

    with Path(filepath).open("r") as f:
        for i, line in enumerate(f, start=1):
            if i % 3 == 1:
                packet_L = json.loads(line.strip())
            elif i % 3 == 2:
                packet_R = json.loads(line.strip())
            else:
                # compare packets
                in_order = compare(packet_L, packet_R)

                if in_order:
                    ordered_idx.append(idx)

                idx += 1

        # compare last pair of packets
        in_order = compare(packet_L, packet_R)

        if in_order:
            ordered_idx.append(idx)

    return ordered_idx


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
        indices = get_sorted_indices(args.input_path)
        print(sum(indices))
    else:
        pass
