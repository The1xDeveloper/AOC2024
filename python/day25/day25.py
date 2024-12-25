import re
import sys
import heapq
import math
import time
from collections import deque, defaultdict, Counter
from functools import cache

sys.setrecursionlimit(100000)
i = open("../../inputs/day25.txt").read()


def manhat(curr, end):
    return abs(curr[0] - end[0]) + abs(curr[1] - end[1])


def is_in_bounds(point, max_x, max_y):
    return (0 <= point[0] <= max_x) and (0 <= point[1] <= max_y)


def is_int(a):
    b = math.floor(a + 0.5)
    # print(a, b, abs(a - b), sys.float_info.epsilon)
    return abs(a - b) < 0.001


def part1(blob):
    locks = list()
    locks_heights = list()
    keys = list()
    keys_heights = list()
    for game in blob.split("\n\n"):
        game_lines = game.split("\n")
        game_lines = [x.strip() for x in game_lines if x.strip() != ""]
        print(game_lines)
        if all(x == "." for x in game_lines[-1].strip()):
            locks.append(game_lines)
            l_heights = defaultdict(int)
            for yi, line in enumerate(game_lines):
                for xi, ch in enumerate(line):
                    if ch == "#":
                        l_heights[xi] = max(l_heights[xi], yi)
            l_h = len(game_lines) - 1
            locks_heights.append((l_h, l_heights.values()))

        else:
            keys.append(game_lines)
            k_heights = defaultdict(int)
            for yi, line in enumerate(game_lines[::-1]):
                for xi, ch in enumerate(line):
                    if ch == "#":
                        k_heights[xi] = max(k_heights[xi], yi)
            keys_heights.append(k_heights.values())
    ans = 0
    for l_h, lock_h in locks_heights:
        for key_hight in keys_heights:
            if all(a + b < l_h for a, b in zip(lock_h, key_hight)):
                # print("good ", l_h, lock_h, key_hight)
                ans += 1
            # else:
            # print("failed ", l_h, lock_h, key_hight)

    return ans


print("ans pt1:", part1(i))
print("***********part 2***************")
# print(part2(i))
