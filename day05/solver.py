import re
from pathlib import Path


def generate_stacks(filepath):
    stacks = {}

    with Path(filepath).open("r") as f:
        num_stacks = 0

        # 1st pass, determine number of stacks
        for line in f:
            if line.startswith(" "):
                num_stacks = int(line.strip()[-1])
                break

        # 2nd pass, build stacks
        f.seek(0, 0)
        for line in f:
            if line.startswith(" "):
                break

            for stack in range(num_stacks):
                stack_list = stacks.get(str(stack + 1), [])

                if stack == 0:
                    if line[1] != " ":
                        stack_list.append(line[1])
                else:
                    try:
                        if line[1 + stack * 4] != " ":
                            stack_list.append(line[1 + stack * 4])
                    except IndexError:
                        pass

                stacks[str(stack + 1)] = stack_list

    return dict([(k, v[::-1]) for k, v in stacks.items()])


def move_with_cratemover9000(filepath, stacks):
    with Path(filepath).open("r") as f:
        for line in f:
            if line.startswith("move"):
                qty, from_stack, to_stack = re.findall(r"\d+", line)

                for _ in range(int(qty)):
                    popped = stacks[from_stack].pop()
                    stacks[to_stack].append(popped)

    return "".join([v[-1] for v in stacks.values()])


def move_with_cratemover9001(filepath, stacks):
    with Path(filepath).open("r") as f:
        for line in f:
            if line.startswith("move"):
                qty, from_stack, to_stack = re.findall(r"\d+", line)

                to_move = stacks[from_stack][-int(qty) :]
                stacks[from_stack] = stacks[from_stack][: -int(qty)]
                stacks[to_stack] = stacks[to_stack] + to_move

    return "".join([v[-1] for v in stacks.values()])


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

    stacks = generate_stacks(args.input_path)

    if args.part == "1":
        print(move_with_cratemover9000(args.input_path, stacks))
    else:
        print(move_with_cratemover9001(args.input_path, stacks))
