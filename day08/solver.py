from pathlib import Path


def build_matrix(filepath):
    matrix = []

    with Path(filepath).open("r") as f:
        for line in f:
            values = line.strip()
            matrix.append(list(map(int, list(values))))

    return matrix


def count_visible_trees(matrix):
    positions = set()

    # left and right
    for idx, row in enumerate(matrix):
        # from left
        highest = 0
        for col_idx, tree in enumerate(row):
            if idx == 0 or idx == len(matrix) - 1:
                positions.add(f"{idx}-{col_idx}")
            elif col_idx == 0:
                highest = tree
            elif tree > highest:
                positions.add(f"{idx}-{col_idx}")
                highest = tree

        # from right
        reversed = row[::-1]
        highest = 0
        for col_idx, tree in enumerate(reversed):
            if col_idx == 0:
                highest = tree
            elif tree > highest:
                positions.add(f"{idx}-{len(reversed) - 1 - col_idx}")
                highest = tree

    # top and bottom
    transposed = list(zip(*matrix))
    for idx, col in enumerate(transposed):
        # from top
        highest = 0
        for row_idx, tree in enumerate(col):
            if idx == 0 or idx == len(transposed) - 1:
                positions.add(f"{row_idx}-{idx}")
            elif row_idx == 0:
                highest = tree
            elif tree > highest:
                positions.add(f"{row_idx}-{idx}")
                highest = tree

        # from bottom
        reversed = col[::-1]
        highest = 0
        for row_idx, tree in enumerate(reversed):
            if row_idx == 0:
                highest = tree
            elif tree > highest:
                positions.add(f"{len(reversed) - 1 - row_idx}-{idx}")
                highest = tree

    return len(positions)

def get_highest_scenic_score(matrix):
    score = 0
    transposed = list(zip(*matrix))

    for row_idx in range(len(matrix)):
        for col_idx in range(len(matrix[0])):
            pass
    return 0


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

    matrix = build_matrix(args.input_path)

    if args.part == "1":
        print(count_visible_trees(matrix))
    else:
        print(get_highest_scenic_score(matrix))
