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


def process_neighbor(
    neighbor, current, matrix, traversed, steps=[], add_to_traverse=[]
):
    neighbor_y, neighbor_x = neighbor

    # if neighbor is out of bounds
    if (
        neighbor_x < 0
        or neighbor_x > len(matrix[0]) - 1
        or neighbor_y < 0
        or neighbor_y > len(matrix) - 1
    ):
        return steps, add_to_traverse

    curr_y, curr_x = current
    curr_ele = ELEVATION_MAP[matrix[curr_y][curr_x]]
    neighbor_ele = ELEVATION_MAP[matrix[neighbor_y][neighbor_x]]

    # if neighbor is higher than current, or current is 1 unit higher than
    # neighbor then we can assume that we can walk from neighbor to current
    # thus, we can get their stepped value
    if neighbor_ele >= curr_ele or neighbor_ele == curr_ele - 1:
        if (neighbor_y, neighbor_x) in traversed:
            steps.append(traversed[(neighbor_y, neighbor_x)])

    # if neighbor is same height or 1 unit higher than current
    if neighbor_ele == curr_ele or neighbor_ele == curr_ele + 1:
        if ((neighbor_y, neighbor_x) not in traversed) and (
            (neighbor_y, neighbor_x) not in add_to_traverse
        ):
            add_to_traverse.append((neighbor_y, neighbor_x))

    return steps, add_to_traverse


def get_neighbors(curr, matrix, traversed):
    steps = []
    add_to_traverse = []
    curr_y, curr_x = curr

    steps, add_to_traverse = process_neighbor(
        (curr_y, curr_x - 1), curr, matrix, traversed, steps, add_to_traverse
    )
    steps, add_to_traverse = process_neighbor(
        (curr_y, curr_x + 1), curr, matrix, traversed, steps, add_to_traverse
    )
    steps, add_to_traverse = process_neighbor(
        (curr_y - 1, curr_x), curr, matrix, traversed, steps, add_to_traverse
    )
    steps, add_to_traverse = process_neighbor(
        (curr_y + 1, curr_x), curr, matrix, traversed, steps, add_to_traverse
    )

    return steps, add_to_traverse


def build_paths(matrix, start, end):
    traversed = {}
    to_traverse = [start]

    # create early termination conditions
    # if end and its neighbors are in traversed
    end_y, end_x = end
    end_condition = [end]

    if end_x - 1 >= 0:
        end_condition.append((end_y, end_x - 1))
    if end_x + 1 <= len(matrix[0]) - 1:
        end_condition.append((end_y, end_x + 1))
    if end_y - 1 >= 0:
        end_condition.append((end_y - 1, end_x))
    if end_y + 1 <= len(matrix) - 1:
        end_condition.append((end_y + 1, end_x))

    while len(to_traverse) > 0:
        curr = to_traverse.pop(0)

        # process neighbors
        neighbor_steps, add_to_traverse = get_neighbors(
            curr,
            matrix,
            traversed,
        )

        # if current cell is the starting position, then step is 0
        if curr == start:
            traversed[curr] = 0
        else:
            traversed[curr] = min(neighbor_steps) + 1

        to_traverse += add_to_traverse

        # early termination
        if all(cell in traversed for cell in end_condition):
            return traversed

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
        optimized = build_paths(M, start, end)
        print(optimized[end])
    else:
        pass
