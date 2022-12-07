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
                _, _, argument = line.split()

                if argument == "/":
                    root = current = Node("/")
                elif argument == "..":
                    current = current.up()
                else:
                    current = current.down(f"{current.name}/{argument}")
            elif line.startswith("$ ls"):
                pass  # ignore this command
            else:
                detail, name = line.split()

                if detail.startswith("dir"):
                    current.add_child(
                        Node(f"{current.name}/{name}", parent=current)
                    )
                else:
                    current.add_child(
                        Node(
                            f"{current.name}/{name}",
                            parent=current,
                            size=int(detail),
                        )
                    )

    return root


def traverse_tree(current, dirs={}, to_traverse=[]):
    # add directory to dirs
    dirs[current.name] = dirs.get(current, 0)
    # fetch all target dirs that fall in the current dir's path (parents + current)
    target_dirs = [d for d in dirs.keys() if current.name.startswith(d)]

    for child in current.children:
        if child.size:
            for dir in target_dirs:
                dirs[dir] = dirs.get(dir, 0) + child.size
        else:
            to_traverse.append(child)

    if to_traverse:
        new_dir = to_traverse.pop()
        return traverse_tree(new_dir, dirs, to_traverse)

    return dirs


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

    start = build_tree(args.input_path)
    dirs = traverse_tree(start)

    if args.part == "1":
        sizes_under_100k = [v for v in dirs.values() if v <= 100000]
        print(sum(sizes_under_100k))
    else:
        # get size of root
        root_size = dirs["/"]

        remaining = 70000000 - root_size
        space_to_free_up = 30000000 - remaining
        sizes_meeting_criteria = [
            v for v in dirs.values() if v >= space_to_free_up
        ]

        print(min(sizes_meeting_criteria))
