from __future__ import annotations

from pathlib import Path
import numpy as np


def possible_moves(map_arr, tile):
    y, x = [int(n) for n in tile]
    height, width = map_arr.shape
    possible_tiles_to_move_to = []

    if x > 0 and ord(map_arr[y, x - 1]) <= ord(map_arr[y, x]) + 1:
        possible_tiles_to_move_to.append((y, x - 1))
    if x < width - 1 and ord(map_arr[y, x + 1]) <= ord(map_arr[y, x]) + 1:
        possible_tiles_to_move_to.append((y, x + 1))
    if y > 0 and ord(map_arr[y - 1, x]) <= ord(map_arr[y, x]) + 1:
        possible_tiles_to_move_to.append((y - 1, x))
    if y < height - 1 and ord(map_arr[y + 1, x]) <= ord(map_arr[y, x]) + 1:
        possible_tiles_to_move_to.append((y + 1, x))

    return possible_tiles_to_move_to


def search(map_arr, start, end):
    queue = []
    explored = {(int(start[0]), int(start[1]))}
    queue.append((start, 0))
    while len(queue) > 0:
        next_tile, moves_made = queue.pop(0)
        if next_tile == end:
            return moves_made
        for move in possible_moves(map_arr, next_tile):
            if (int(move[0]), int(move[1])) not in explored:
                explored.add(move)
                queue.append((move, moves_made + 1))


def main():
    input_str = Path("input.txt").read_text()
    map_arr = np.array([list(line) for line in input_str.splitlines()])
    start = np.where(map_arr == "S")
    map_arr[start] = "a"
    end = np.where(map_arr == "E")
    map_arr[end] = "z"
    min_distance = search(map_arr, start, end)
    print(f"Minimum distance from start to finish = {min_distance}")

    all_lowest_points = np.transpose(np.where(map_arr == "a"))
    distances = [search(map_arr, (y, x), end) for (y, x) in all_lowest_points]
    print(f"Minimum trail length = {min([d for d in distances if d is not None])}")


if __name__ == "__main__":
    main()
