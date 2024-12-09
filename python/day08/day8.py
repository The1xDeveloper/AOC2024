import re
import heapq
from collections import deque, defaultdict, Counter


input = open("../../inputs/day8.txt").readlines()


def is_in_bounds(point, max_x, max_y):
    return (0 <= point[0] <= max_x) and (0 <= point[1] <= max_y)


# 425 too high
# ofc 613 too high......
def part1(lines):
    ans = 0
    antennas = defaultdict(list)
    max_y = len(lines) - 1
    max_x = (
        len(lines[0]) - 2
    )  # here was bug....... I have newlines!!!! must subtract 2.....
    for yi, line in enumerate(lines):
        line = line.strip()
        for xi, char in enumerate(line):
            if char != ".":
                antennas[char].append((xi, yi))
    antinodes = set()
    print(antennas.keys())
    for _, locs in antennas.items():
        for i in range(len(locs)):
            for j in range(i, len(locs)):
                if i == j:
                    continue
                a, b = locs[i], locs[j]
                change = (a[0] - b[0], a[1] - b[1])
                # print(change)
                pOne = (a[0] + change[0], a[1] + change[1])
                pTwo = (b[0] - change[0], b[1] - change[1])
                if is_in_bounds(pOne, max_x, max_y):
                    antinodes.add(pOne)
                if is_in_bounds(pTwo, max_x, max_y):
                    antinodes.add(pTwo)

    # print(len(antinodes))
    # print(antinodes)
    print(len(antinodes))

    return antinodes


# 1182 too low....
def part2(lines):
    ans = 0
    antennas = defaultdict(list)
    max_y = len(lines) - 1
    max_x = (
        len(lines[0]) - 2
    )  # here was bug....... I have newlines!!!! must subtract 2.....
    for yi, line in enumerate(lines):
        line = line.strip()
        for xi, char in enumerate(line):
            if char != ".":
                antennas[char].append((xi, yi))
    antinodes = set()
    for _, locs in antennas.items():
        for i in range(len(locs)):
            for j in range(i, len(locs)):
                if i == j:
                    continue
                a, b = locs[i], locs[j]
                change = (a[0] - b[0], a[1] - b[1])
                pOne = (a[0] + change[0], a[1] + change[1])
                antinodes.add(a)
                antinodes.add(b)
                while is_in_bounds(pOne, max_x, max_y):
                    antinodes.add(pOne)
                    pOne = (pOne[0] + change[0], pOne[1] + change[1])
                pTwo = (b[0] - change[0], b[1] - change[1])
                while is_in_bounds(pTwo, max_x, max_y):
                    antinodes.add(pTwo)
                    pTwo = (pTwo[0] - change[0], pTwo[1] - change[1])

    # print(len(antinodes))
    # print(antinodes)
    print(len(antinodes))

    return antinodes


def part1b(lines):
    antennas = defaultdict(list)

    for yi, line in enumerate(lines):
        line = line.strip()
        for xi, char in enumerate(line):
            if char != ".":
                antennas[char].append((xi, yi))

    nodes = set()
    for yi, line in enumerate(lines):
        line = line.strip()
        for xi, char in enumerate(line):
            for _, locs in antennas.items():
                set_locs = set(locs)
                diffs = calc_diffs(xi, yi, locs)
                set_diffs = set(diffs)
                if any(
                    (d[0] * 2, d[1] * 2) in set_diffs
                    and d[0] * 2 != d[0]
                    and d[1] * 2 != d[1]
                    for d in diffs
                ):
                    nodes.add((xi, yi))

    print(len(nodes))
    return nodes


def calc_diffs(xi, yi, locations):
    return [(xi - loc[0], yi - loc[1]) for loc in locations]


one = part1(input)
two = part1b(input)
print(one - two)
print(two - one)
print("***********part 2***************")
part2(input)
