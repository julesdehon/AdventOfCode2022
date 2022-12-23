from __future__ import annotations

import math
from pathlib import Path
from typing import List, Callable

import tqdm as tqdm


def rest_of_string(after: str, original: str) -> str:
    if after not in original:
        return ""
    return original[original.find(after) + len(after):]


class Monkey:
    def __init__(self, starting_items: List[int], operation: Callable[[int], int], relieve: Callable[[int], int],
                 test: Callable[[int], bool], throw_to_if_true: int, throw_to_if_false: int, monkeys: List[Monkey]):
        self.items = starting_items
        self.operation = operation
        self.relieve = relieve
        self.test = test
        self.throw_to_if_true = throw_to_if_true
        self.throw_to_if_false = throw_to_if_false
        self.monkeys = monkeys
        self.times_inspected = 0

    def take_turn(self):
        while len(self.items) > 0:
            item = self.items.pop(0)
            item = self.operation(item)
            item = self.relieve(item)
            monkey_to_throw_to = self.throw_to_if_true if self.test(item) else self.throw_to_if_false
            self.monkeys[monkey_to_throw_to].items.append(item)
            self.times_inspected += 1


def parse_starting_items(raw_starting_items: str) -> List[int]:
    str_to_find = "Starting items: "
    raw_starting_items = rest_of_string(str_to_find, raw_starting_items).split(", ")
    return [int(starting_item) for starting_item in raw_starting_items]


def parse_operation(raw_operation: str) -> Callable[[int], int]:
    str_to_find = "Operation: new = "
    arg1, op, arg2 = rest_of_string(str_to_find, raw_operation).split()
    op = (lambda x, y: x + y) if op == "+" else (lambda x, y: x * y)
    return lambda old: op(old if arg1 == "old" else int(arg1), old if arg2 == "old" else int(arg2))


def parse_test(raw_test: str) -> Callable[[int], bool]:
    str_to_find = "Test: divisible by "
    divisible_by = int(rest_of_string(str_to_find, raw_test))
    return lambda item: item % divisible_by == 0


def parse_monkey_to_throw_to(raw_monkey_to_throw_to: str) -> int:
    str_to_find = "throw to monkey "
    return int(rest_of_string(str_to_find, raw_monkey_to_throw_to))


def parse_monkeys(lines: List[str], relieve: Callable[[int], int]) -> List[Monkey]:
    monkeys = []
    i = 0
    while i < len(lines):
        monkeys.append(Monkey(
            parse_starting_items(lines[i + 1]),
            parse_operation(lines[i + 2]),
            relieve,
            parse_test(lines[i + 3]),
            parse_monkey_to_throw_to(lines[i + 4]),
            parse_monkey_to_throw_to(lines[i + 5]),
            monkeys
        ))
        i += 7
    return monkeys


def find_all_divisors(lines: List[str]):
    str_to_find = "Test: divisible by "
    return [int(rest_of_string(str_to_find, line)) for line in lines if str_to_find in line]


def main():
    input_str = Path("input.txt").read_text()
    monkeys = parse_monkeys(input_str.splitlines(), lambda x: x // 3)
    for _ in range(20):
        [monkey.take_turn() for monkey in monkeys]
    monkey_business = math.prod(sorted([monkey.times_inspected for monkey in monkeys], reverse=True)[:2])
    print(f"After 20 rounds, the level of monkey business is {monkey_business}")

    all_divisors = find_all_divisors(input_str.splitlines())
    monkeys = parse_monkeys(input_str.splitlines(), lambda x: x % math.prod(all_divisors))
    for _ in range(10000):
        [monkey.take_turn() for monkey in monkeys]
    monkey_business = math.prod(sorted([monkey.times_inspected for monkey in monkeys], reverse=True)[:2])
    print(f"After 20 rounds, the level of monkey business is {monkey_business}")


if __name__ == "__main__":
    main()
