from pathlib import Path


class PathNode:
    def __init__(self, x, y, elevation, is_destination=False):
        self.x = x
        self.y = y
        self.elevation = elevation
        self.is_destination = is_destination
        self.L = None
        self.R = None
        self.T = None
        self.B =None

    def add_L(self, L):
        self.L = L

    def add_R(self, R):
        self.R = R

    def add_T(self, T):
        self.T = T

    def add_B(self, B):
        self.B = B

    def go_direction(self, direction):
        if direction == "left":
            return self.L
        elif direction == "right":
            return self.R
        elif direction == "up":
            return self.T
        else:
            return self.B


def generate_matrix(filepath):
    matrix = []

    with Path(filepath).open("r") as f:
        for line in f:
            values = list(line.strip())
            matrix.append(values)
    return matrix


def get_shortest(matrix, cursor=(0,0), traversed=[], to_traverse=[], step=0):
    x, y = cursor
    elevation = "z" if matrix[x][y] == "E" else matrix[x][y]
    is_destination = matrix[x][y] == "E"


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
        pass
    else:
        pass
