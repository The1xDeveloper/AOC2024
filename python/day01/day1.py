import re
import heapq
from collections import deque, defaultdict, Counter


input = open("../../inputs/day1.txt").readlines()


def part1(lines):
    a = []
    b = []
    for line in lines:
        x, y = line.split()
        a.append(int(x.strip()))
        b.append(int(y.strip()))
    a.sort()
    b.sort()
    ans = 0
    for p, q in zip(a, b):
        t = abs(p - q)
        ans += t

    return ans


def part2(lines):
    a = []
    b = []
    for line in lines:
        x, y = line.split()
        a.append(int(x.strip()))
        b.append(int(y.strip()))
    freq = Counter(b)
    ans = 0
    for p in a:
        if p in freq:
            f = freq[p]
            ans += p * f

    return ans


print(part1(input))
print(part2(input))
