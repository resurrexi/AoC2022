from pathlib import Path


def get_packed_quantities(filepath):
    packers = []
    elf_idx = 0
    elf_sum = 0

    with Path(filepath).open("r") as f:
        for line in f:
            value = line.strip()
            if value:
                elf_sum += int(value)
            else:
                packers.append((elf_idx, elf_sum))
                elf_idx += 1  # increment to next elf
                elf_sum = 0  # reset

    return packers


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_path",
        help="Path to input file",
    )
    args = parser.parse_args()

    packers = get_packed_quantities(args.input_path)

    # sort by descending
    print(sorted(packers, key=lambda x: x[1], reverse=True))
