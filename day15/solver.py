import functools
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Event


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


def get_coverage(devices, line):
    _, _, min_col, max_col = get_bounds(devices)
    sensors = dict([(k, v) for k, v in devices.items() if v["type"] == "S"])

    coverage = 0
    for col in range(min_col, max_col + 1):
        # if this point is a device, don't evaluate
        if (line, col) in devices:
            continue

        # is this point on the line within any coverage of a S
        for k, v in sensors.items():
            distance = get_distance((line, col), k)

            if distance <= v["coverage"]:
                coverage += 1
                break

    return coverage


def parallel_search(position, devices, distance_fn, event):
    # another task found beacon; terminate
    if event.is_set():
        return False

    sensors = dict([(k, v) for k, v in devices.items() if v["type"] == "S"])
    row, col = position

    if (row, col) in devices:
        return False

    for k, v in sensors.items():
        distance = distance_fn((row, col), k)

        if distance <= v["coverage"]:
            return False

    # exhausted all sensors, this position is the beacon
    return True


def search_beacon(devices, search_space):
    min_row, max_row, min_col, max_col = search_space
    event = Event()

    # feed them to worker pool
    with ThreadPoolExecutor(max_workers=1000) as executor:
        for row in range(min_row, max_row + 1):
            # generate list of candidates to search
            candidates = [(row, col) for col in range(min_col, max_col + 1)]

            results = executor.map(
                functools.partial(
                    parallel_search,
                    devices=devices,
                    distance_fn=get_distance,
                    event=event,
                ),
                candidates,
            )

            for pos, found in zip(candidates, results):
                if found:
                    # mark event to set so remaining tasks finish early
                    event.set()
                    return pos

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
