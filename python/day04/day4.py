import re
import heapq
from collections import deque, defaultdict, Counter


input = open("../../inputs/day4.txt").readlines()


def find(xi, yi, grid):
    c = 0
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    max_y = len(grid) - 1
    max_x = len(grid[0]) - 1
    for dx, dy in directions:
        sub_str = "X"
        cx = xi
        cy = yi
        for _ in range(3):
            cx = cx + dx
            cy = cy + dy
            if not (0 <= cx <= max_x and 0 <= cy <= max_y):
                sub_str = "X"
                break
            sub_str += grid[cy][cx]
        if sub_str == "XMAS":
            c += 1

    return c


def find2(xi, yi, grid):
    max_y = len(grid) - 1
    max_x = len(grid[0]) - 1
    if not ((0 <= xi + 1 <= max_x) and (0 <= xi - 1 <= max_x)):
        return 0
    if not ((0 <= yi + 1 <= max_y) and (0 <= yi - 1 <= max_y)):
        return 0

    right_to_left = grid[yi - 1][xi - 1] + grid[yi][xi] + grid[yi + 1][xi + 1]
    left_to_right = grid[yi + 1][xi - 1] + grid[yi][xi] + grid[yi - 1][xi + 1]
    if (right_to_left == "MAS" or right_to_left[::-1] == "MAS") and (
        left_to_right == "MAS" or left_to_right[::-1] == "MAS"
    ):
        return 1
    return 0


def part1(lines):
    ans = 0
    for yi, line in enumerate(lines):
        for xi, char in enumerate(line):
            if char == "X":
                ans += find(xi, yi, lines)
    return ans


def part2(lines):
    ans = 0
    for yi, line in enumerate(lines):
        for xi, char in enumerate(line):
            if char == "A":
                ans += find2(xi, yi, lines)
    return ans


print(part1(input))
print("***********part 2***************")
print(part2(input))
