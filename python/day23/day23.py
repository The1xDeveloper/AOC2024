import re
import sys
import heapq
import math
import time
from collections import deque, defaultdict, Counter
from functools import cache
sys.setrecursionlimit(100000)
i = open("../../inputs/day23.txt").read().splitlines()

def manhat(curr, end):
    return abs(curr[0] - end[0]) + abs(curr[1] - end[1])


def is_in_bounds(point, max_x, max_y):
    return (0 <= point[0] <= max_x) and (0 <= point[1] <= max_y)


def is_int(a):
    b = math.floor(a + 0.5)
    # print(a, b, abs(a - b), sys.float_info.epsilon)
    return abs(a - b) < 0.001

def part1(lines):
    adj = defaultdict(set)
    ans = 0
    ts = set()
    for yi, line in enumerate(lines):
        a, b = line.split("-")
        a = a.strip()
        b = b.strip()
        adj[a].add(b)
        adj[b].add(a)
        if a.startswith("t"):
            ts.add(a)
        if b.startswith("t"):
            ts.add(b)
    ans_set = set()
    for t in ts:
        in_first_t = adj[t]
        for nei in in_first_t:
            in_neig = adj[nei]
            for nei2 in in_neig:
                if nei2 != t and nei2 in in_first_t:
                    l = [t, nei, nei2]
                    l.sort()
                    ans_set.add(''.join(l))

    return len(ans_set)

def are_all_connected(nodes, adj):
    print(nodes)
    for i in nodes:
        for j in nodes:
            if i == j:
                continue
            if j not in adj[i] or i not in adj[j]:
                return False
    return True

def part2(lines):
    adj = defaultdict(set)
    ans = 0
    ts = set()
    for yi, line in enumerate(lines):
        a, b = line.split("-")
        a = a.strip()
        b = b.strip()
        adj[a].add(b)
        adj[b].add(a)
        if a.startswith("t"):
            ts.add(a)
        if b.startswith("t"):
            ts.add(b)
    ans_set = set()
    potential_answers = list()
    adj_copy = adj.copy()
    m = defaultdict(int)
    for k, v in adj_copy.items():
        candidate = v | {k}
        q = deque([])
        q.append((k, candidate))
        seen = set()
        seen.add(k)
        while q:
            prev, current_candidate = q.popleft()

            has_added = False
            for nei in current_candidate:
                next_candidate = adj[nei] | {nei}
                c = next_candidate & current_candidate
                m[frozenset(c)] += 1
                # print("nei: ", nei, "c: ", c)
                if c and nei not in seen:
                    q.append((nei, c))
                    seen.add(nei)
                    has_added = True

            if not has_added:
                potential_answers.append(current_candidate)
    max_m = max([v for k, v in m.items()])
    z = [x for x, v in m.items() if v == max_m]
    print("=================")
    print(','.join(sorted(list(z[0]))))

    return len(ans_set)

print("ans pt1:", part1(i))
print("***********part 2***************")
print(part2(i))
