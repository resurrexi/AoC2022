import re
from collections import OrderedDict
from pathlib import Path


def get_shortest_path(to_traverse, dest, valves, traversed=set(), step=0):
    visited = traversed.copy()
    new_traverse_list = []

    if dest in to_traverse:
        return step

    visited.update(to_traverse)

    for v in to_traverse:
        for new_valve in valves[v]["to"]:
            if new_valve not in visited:
                new_traverse_list.append(new_valve)

    return get_shortest_path(
        new_traverse_list,
        dest,
        valves,
        traversed=visited,
        step=step + 1,
    )


def optimize_flow(valves):
    valves_copy = valves.copy()
    curr = list(valves_copy.keys())[0]
    opened = [k for k, v in valves_copy.items() if v["rate"] == 0]
    minute = 30
    step_required = 0
    total_flow = 0
    max_flow = 0
    next = None

    while minute > 0:
        # simulate an action taken going to a valve
        if step_required > 0:
            minute -= step_required
            step_required = 0
            continue
        elif max_flow > 0:
            # once step required is exhausted,
            # open valve, which means total flow is updated
            # update total flow
            total_flow += max_flow
            minute -= 1
            print(
                f"opening {curr} at {minute} remaining, adding {max_flow} for total {total_flow}"
            )
            max_flow = 0
            continue
        elif len(opened) == len(valves_copy):
            break

        # reset variables and determine next valve to open
        max_flow = 0
        for k, v in valves_copy.items():
            if k not in opened:
                steps = get_shortest_path([curr], k, valves_copy)
                valve_rate = v["rate"] * (minute - steps - 1)
                print(f"{curr} to {k}={v['rate']} in {steps}: {valve_rate}")
                if valve_rate > max_flow:
                    max_flow = valve_rate
                    next = k
                    step_required = steps

        # add next valve to opened
        opened.append(next)
        curr = next

    return total_flow


def get_valves(filepath):
    valves = OrderedDict()

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
        print(optimize_flow(valves))
    else:
        pass
