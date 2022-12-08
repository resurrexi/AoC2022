from pathlib import Path


def build_matrix(filepath):
    matrix = []

    with Path(filepath).open("r") as f:
        for line in f:
            values = line.strip()
            matrix.append(list(map(int, list(values))))

    return matrix


def count_visible_trees(matrix):
    count = 0
    dim_row, dim_col = len(matrix), len(matrix[0])

    for row_idx in range(dim_row):
        for col_idx in range(dim_col):
            if row_idx == 0 or col_idx == 0:
                count += 1
            else:
                current = matrix[row_idx][col_idx]
                left = matrix[row_idx][:col_idx]
                right = matrix[row_idx][col_idx + 1 :]
                top = [row[col_idx] for row in matrix[:row_idx]]
                bottom = [row[col_idx] for row in matrix[row_idx + 1 :]]

                if (
                    all(tree < current for tree in left)
                    or all(tree < current for tree in right)
                    or all(tree < current for tree in top)
                    or all(tree < current for tree in bottom)
                ):
                    count += 1

    return count


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

    treemap = build_matrix(args.input_path)

    if args.part == "1":
        print(count_visible_trees(treemap))
    else:
        print(get_highest_scenic_score(treemap))
