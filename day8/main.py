from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Optional, Any


def flatten(list_of_lists: List[List[Any]]) -> List[Any]:
    return [item for sublist in list_of_lists for item in sublist]


class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size


class Directory:
    def __init__(self, name: str, parent: Optional[Directory]):
        self.name = name
        self.dirs: Dict[str, Directory] = {"..": parent}
        self.files: List[File] = []

    def _child_dirs(self) -> List[Directory]:
        return [directory for name, directory in self.dirs.items() if name != ".."]

    def mkdir(self, dir_name: str):
        self.dirs[dir_name] = Directory(dir_name, self)

    def touch(self, file_name: str, size: int):
        self.files.append(File(file_name, size))

    def all_child_dirs(self) -> List[Directory]:
        child_dirs = self._child_dirs()
        return child_dirs + flatten([child_dir.all_child_dirs() for child_dir in child_dirs])

    def get_total_size(self) -> int:
        return sum(file.size for file in self.files) + sum(
            directory.get_total_size() for directory in self._child_dirs())

    def __str__(self) -> str:
        dir_string = f"- {self.name} (dir)"
        for dir_name, directory in self.dirs.items():
            if directory is None or dir_name == "..":
                continue
            dir_string_with_indent = "  " + str(directory).replace("\n", "\n  ")
            dir_string += f"\n{dir_string_with_indent}"
        for file in self.files:
            dir_string += f"\n  - {file.name} (file, size={file.size})"

        return dir_string


class FileSystemNavigator:
    def __init__(self, root: Directory):
        self.root = root
        self.curr_dir = root

    def cd(self, dir_name: str):
        if dir_name == "/":
            self.curr_dir = self.root
            return

        self.curr_dir = self.curr_dir.dirs[dir_name]


def parse_directory_structure(console_output: List[str]) -> Directory:
    root = Directory("/", None)
    file_system_navigator = FileSystemNavigator(root)

    for line in console_output:
        if line[0] == "$":
            argv = line[2:].split()
            if argv[0] == "cd":
                file_system_navigator.cd(argv[1])
            continue

        out = line.split()
        if out[0] == "dir":
            file_system_navigator.curr_dir.mkdir(out[1])
        else:
            file_system_navigator.curr_dir.touch(out[1], int(out[0]))

    return root


def main():
    input_str = Path("input.txt").read_text()
    root = parse_directory_structure(input_str.splitlines())
    print(root)

    small_dir_sizes = [directory.get_total_size() for directory in root.all_child_dirs() if
                       directory.get_total_size() <= 100000]
    print(f"The sum of the total sizes of directories with size of at most 100000 is {sum(small_dir_sizes)}")

    free_space_required = 30_000_000 - (70_000_000 - root.get_total_size())
    smallest_sufficient_dir_size = min([directory.get_total_size() for directory in root.all_child_dirs() if
                                        directory.get_total_size() >= free_space_required])
    print(f"The size of the smallest directory that would be large enough to allow the system update is "
          f"{smallest_sufficient_dir_size}")


if __name__ == "__main__":
    main()
