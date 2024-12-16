import re
import sys
import heapq
import math
import time
import copy
from collections import deque, defaultdict, Counter

i = open("../../inputs/day16.txt").read().splitlines()



def is_in_bounds(point, max_x, max_y):
    return (0 <= point[0] <= max_x) and (0 <= point[1] <= max_y)


def is_int(a):
    b = math.floor(a + 0.5)
    # print(a, b, abs(a - b), sys.float_info.epsilon)
    return abs(a - b) < 0.001

def dikstras(start, end, graph):
    #    cost, currpoint
    h = [(0, start, (1, 0), [start])]
    node_track = defaultdict(lambda: 1e999)

    all_seen = set()
    m = 1e99
    while h:
        cost, curr_point, curr_dir, curr_path = heapq.heappop(h)
        if node_track[(curr_point, curr_dir)] < cost:
            continue
        node_track[(curr_point, curr_dir)] = cost

        if cost > m:
            continue

        if curr_point == end:
            for zzz in curr_path:
                all_seen.add(zzz)
            m = min(m, cost)

        next_striaght = (curr_point[0] + curr_dir[0], curr_point[1] + curr_dir[1])
        if graph[next_striaght[1]][next_striaght[0]] != "#" and next_striaght not in set(curr_path):
            if cost + 1 > m:
                continue
            heapq.heappush(h, (cost + 1, next_striaght, curr_dir, curr_path + [next_striaght]))
        dy = curr_dir[1]
        dx = curr_dir[0]
        # clockwise dir
        dy = -1 * dy
        dy, dx = dx, dy
        clockwise = (curr_point[0] + dx, curr_point[1] + dy)
        if graph[clockwise[1]][clockwise[0]] != '#' and clockwise not in set(curr_path):
            if cost + 1001 > m:
                continue
            heapq.heappush(h, (cost + 1001, clockwise, (-curr_dir[1], curr_dir[0]), curr_path + [clockwise]))

        dy = curr_dir[1]
        dx = curr_dir[0]
        # counter-clockwise dir
        dx = -1 * dx
        dy, dx = dx, dy
        c_clockwise = (curr_point[0] + dx, curr_point[1] + dy)
        if graph[c_clockwise[1]][c_clockwise[0]] != '#' and c_clockwise not in set(curr_path):
            if cost + 1001 > m:
                continue
            heapq.heappush(h, (cost + 1001, c_clockwise, (curr_dir[1], -curr_dir[0]), curr_path + [c_clockwise]))

    print(len(all_seen))
    return m, all_seen
        
def part1(lines):
    ans = 0
    start = (0, 0)
    end = (0, 0)
    for yi, line in enumerate(lines):
        for xi, ch in enumerate(line):
            if ch == 'S':
                start = (xi, yi)
            if ch == 'E':
                end = (xi, yi)
    ans, paths = dikstras(start, end, lines)

    g = [list(s) for s in lines]
    for yi, line in enumerate(lines):
        for xi, ch in enumerate(line):
            if (xi, yi) in paths:
                g[yi][xi] = "O"
            else:
                g[yi][xi] = lines[yi][xi]
    for line in g:
        print(''.join(line))


    return ans 



target = part1(i)
print("ans pt1:", target)
print("***********part 2***************")
