import re
from copy import deepcopy
from pathlib import Path
from typing import Tuple, List, Optional


def consume_next_crate(row_str) -> Tuple[Optional[str], Optional[str]]:
    if row_str == "":
        return None, None
    maybe_crate, row_str = row_str[:3], row_str[3:]
    if len(row_str) > 0:
        row_str = row_str[1:]
    return (maybe_crate[1] if maybe_crate[1] != " " else None), row_str


def parse_stacks(lines: List[str]) -> Tuple[List[List[str]], int]:
    stacks = []
    line_num = 0
    for line in lines:
        line_num += 1

        if "[" not in line:
            break

        i = 0
        maybe_crate, line = consume_next_crate(line)
        while line is not None:
            if i >= len(stacks):
                stacks.append([])
            if maybe_crate:
                stacks[i].insert(0, maybe_crate)
            i += 1
            maybe_crate, line = consume_next_crate(line)

    return stacks, line_num + 1


INSTRUCTION_REGEX = re.compile("move (\\d+) from (\\d+) to (\\d+)")


def parse_move_instruction(instruction: str) -> Tuple[int, int, int]:
    match = INSTRUCTION_REGEX.match(instruction)
    num_to_move = int(match.group(1))
    from_idx = int(match.group(2)) - 1
    to_idx = int(match.group(3)) - 1

    return num_to_move, from_idx, to_idx


def move(instruction: str, stacks: List[List[str]]):
    num_to_move, from_idx, to_idx = parse_move_instruction(instruction)
    for _ in range(num_to_move):
        stacks[to_idx].append(stacks[from_idx].pop())


def move_crate_mover_9001(instruction: str, stacks: List[List[str]]):
    num_to_move, from_idx, to_idx = parse_move_instruction(instruction)
    stacks[to_idx] += stacks[from_idx][-num_to_move:]
    stacks[from_idx] = stacks[from_idx][:-num_to_move]


def get_top_crate_string(stacks: List[List[str]]):
    top_crates = ""
    for stack in stacks:
        top_crates += stack[-1]

    return top_crates


def main():
    lines = Path("input.txt").read_text().splitlines()
    initial_stack_configuration, i = parse_stacks(lines)

    stacks = deepcopy(initial_stack_configuration)
    for line in lines[i:]:
        move(line, stacks)
    print(f"After performing all moves, the top crates are {get_top_crate_string(stacks)}")

    stacks = deepcopy(initial_stack_configuration)
    for line in lines[i:]:
        move_crate_mover_9001(line, stacks)
    print(f"Now that we know it is a CrateMover9001, the top crates are {get_top_crate_string(stacks)}")


if __name__ == "__main__":
    main()
