from pathlib import Path


class Node:
    def __init__(self, name, parent=None, size=None):
        self.parent = parent
        self.children = []
        self.name = name
        self.size = size

    def add_child(self, node):
        self.children.append(node)

    def up(self):
        return self.parent

    def down(self, name):
        for child in self.children:
            if child.name == name:
                return child

    def __str__(self):
        return f"{self.size if self.size else 'dir'} {self.name}"


def build_tree(filepath):
    root = None
    current = None

    with Path(filepath).open("r") as f:
        for line in f:
            line = line.strip()

            if line.startswith("$ cd"):
                _, command, argument = line.split()

                if command == "cd":
                    if argument == "/":
                        root = current = Node("/")
                    elif argument == "..":
                        current = current.up()
                    else:
                        current = current.down(argument)
            elif line.startswith("$ ls"):
                pass  # ignore this command
            else:
                detail, name = line.split()

                if detail.startswith("dir"):
                    current.add_child(Node(name, parent=current))
                else:
                    current.add_child(
                        Node(name, parent=current, size=int(detail))
                    )

    return root


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
        start = build_tree(args.input_path)
        print(start)
    else:
        pass
