import re
import sys
import heapq
import math
import time
from collections import deque, defaultdict, Counter
from functools import cache

i = open("../../inputs/day19.txt").read().splitlines()


def is_in_bounds(point, max_x, max_y):
    return (0 <= point[0] <= max_x) and (0 <= point[1] <= max_y)


def is_int(a):
    b = math.floor(a + 0.5)
    # print(a, b, abs(a - b), sys.float_info.epsilon)
    return abs(a - b) < 0.001


class A:
    towels = []

    def __init__(self, ts):
        self.towels = ts

    @cache
    def backtrack(self, word):
        if not word:
            return 1
        for t in self.towels:
            if word.startswith(t):
                can_make = self.backtrack(word[len(t):])
                if can_make:
                    return 1

        return 0

class B:
    towels = []

    def __init__(self, ts):
        self.towels = ts

    @cache
    def backtrack(self, word):
        if not word:
            return 1
        sub_s = 0
        for t in self.towels:
            if word.startswith(t):
                sub_s += self.backtrack(word[len(t):])

        return sub_s
def part1(lines):
    ans = 0

    towels = [x.strip() for x in lines[0].split(",")]
    runs = lines[1:]
    game = A(towels)
    for yi, line in enumerate(runs):
        if line:
            ans += game.backtrack(line.strip())
    return ans

def part2(lines):
    ans = 0

    towels = [x.strip() for x in lines[0].split(",")]
    runs = lines[1:]
    game = B(towels)
    for yi, line in enumerate(runs):
        if line:
            ans += game.backtrack(line.strip())
    return ans

print("ans pt1:", part1(i))
print("***********part 2***************")
print(part2(i))
