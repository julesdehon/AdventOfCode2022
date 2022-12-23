from __future__ import annotations
from pathlib import Path
from typing import Set, Tuple, List


class World:
    SAND_START = (500, 0)

    def __init__(self, rock_coords: Set[Tuple[int, int]], with_floor=False):
        self._rock_coords = rock_coords
        self._sand_coords = set()
        self._lowest_y_coord = max(y for (x, y) in self._rock_coords)
        self._with_floor = with_floor

    def drop_sand(self) -> bool:
        if self.position_taken(self.SAND_START):
            return True

        (x, y) = self.SAND_START

        blocked = False
        while not blocked and (y < self._lowest_y_coord if not self._with_floor else True):
            if not self.position_taken((x, y + 1)):
                x, y = x, y + 1
                continue
            if not self.position_taken((x - 1, y + 1)):
                x, y = x - 1, y + 1
                continue
            if not self.position_taken((x + 1, y + 1)):
                x, y = x + 1, y + 1
                continue
            blocked = True

        if blocked:
            self._sand_coords.add((x, y))
            return False

        return True

    def position_taken(self, coord):
        return (coord in self._rock_coords or coord in self._sand_coords) or (
            coord[1] == self._lowest_y_coord + 2 if self._with_floor else False)

    @staticmethod
    def from_input(input_lines: List[str], with_floor=False) -> World:
        rock_coords = set()
        for line in input_lines:
            anchors = [(int(x), int(y)) for x, y in [raw_anchor.split(",") for raw_anchor in line.split(" -> ")]]
            for i in range(len(anchors) - 1):
                x_direction = 1 if anchors[i][0] <= anchors[i + 1][0] else -1
                y_direction = 1 if anchors[i][1] <= anchors[i + 1][1] else -1
                for x in range(anchors[i][0], anchors[i + 1][0] + x_direction, x_direction):
                    for y in range(anchors[i][1], anchors[i + 1][1] + y_direction, y_direction):
                        rock_coords.add((x, y))

        return World(rock_coords, with_floor=with_floor)


def main():
    input_str = Path("input.txt").read_text()

    world = World.from_input(input_str.splitlines())
    i = 0
    while not world.drop_sand():
        i += 1
    print(f"{i} units of sand come to rest before sand starts flowing into the abyss below")

    world_with_floor = World.from_input(input_str.splitlines(), with_floor=True)
    i = 0
    while not world_with_floor.drop_sand():
        i += 1
    print(f"{i} units of sand come to rest before the source of the sand becomes blocked")


if __name__ == "__main__":
    main()
