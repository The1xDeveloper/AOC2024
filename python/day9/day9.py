import re
import heapq
from collections import deque, defaultdict, Counter


input = open("../../inputs/day9.txt").read().splitlines()


def is_in_bounds(point, max_x, max_y):
    return (0 <= point[0] <= max_x) and (0 <= point[1] <= max_y)


def part1(lines):
    ans = 0
    for yi, line in enumerate(lines):
        for xi, char in enumerate(line):
            pass

    return ans


def part2(lines):
    ans = 0
    for yi, line in enumerate(lines):
        for xi, char in enumerate(line):
            pass

    return ans


one = part1(input)
print("***********part 2***************")
part2(input)
