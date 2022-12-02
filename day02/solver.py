from pathlib import Path

SCORE_MAP = {
    "R": 1,
    "P": 2,
    "S": 3,
    "L": 0,
    "D": 3,
    "W": 6,
}

CODE_MAP = {
    "A": "R",
    "B": "P",
    "C": "S",
    "X1": "R",
    "Y1": "P",
    "Z1": "S",
    "X2": "L",
    "Y2": "D",
    "Z2": "W",
}


OUTCOME_MAP = {
    "RR": "D",
    "RP": "W",
    "RS": "L",
    "PR": "L",
    "PP": "D",
    "PS": "W",
    "SR": "W",
    "SP": "L",
    "SS": "D",
}

ROLL_MAP = {
    "RL": "S",
    "RD": "R",
    "RW": "P",
    "PL": "R",
    "PD": "P",
    "PW": "S",
    "SL": "P",
    "SD": "S",
    "SW": "R",
}


def calc_score(filepath, part):
    total = 0

    with Path(filepath).open("r") as f:
        for line in f:
            values = line.strip()

            if part == "1":
                opponent, player = values.split(" ")
                opponent = CODE_MAP[opponent]
                player = CODE_MAP[player + part]
                strategy = f"{opponent}{player}"

                total += SCORE_MAP[player] + SCORE_MAP[OUTCOME_MAP[strategy]]
            else:
                opponent, outcome = values.split(" ")
                opponent = CODE_MAP[opponent]
                outcome = CODE_MAP[outcome + part]
                strategy = f"{opponent}{outcome}"

                total += SCORE_MAP[ROLL_MAP[strategy]] + SCORE_MAP[outcome]

    return total


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

    score = calc_score(args.input_path, args.part)

    print(score)
