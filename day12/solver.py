from collections import OrderedDict
from pathlib import Path
from random import randint

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
    neighbor, current, matrix, traversed, steps=[], to_traverse=[]
):
    neighbor_y, neighbor_x = neighbor

    # if neighbor is out of bounds
    if (
        neighbor_x < 0
        or neighbor_x > len(matrix[0]) - 1
        or neighbor_y < 0
        or neighbor_y > len(matrix) - 1
    ):
        return steps, to_traverse

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
    if neighbor_ele <= curr_ele or neighbor_ele == curr_ele + 1:
        if (neighbor_y, neighbor_x) not in traversed:
            # this is to ensure we don't overload `to_traverse` with the
            # same neighbor to traverse. Max allowed is really 4 since
            # there are 4 directions that can converge to the neighbor
            if to_traverse.count((neighbor_y, neighbor_x)) < 4:
                to_traverse.append((neighbor_y, neighbor_x))

    return steps, to_traverse


def get_neighbors(curr, matrix, traversed, to_traverse):
    steps = []
    curr_y, curr_x = curr

    steps, to_traverse = process_neighbor(
        (curr_y, curr_x - 1), curr, matrix, traversed, steps, to_traverse
    )
    steps, to_traverse = process_neighbor(
        (curr_y, curr_x + 1), curr, matrix, traversed, steps, to_traverse
    )
    steps, to_traverse = process_neighbor(
        (curr_y - 1, curr_x), curr, matrix, traversed, steps, to_traverse
    )
    steps, to_traverse = process_neighbor(
        (curr_y + 1, curr_x), curr, matrix, traversed, steps, to_traverse
    )

    return steps, to_traverse


def build_paths(matrix, start, end, visual=True):
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

    idx = 0
    while len(to_traverse) > 0:
        curr = to_traverse.pop(0)

        # process neighbors
        neighbor_steps, to_traverse = get_neighbors(
            curr,
            matrix,
            traversed,
            to_traverse,
        )

        # if current cell is the starting position, then step is 0
        if curr == start:
            traversed[curr] = 0
        else:
            traversed[curr] = min(neighbor_steps) + 1

        # diagnostics
        if visual:
            print(f"{idx=}")
            printed = ""
            for row in range(len(matrix)):
                for col in range(len(matrix[0])):
                    if (row, col) == start:
                        printed += "S"
                    elif (row, col) == end:
                        printed += "E"
                    elif (row, col) in traversed:
                        printed += "@"
                    elif (row, col) in to_traverse:
                        printed += "X"
                    else:
                        printed += "-"
                printed += "\n"
            print(printed)
            idx += 1

        # early termination
        if all(cell in traversed for cell in end_condition):
            return traversed

    return traversed


def find_shortest_path(matrix, end):
    a_cells = []
    path_lengths = []

    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[row][col] == "a":
                a_cells.append((row, col))

    for cell in a_cells:
        try:
            path_lengths.append(
                build_paths(matrix, cell, end, visual=False)[end]
            )
        except KeyError:
            pass

    return min(path_lengths)


def is_neighbor(curr, candidate):
    curr_y, curr_x = curr
    cand_y, cand_x = candidate

    if curr_y == cand_y and curr_x - 1 == cand_x:
        return True
    if curr_y == cand_y and curr_x + 1 == cand_x:
        return True
    if curr_y - 1 == cand_y and curr_x == cand_x:
        return True
    if curr_y + 1 == cand_y and curr_x == cand_x:
        return True

    return False


def get_direction(start, end):
    start_y, start_x = start
    end_y, end_x = end

    if start_y < end_y:
        return "v"
    if start_y > end_y:
        return "^"
    if start_x < end_x:
        return ">"
    return "<"


def get_random_optimized_path(optimized, start, end):
    optimized_copy = optimized.copy()
    path = OrderedDict()
    path[start] = "S"  # add starting point to path

    idx = 1
    while idx <= optimized_copy[end]:
        cells = [k for k, v in optimized_copy.items() if v == idx]

        # filter out cells that are neighbors of last cell in path
        neighbors = [k for k in cells if is_neighbor(k, list(path.keys())[-1])]

        if (len(neighbors) == 0) or (
            idx == optimized_copy[end] and end not in neighbors
        ):
            # last cell in path is a dead end or isn't endpoint; delete
            last_path_node = list(path.keys())[-1]
            del optimized_copy[last_path_node]
            del path[last_path_node]
            # backtrack and redo
            idx -= 1
            continue

        if idx == optimized_copy[end]:
            path[end] = "E"
        else:
            # select a random neighbor and attach to path
            choice = randint(0, len(neighbors) - 1)
            path[neighbors[choice]] = get_direction(
                list(path.keys())[-1], neighbors[choice]
            )

        idx += 1

    return path


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
        optimized = build_paths(M, start, end, visual=False)
        print(optimized[end])

        shortest = get_random_optimized_path(optimized, start, end)

        printed = ""
        for row in range(len(M)):
            for col in range(len(M[0])):
                if (row, col) in shortest:
                    printed += shortest[(row, col)]
                else:
                    printed += "-"
            printed += "\n"
        print(printed)
    else:
        print(find_shortest_path(M, end))
