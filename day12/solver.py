from pathlib import Path

ELEVATION_MAP = dict(
    zip("abcdefghijklmnopqrstuvwxyzSE", list(range(26)) + [0, 25])
)


def build_matrix(filepath):
    matrix = []
    start = None
    end = None

    with Path(filepath).open("r") as f:
        for idx, line in enumerate(f):
            values = list(line.strip())

            if "S" in values:
                start = (idx, values.index("S"))
            if "E" in values:
                end = (idx, values.index("E"))

            matrix.append(values)

    return matrix, start, end


def process_cell(y, x, matrix, compare, traversed, to_traverse, min_step):
    cell = matrix[y][x]

    if (ELEVATION_MAP[cell] == compare) or (ELEVATION_MAP[cell] == compare - 1):
        if (y, x) in traversed.keys():
            min_step = min(traversed[(y, x)], min_step)
    if (ELEVATION_MAP[cell] == compare) or (ELEVATION_MAP[cell] == compare + 1):
        if (y, x) not in traversed.keys():
            to_traverse.append((y, x))

    return min_step, to_traverse


def build_paths(matrix, cursor):
    y, x = cursor
    traversed = {}
    to_traverse = [cursor]

    while len(to_traverse) > 0:
        elevation = ELEVATION_MAP[matrix[y][x]]

        # find adjacent paths to determine next minimum step
        min_step = -1 if matrix[y][x] == "S" else 9999

        if x - 1 >= 0:
            min_step, to_traverse = process_cell(
                y, x - 1, matrix, elevation, traversed, to_traverse, min_step
            )
        if x + 1 <= len(matrix[0]) - 1:
            min_step, to_traverse = process_cell(
                y, x + 1, matrix, elevation, traversed, to_traverse, min_step
            )
        if y - 1 >= 0:
            min_step, to_traverse = process_cell(
                y - 1, x, matrix, elevation, traversed, to_traverse, min_step
            )
        if y + 1 <= len(matrix) - 1:
            min_step, to_traverse = process_cell(
                y + 1, x, matrix, elevation, traversed, to_traverse, min_step
            )

        traversed[(y, x)] = min_step + 1

        y, x = to_traverse.pop(0)

    return traversed


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

    M, start, end = build_matrix(args.input_path)

    if args.part == "1":
        optimized = build_paths(M, start)
        print(optimized[end])
    else:
        pass
