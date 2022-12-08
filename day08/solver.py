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


def get_distance(current, direction):
    for idx, tree in enumerate(direction, start=1):
        if tree >= current:
            return idx
    return len(direction)


def get_highest_scenic_score(matrix):
    highest = 0
    dim_row, dim_col = len(matrix), len(matrix[0])

    for row_idx in range(dim_row):
        for col_idx in range(dim_col):
            current = matrix[row_idx][col_idx]
            left = matrix[row_idx][:col_idx][::-1]
            right = matrix[row_idx][col_idx + 1 :]
            top = [row[col_idx] for row in matrix[:row_idx]][::-1]
            bottom = [row[col_idx] for row in matrix[row_idx + 1 :]]

            if left and right and top and bottom:
                left_distance = get_distance(current, left)
                right_distance = get_distance(current, right)
                top_distance = get_distance(current, top)
                bottom_distance = get_distance(current, bottom)

                score = (
                    left_distance
                    * right_distance
                    * top_distance
                    * bottom_distance
                )

                if score > highest:
                    highest = score

    return highest


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
