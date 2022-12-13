import json
from pathlib import Path


def compare(list1, list2, idx=0, remaining1=[], remaining2=[]):
    try:
        first = list1[idx]
    except IndexError:
        first = None

    try:
        second = list2[idx]
    except IndexError:
        second = None

    # if list in any is exhausted
    if first is not None and second is None:
        return 1
    if first is None and second is not None:
        return -1
    if first is None and second is None:
        if len(remaining1) > 0 or len(remaining2) > 0:
            return compare(remaining1, remaining2)
        return 0

    if isinstance(first, list) and isinstance(second, list):
        return compare(
            first,
            second,
            remaining1=remaining1 + list1[idx + 1 :],
            remaining2=remaining2 + list2[idx + 1 :],
        )
    if isinstance(first, list) and isinstance(second, int):
        return compare(
            first,
            [second],
            remaining1=remaining1 + list1[idx + 1 :],
            remaining2=remaining2 + list2[idx + 1 :],
        )
    if isinstance(first, int) and isinstance(second, list):
        return compare(
            [first],
            second,
            remaining1=remaining1 + list1[idx + 1 :],
            remaining2=remaining2 + list2[idx + 1 :],
        )

    # if first and second are ints
    if first > second:
        return 1

    if first < second:
        return -1

    return compare(
        list1, list2, idx=idx + 1, remaining1=remaining1, remaining2=remaining2
    )


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
                in_order = compare(packet_L, packet_R) <= 0

                if in_order:
                    ordered_idx.append(idx)

                idx += 1

        # compare last pair of packets
        in_order = compare(packet_L, packet_R) <= 0

        if in_order:
            ordered_idx.append(idx)

    return ordered_idx


def sort_arr(array):
    for i in range(1, len(array)):
        key_item = array[i]

        j = i - 1

        while j >= 0 and compare(array[j], key_item) > 0:
            array[j + 1] = array[j]
            j -= 1

        array[j + 1] = key_item

    return array


def get_decoder_key(filepath):
    packets = []

    with Path(filepath).open("r") as f:
        for i, line in enumerate(f, start=1):
            if i % 3 == 0:
                continue

            value = json.loads(line.strip())
            packets.append(value)

    packets.append([[2]])
    packets.append([[6]])

    packets = sort_arr(packets)

    return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)


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
        print(get_decoder_key(args.input_path))
