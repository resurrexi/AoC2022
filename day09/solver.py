from pathlib import Path


def update_position(lead, lag):
    lead_x, lead_y = lead
    lag_x, lag_y = lag

    if lag_x - lead_x > 1:
        lag_x -= 1
        lag_y -= lag_y - lead_y
    elif lead_x - lag_x > 1:
        lag_x += 1
        lag_y -= lag_y - lead_y
    elif lag_y - lead_y > 1:
        lag_y -= 1
        lag_x -= lag_x - lead_x
    elif lead_y - lag_y > 1:
        lag_y += 1
        lag_x -= lag_x - lead_x

    return lag_x, lag_y


def count_visited_positions(filepath):
    visited = {(0, 0)}
    H_X, H_Y = T_X, T_Y = (0, 0)

    with Path(filepath).open("r") as f:
        for line in f:
            values = line.strip()
            direction, times = values.split()

            if direction == "U":
                for _ in range(int(times)):
                    H_Y -= 1
                    T_X, T_Y = update_position((H_X, H_Y), (T_X, T_Y))
                    visited.add((T_X, T_Y))
            elif direction == "D":
                for _ in range(int(times)):
                    H_Y += 1
                    T_X, T_Y = update_position((H_X, H_Y), (T_X, T_Y))
                    visited.add((T_X, T_Y))
            elif direction == "L":
                for _ in range(int(times)):
                    H_X -= 1
                    T_X, T_Y = update_position((H_X, H_Y), (T_X, T_Y))
                    visited.add((T_X, T_Y))
            else:
                for _ in range(int(times)):
                    H_X += 1
                    T_X, T_Y = update_position((H_X, H_Y), (T_X, T_Y))
                    visited.add((T_X, T_Y))

    return len(visited)


def count_visited_positions2(filepath):
    visited = {(0, 0)}
    knots = dict([(i, {"x": 0, "y": 0}) for i in range(10)])

    with Path(filepath).open("r") as f:
        for line in f:
            values = line.strip()
            direction, times = values.split()

            if direction == "U":
                for _ in range(int(times)):
                    knots[0]["y"] -= 1

                    for i in range(1, 10):
                        knots[i]["x"], knots[i]["y"] = update_position(
                            (knots[i - 1]["x"], knots[i - 1]["y"]),
                            (knots[i]["x"], knots[i]["y"]),
                        )

                        if i == 9:
                            visited.add((knots[i]["x"], knots[i]["y"]))
            elif direction == "D":
                for _ in range(int(times)):
                    knots[0]["y"] += 1

                    for i in range(1, 10):
                        knots[i]["x"], knots[i]["y"] = update_position(
                            (knots[i - 1]["x"], knots[i - 1]["y"]),
                            (knots[i]["x"], knots[i]["y"]),
                        )

                        if i == 9:
                            visited.add((knots[i]["x"], knots[i]["y"]))
            elif direction == "L":
                for _ in range(int(times)):
                    knots[0]["x"] -= 1

                    for i in range(1, 10):
                        knots[i]["x"], knots[i]["y"] = update_position(
                            (knots[i - 1]["x"], knots[i - 1]["y"]),
                            (knots[i]["x"], knots[i]["y"]),
                        )

                        if i == 9:
                            visited.add((knots[i]["x"], knots[i]["y"]))
            else:
                for _ in range(int(times)):
                    knots[0]["x"] += 1

                    for i in range(1, 10):
                        knots[i]["x"], knots[i]["y"] = update_position(
                            (knots[i - 1]["x"], knots[i - 1]["y"]),
                            (knots[i]["x"], knots[i]["y"]),
                        )

                        if i == 9:
                            visited.add((knots[i]["x"], knots[i]["y"]))

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
        print(count_visited_positions(args.input_path))
    else:
        print(count_visited_positions2(args.input_path))
