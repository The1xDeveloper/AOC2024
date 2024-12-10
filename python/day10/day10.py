import re
import heapq
from collections import deque, defaultdict, Counter


input = open("../../inputs/day10.txt").read().splitlines()


def is_in_bounds(point, max_x, max_y):
    return (0 <= point[0] <= max_x) and (0 <= point[1] <= max_y)


def bfs2(xi, yi, lines):
    directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    max_y = len(lines) - 1
    max_x = len(lines[0]) - 1
    q = deque([(0, xi, yi)])
    ans = 0
    while q:
        steps, curr_x, curr_y = q.popleft()
        for dx, dy in directions:
            px = curr_x + dx
            py = curr_y + dy
            if is_in_bounds((px, py), max_x, max_y):
                is_p_inc = int(lines[py][px]) == int(lines[curr_y][curr_x]) + 1
                if not is_p_inc:
                    continue
                if lines[py][px] == "9":
                    ans += 1
                else:
                    q.append((steps + 1, px, py))
    return ans


def bfs(xi, yi, lines):
    directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    max_y = len(lines) - 1
    max_x = len(lines[0]) - 1
    seen = set()
    q = deque([(0, xi, yi)])
    nines = set()
    while q:
        steps, curr_x, curr_y = q.popleft()
        seen.add((curr_x, curr_y))
        for dx, dy in directions:
            px = curr_x + dx
            py = curr_y + dy
            if (px, py) not in seen and is_in_bounds((px, py), max_x, max_y):
                is_p_inc = int(lines[py][px]) == int(lines[curr_y][curr_x]) + 1
                if not is_p_inc:
                    continue
                seen.add((px, py))
                if lines[py][px] == "9":
                    nines.add((px, py))
                else:
                    q.append((steps + 1, px, py))
    return len(nines)


def part1b(lines):
    ans = 0
    for yi, line in enumerate(lines):
        for xi, char in enumerate(line):
            if char == "0":
                ans += bfs(xi, yi, lines)
    return ans


def part2(lines):
    ans = 0
    for yi, line in enumerate(lines):
        for xi, char in enumerate(line):
            if char == "0":
                ans += bfs2(xi, yi, lines)
    return ans


print("ans pt1:", part1b(input))
print("***********part 2***************")
print(part2(input))
