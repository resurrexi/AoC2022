from math import sqrt
from pathlib import Path


def update_position(lead, lag):
    distance = sqrt((lead["x"] - lag["x"]) ** 2 + (lead["y"] - lag["y"]) ** 2)

    if distance >= 2:
        if lag["x"] != lead["x"]:
            lag["x"] += 1 if lead["x"] > lag["x"] else -1
        if lag["y"] != lead["y"]:
            lag["y"] += 1 if lead["y"] > lag["y"] else -1

    return lag


def update_direction(knot, direction):
    if direction == "U":
        return {"x": knot["x"], "y": knot["y"] - 1}
    if direction == "D":
        return {"x": knot["x"], "y": knot["y"] + 1}
    if direction == "L":
        return {"x": knot["x"] - 1, "y": knot["y"]}
    return {"x": knot["x"] + 1, "y": knot["y"]}


def count_visited_positions(filepath, knot_size):
    visited = {(0, 0)}
    knots = [{"x": 0, "y": 0} for _ in range(knot_size)]

    with Path(filepath).open("r") as f:
        for line in f:
            values = line.strip()
            direction, times = values.split()

            for _ in range(int(times)):
                for i in range(knot_size):
                    if i == 0:
                        knots[i] = update_direction(knots[i], direction)
                    else:
                        knots[i] = update_position(knots[i - 1], knots[i])

                visited.add((knots[-1]["x"], knots[-1]["y"]))

    return len(visited)


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
        print(count_visited_positions(args.input_path, 2))
    else:
        print(count_visited_positions(args.input_path, 10))
