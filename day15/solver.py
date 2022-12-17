import functools
import re
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path


def get_bounds(devices):
    sensors = dict([(k, v) for k, v in devices.items() if v["type"] == "S"])
    min_row = max_row = min_col = max_col = 0

    for i, (k, v) in enumerate(sensors.items()):
        if i == 0:
            min_row = k[0] - v["coverage"]
            max_row = k[0] + v["coverage"]
            min_col = k[1] - v["coverage"]
            max_col = k[1] + v["coverage"]
        else:
            min_row = min(min_row, k[0] - v["coverage"])
            max_row = max(max_row, k[0] + v["coverage"])
            min_col = min(min_col, k[1] - v["coverage"])
            max_col = max(max_col, k[1] + v["coverage"])

    return min_row, max_row, min_col, max_col


def get_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_devices(filepath):
    devices = {}

    with Path(filepath).open("r") as f:
        for line in f:
            values = line.strip()
            sensor_str, beacon_str = values.split(":")
            sensor_x, sensor_y = map(int, re.findall(r"-?\d+", sensor_str))
            beacon_x, beacon_y = map(int, re.findall(r"-?\d+", beacon_str))
            distance = get_distance((sensor_y, sensor_x), (beacon_y, beacon_x))

            devices[(sensor_y, sensor_x)] = {"type": "S", "coverage": distance}
            devices[(beacon_y, beacon_x)] = {"type": "B"}

    return devices


def cannot_have_beacon(x, y, devices):
    # if position is already occupied
    if (y, x) in devices:
        return 0

    # if position is within coverage of a sensor
    sensors = dict([(k, v) for k, v in devices.items() if v["type"] == "S"])
    for k, v in sensors.items():
        distance = get_distance((y, x), k)

        if distance <= v["coverage"]:
            return 1

    return 0


def get_coverage(devices, line):
    _, _, min_col, max_col = get_bounds(devices)

    with ProcessPoolExecutor() as executor:
        results = executor.map(
            functools.partial(
                cannot_have_beacon,
                y=line,
                devices=devices,
            ),
            range(min_col, max_col + 1),
            chunksize=100,
        )

        return sum(results)


def parallel_search(
    unit, pivot, from_corner, sensors, search_space, distance_fn
):
    min_row, max_row, min_col, max_col = search_space

    if from_corner == "top":
        row, col = pivot[0] + unit, pivot[1] + unit
    elif from_corner == "right":
        row, col = pivot[0] + unit, pivot[1] - unit
    elif from_corner == "bottom":
        row, col = pivot[0] - unit, pivot[1] - unit
    else:
        row, col = pivot[0] - unit, pivot[1] + unit

    if row < min_row or row > max_row or col < min_col or col > max_col:
        return False

    for k, v in sensors.items():
        distance = distance_fn((row, col), k)

        if distance <= v["coverage"]:
            return False

    # exhausted all sensors within search space, this position is the beacon
    return True


def search_beacon(devices, search_space):
    min_row, _, min_col, _ = search_space
    sensors = dict([(k, v) for k, v in devices.items() if v["type"] == "S"])

    # parallelize
    with ProcessPoolExecutor() as executor:
        for k, v in sensors.items():
            s_y, s_x = k
            s_cov = v["coverage"]
            bounds = {}

            bounds["top"] = (s_y - s_cov - 1, s_x)
            bounds["right"] = (s_y, s_x + s_cov + 1)
            bounds["bottom"] = (s_y + s_cov + 1, s_x)
            bounds["left"] = (s_y, s_x - s_cov - 1)

            # sweep clockwise around sensor's border
            for corner, position in bounds.items():
                results = executor.map(
                    functools.partial(
                        parallel_search,
                        pivot=position,
                        from_corner=corner,
                        sensors=sensors,
                        search_space=search_space,
                        distance_fn=get_distance,
                    ),
                    range(s_cov + 1),
                    chunksize=100,
                )

                for unit, found in zip(range(s_cov), results):
                    if found:
                        if corner == "top":
                            return position[0] + unit, position[1] + unit
                        elif corner == "right":
                            return position[0] + unit, position[1] - unit
                        elif corner == "bottom":
                            return position[0] - unit, position[1] - unit
                        else:
                            return position[0] - unit, position[1] + unit

    # return OOB coords if beacon not found
    return min_row - 1, min_col - 1


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

    devices = get_devices(args.input_path)

    if args.part == "1":
        print(get_coverage(devices, 2000000))
    else:
        position = search_beacon(devices, (0, 4000000, 0, 4000000))
        print(position[1] * 4000000 + position[0])
