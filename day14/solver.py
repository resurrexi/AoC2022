from pathlib import Path


def get_bounds(matrix):
    min_row = min(k[0] for k in matrix.keys())
    max_row = max(k[0] for k in matrix.keys())
    min_col = min(k[1] for k in matrix.keys())
    max_col = max(k[1] for k in matrix.keys())

    return min_row, max_row, min_col, max_col


def map_cave(filepath):
    matrix = {}

    with Path(filepath).open("r") as f:
        for i, line in enumerate(f):
            values = line.strip()
            coords = values.split(" -> ")

            prev_x, prev_y = 0, 0
            for i_c, coord in enumerate(coords):
                x, y = map(int, coord.split(","))

                if i_c == 0:
                    prev_x, prev_y = x, y
                else:
                    for row in range(min(prev_y, y), max(prev_y, y) + 1):
                        for col in range(min(prev_x, x), max(prev_x, y) + 1):
                            matrix[(row, col)] = "#"

    return matrix


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

    cave = map_cave(args.input_path)

    if args.part == "1":
        print(get_bounds(cave))
    else:
        pass
