import re
import heapq
from collections import deque, defaultdict, Counter


input = open("../../inputs/day6.txt").readlines()


def bfs_find_cycle(origin, lines):
    dy = -1
    dx = 0
    max_y = len(lines) - 1
    max_x = len(lines[0]) - 1
    seen = set()
    xi, yi = origin
    q = deque([(0, xi, yi)])
    while q:
        steps, curr_x, curr_y = q.popleft()
        if (curr_x, curr_y, dx, dy) in seen:
            return 1
        seen.add((curr_x, curr_y, dx, dy))
        px = curr_x + dx
        py = curr_y + dy
        if not ((0 <= px <= max_x) and (0 <= py <= max_y)):
            return 0
        while lines[py][px] == "#":
            dy = -1 * dy
            dy, dx = dx, dy
            px = curr_x + dx
            py = curr_y + dy

            if not ((0 <= px <= max_x) and (0 <= py <= max_y)):
                return 0
        q.append((steps + 1, px, py))
    return 0


def bfspt2(xi, yi, lines):
    dy = -1
    dx = 0
    max_y = len(lines) - 1
    max_x = len(lines[0]) - 1
    seen = set()
    q = deque([(0, xi, yi)])
    while q:
        steps, curr_x, curr_y = q.popleft()
        seen.add((curr_x, curr_y))
        px = curr_x + dx
        py = curr_y + dy
        if not ((0 <= px <= max_x) and (0 <= py <= max_y)):
            return seen
        while lines[py][px] == "#":
            dy = -1 * dy
            dy, dx = dx, dy
            px = curr_x + dx
            py = curr_y + dy

            if not ((0 <= px <= max_x) and (0 <= py <= max_y)):
                return seen
        q.append((steps + 1, px, py))
    return seen


def bfs(xi, yi, lines):
    dy = -1
    dx = 0
    max_y = len(lines) - 1
    max_x = len(lines[0]) - 1
    seen = set()
    q = deque([(0, xi, yi)])
    while q:
        steps, curr_x, curr_y = q.popleft()
        seen.add((curr_x, curr_y))
        px = curr_x + dx
        py = curr_y + dy
        if not ((0 <= px <= max_x) and (0 <= py <= max_y)):
            return len(seen)
        while lines[py][px] == "#":
            dy = -1 * dy
            dy, dx = dx, dy
            px = curr_x + dx
            py = curr_y + dy

            if not ((0 <= px <= max_x) and (0 <= py <= max_y)):
                return len(seen)
        q.append((steps + 1, px, py))
    return -1


def part1(lines):
    ans = 0
    for yi, line in enumerate(lines):
        for xi, char in enumerate(line):
            if char == "^":
                return bfs(xi, yi, lines)

    return ans


def part2(lines):
    ans = 0
    potential_spots = set()
    origin = None
    grid = [list(s) for s in lines]
    for yi, line in enumerate(grid):
        for xi, char in enumerate(line):
            if char == "^":
                origin = (xi, yi)
                potential_spots = bfspt2(xi, yi, lines)
                break
    for ox, oy in potential_spots:
        if (ox, oy) == origin:
            continue
        grid[oy][ox] = "#"
        ans += bfs_find_cycle(origin, grid)
        grid[oy][ox] = "."

    return ans


print(part1(input))
print("***********part 2***************")
print(part2(input))
