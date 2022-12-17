import re
from pathlib import Path


def get_valves(filepath):
    valves = {}

    with Path(filepath).open("r") as f:
        for line in f:
            values = line.strip()
            valve_str, tunnels_str = values.split(";")
            valve = valve_str[6:8]
            flow_rate = int(valve_str[valve_str.index("=") + 1 :])
            destinations = re.findall(r"[A-Z]{2}", tunnels_str)

            valves[valve] = {"rate": flow_rate, "to": destinations}

    return valves


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

    valves = get_valves(args.input_path)

    if args.part == "1":
        print(valves)
    else:
        pass
