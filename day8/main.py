from pathlib import Path
from typing import List, Any, Tuple, Iterable, Callable


def first_idx(xs: List[Any], predicate: Callable[[Any], bool]) -> int:
    try:
        return next(i + 1 for i, x in enumerate(xs) if predicate(x))
    except StopIteration:
        return len(xs)


def is_visible(tree_heights: List[List[int]], i: int, j: int) -> bool:
    tree_height = tree_heights[i][j]
    visible_from_left = all(
        height < tree_height for height in tree_heights[i][:j])
    visible_from_top = all(
        height < tree_height for height in [tree_heights[p][j] for p in range(i)])
    visible_from_right = all(
        height < tree_height for height in tree_heights[i][j + 1:])
    visible_from_bottom = all(
        height < tree_height for height in [tree_heights[p][j] for p in range(i + 1, len(tree_heights))])

    return visible_from_left or visible_from_top or visible_from_right or visible_from_bottom


def scenic_score(tree_heights: List[List[int]], i: int, j: int) -> int:
    tree_height = tree_heights[i][j]
    visible_to_left = first_idx(
        [height for height in [tree_heights[i][p] for p in range(j - 1, -1, -1)]],
        lambda height: height >= tree_height)
    visible_to_top = first_idx(
        [height for height in [tree_heights[p][j] for p in range(i - 1, -1, -1)]],
        lambda height: height >= tree_height)
    visible_to_right = first_idx(
        [height for height in [tree_heights[i][p] for p in range(j + 1, len(tree_heights[0]))]],
        lambda height: height >= tree_height)
    visible_to_bottom = first_idx(
        [height for height in [tree_heights[p][j] for p in range(i + 1, len(tree_heights))]],
        lambda height: height >= tree_height)

    return visible_to_left * visible_to_top * visible_to_right * visible_to_bottom


def main():
    input_str = Path("input.txt").read_text()
    tree_heights = [[int(height) for height in line] for line in input_str.splitlines()]
    all_indices = [(i, j) for i in range(len(tree_heights)) for j in range(len(tree_heights[0]))]
    number_of_visible_trees = sum([is_visible(tree_heights, i, j) for (i, j) in all_indices])
    print(f"The number of visible trees is {number_of_visible_trees}")

    highest_scenic_score = max([scenic_score(tree_heights, i, j) for (i, j) in all_indices])
    print(f"The highest scenic score is {highest_scenic_score}")


if __name__ == "__main__":
    main()
