import ast
import functools
from copy import deepcopy
from pathlib import Path
from typing import List, Any, Optional


def correct_order(left: List[Any], right: List[Any]) -> Optional[bool]:
    left = deepcopy(left)
    right = deepcopy(right)

    if len(left) == 0:
        return None if len(right) == 0 else True
    if len(right) == 0:
        return False

    if isinstance(left[0], int) and isinstance(right[0], int):
        return correct_order(left[1:], right[1:]) if left[0] == right[0] else left[0] < right[0]

    if isinstance(left[0], int) or isinstance(right[0], int):
        left[0] = [left[0]] if isinstance(left[0], int) else left[0]
        right[0] = [right[0]] if isinstance(right[0], int) else right[0]
        return correct_order(left, right)

    first_item_is_correct = correct_order(left[0], right[0])
    if first_item_is_correct is None:
        return correct_order(left[1:], right[1:])
    return first_item_is_correct


def pair_comparator(left, right):
    correct = correct_order(left, right)
    return 0 if correct is None else (-1 if correct else 1)

test = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""
def main():
    input_str = Path("input.txt").read_text()
    # input_str = test
    raw_pairs = input_str.split("\n\n")
    pairs = [(ast.literal_eval(first), ast.literal_eval(second)) for first, second in
             [raw_pair.split("\n") for raw_pair in raw_pairs]]

    correct_indices = [index + 1 for index, correct in enumerate([correct_order(left, right) for (left, right) in pairs]) if correct]
    print(sum(correct_indices))

    all_packets = []
    for left, right in pairs:
        all_packets += [left, right]

    all_packets += [[[2]], [[6]]]
    sorted_packets = sorted(all_packets, key=functools.cmp_to_key(pair_comparator))
    divider_packet_1_index = sorted_packets.index([[2]]) + 1
    divider_packet_2_index = sorted_packets.index([[6]]) + 1
    print(f"The decoder key is {divider_packet_1_index * divider_packet_2_index}")


if __name__ == "__main__":
    main()
