from pathlib import Path


def get_bounds(matrix):
    max_row = max(k[0] for k in matrix.keys())
    min_col = min(k[1] for k in matrix.keys())
    max_col = max(k[1] for k in matrix.keys())

    return 0, max_row, min_col, max_col


def map_cave(filepath):
    rocks = {}

    with Path(filepath).open("r") as f:
        for line in f:
            values = line.strip()
            coords = values.split(" -> ")

            prev_x, prev_y = 0, 0
            for idx, coord in enumerate(coords):
                x, y = map(int, coord.split(","))

                if idx == 0:
                    prev_x, prev_y = x, y
                else:
                    for row in range(min(prev_y, y), max(prev_y, y) + 1):
                        for col in range(min(prev_x, x), max(prev_x, x) + 1):
                            rocks[(row, col)] = "#"

                # update prev
                prev_x, prev_y = x, y

    return rocks


def drizzle(pos, cave, cave_bounds):
    pos_y, pos_x = pos
    _, max_y, min_x, max_x = cave_bounds

    if (pos_y + 1, pos_x) not in cave and pos_y + 1 <= max_y + 1:
        return drizzle((pos_y + 1, pos_x), cave, cave_bounds)
    if (
        (pos_y + 1, pos_x - 1) not in cave
        and pos_y + 1 <= max_y + 1
        and pos_x - 1 >= min_x - 1
    ):
        return drizzle((pos_y + 1, pos_x - 1), cave, cave_bounds)
    if (
        (pos_y + 1, pos_x + 1) not in cave
        and pos_y + 1 <= max_y + 1
        and pos_x + 1 <= max_x + 1
    ):
        return drizzle((pos_y + 1, pos_x + 1), cave, cave_bounds)

    # no more place to fall to
    return pos_y, pos_x


def get_max_sand(cave, visual=True):
    _, max_y, min_x, max_x = cave_bounds = get_bounds(cave)
    sand_y, sand_x = source = (0, 500)
    cave_copy = cave.copy()

    idx = 1
    while True:
        sand_y, sand_x = drizzle(source, cave_copy, cave_bounds)

        if sand_y > max_y or sand_x < min_x or sand_x > max_x:
            # reached abyss
            break
        else:
            cave_copy[(sand_y, sand_x)] = "o"

        # diagnostics
        if visual:
            print(idx)
            printed = ""
            for row in range(max_y + 1):
                for col in range(min_x, max_x + 1):
                    if (row, col) in cave_copy:
                        printed += cave_copy[(row, col)]
                    else:
                        printed += "."
                printed += "\n"
            print(printed)

        idx += 1

    return idx - 1  # don't count the sand that falls to abyss


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
        print(get_max_sand(cave))
    else:
        pass
