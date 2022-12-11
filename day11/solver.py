from math import prod
from pathlib import Path

OPERATION = {
    "*": lambda x, y: x * y,
    "+": lambda x, y: x + y,
}


class TestFactory:
    def __init__(self, divisor):
        self.divisor = divisor

    def test(self, value):
        return value % self.divisor == 0


def generate_monkey_map(filepath):
    monkey_map = {}
    key = None
    items = None
    operator = None
    value = None
    test = None
    true_monkey = None
    false_monkey = None

    with Path(filepath).open("r") as f:
        for line in f:
            values = line.strip()

            if values.startswith("Monkey"):
                key = int(values.split()[1].strip(":"))
            elif values.startswith("Starting items"):
                items_str = values.split(":")[1].split(",")
                items = list(map(int, items_str))
            elif values.startswith("Operation"):
                operation = values.split("new = ")[1]
                operator = "*" if "*" in operation else "+"
                value = operation.split()[-1]
            elif values.startswith("Test"):
                divisor = int(values.split()[-1])
                test = TestFactory(divisor)
            elif values.startswith("If true"):
                true_monkey = int(values.split()[-1])
            elif values.startswith("If false"):
                false_monkey = int(values.split()[-1])
            else:
                monkey_map[key] = {
                    "items": items,
                    "operation": (operator, value),
                    "test": test,
                    "true": true_monkey,
                    "false": false_monkey,
                }

        # for last monkey
        monkey_map[key] = {
            "items": items,
            "operation": (operator, value),
            "test": test,
            "true": true_monkey,
            "false": false_monkey,
        }

    return monkey_map


def get_inspections(monkey_map, rounds, divisor):
    inspected = {}

    for _ in range(rounds):
        for i in range(len(monkey_map)):
            for item in monkey_map[i]["items"]:
                operator = monkey_map[i]["operation"][0]
                op_value = monkey_map[i]["operation"][1]

                if op_value != "old":
                    new = OPERATION[operator](item, int(op_value))
                else:
                    new = OPERATION[operator](item, item)

                new //= divisor

                test_result = monkey_map[i]["test"].test(new)

                if test_result:
                    monkey_map[monkey_map[i]["true"]]["items"].append(new)
                else:
                    monkey_map[monkey_map[i]["false"]]["items"].append(new)

                inspected[i] = inspected.get(i, 0) + 1

            # monkey now has no items this round
            monkey_map[i]["items"] = []

    return inspected


def get_inspections2(monkey_map, rounds):
    inspected = {}
    modulo = prod([i["test"].divisor for i in monkey_map.values()])

    for _ in range(rounds):
        for i in range(len(monkey_map)):
            for item in monkey_map[i]["items"]:
                operator = monkey_map[i]["operation"][0]
                op_value = monkey_map[i]["operation"][1]

                if op_value != "old":
                    new = OPERATION[operator](item, int(op_value))
                else:
                    new = OPERATION[operator](item, item)

                new %= modulo

                test_result = monkey_map[i]["test"].test(new)

                if test_result:
                    monkey_map[monkey_map[i]["true"]]["items"].append(new)
                else:
                    monkey_map[monkey_map[i]["false"]]["items"].append(new)

                inspected[i] = inspected.get(i, 0) + 1

            # monkey now has no items this round
            monkey_map[i]["items"].clear()

    return inspected


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

    instructions = generate_monkey_map(args.input_path)

    if args.part == "1":
        inspections = get_inspections(instructions, 20, 3)
        product = prod(sorted(inspections.values(), reverse=True)[:2])
        print(product)
    else:
        inspections = get_inspections2(instructions, 10000)
        product = prod(sorted(inspections.values(), reverse=True)[:2])
        print(product)
