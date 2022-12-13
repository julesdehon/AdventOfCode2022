from pathlib import Path
from typing import List, Tuple, Set


def index_to_char(index: int) -> str:
    if index == 0:
        return "H"
    return str(index)


def draw(knots: List[Tuple[int, int]], bottom_left: Tuple[int, int], top_right: Tuple[int, int]):
    (x0, y0), (x1, y1) = bottom_left, top_right
    for y in range(y1, y0 - 1, -1):
        line = ""
        for x in range(x0, x1 + 1):
            symbol = "."
            for i, coords in enumerate(knots):
                if coords == (x, y):
                    symbol = index_to_char(i)
                    break
            line += symbol
        print(line)
    print()


def move(knot: Tuple[int, int], direction: str) -> Tuple[int, int]:
    x, y = knot
    if direction == "U":
        return x, y + 1
    elif direction == "R":
        return x + 1, y
    elif direction == "D":
        return x, y - 1
    elif direction == "L":
        return x - 1, y


def follow(follower: Tuple[int, int], leader: Tuple[int, int]) -> Tuple[int, int]:
    (fx, fy), (lx, ly) = follower, leader
    horizontal_distance = lx - fx
    vertical_distance = ly - fy

    if abs(horizontal_distance) <= 1 and abs(vertical_distance) <= 1:
        return follower

    if abs(horizontal_distance) > 1:
        fx += horizontal_distance - (abs(horizontal_distance) / horizontal_distance)
        if abs(vertical_distance) > 1:
            fy += vertical_distance - (abs(vertical_distance) / vertical_distance)
        else:
            fy += vertical_distance

        return fx, fy

    if abs(vertical_distance) > 1:
        fy += vertical_distance - (abs(vertical_distance) / vertical_distance)
        if abs(horizontal_distance) > 1:
            fx += horizontal_distance - (abs(horizontal_distance) / horizontal_distance)
        else:
            fx += horizontal_distance

        return fx, fy


def get_unique_positions(movements: List[Tuple[str, int]], num_knots: int) -> Set[Tuple[int, int]]:
    knots = [(0, 0) for _ in range(num_knots)]
    unique_positions = set()

    # draw(knots, (-11, -5), (14, 15))
    for direction, steps in movements:
        for _ in range(steps):
            knots[0] = move(knots[0], direction)
            for i in range(1, num_knots):
                knots[i] = follow(knots[i], knots[i - 1])
            unique_positions.add(knots[-1])
        # draw(knots, (-11, -5), (14, 15))

    return unique_positions


def main():
    input_str = Path("input.txt").read_text()
    movements = [(direction, int(step_count)) for direction, step_count in
                 [line.split() for line in input_str.splitlines()]]

    unique_positions = get_unique_positions(movements, 2)
    print(f"The tail visited {len(unique_positions)} positions at least once")

    unique_positions_ten_knots = get_unique_positions(movements, 10)
    print(f"The tail of the 10-knot rope visited {len(unique_positions_ten_knots)} positions at least once")


if __name__ == "__main__":
    main()
