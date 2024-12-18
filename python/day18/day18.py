import re
import sys
import heapq
import math
import time
from collections import deque, defaultdict, Counter

l = 71
max_x = l - 1
max_y = l - 1
grid = [['.'] * l for _ in range(l)]
i = open("../../inputs/day18.txt").read().splitlines()


def is_in_bounds(point, max_x, max_y):
    return (0 <= point[0] <= max_x) and (0 <= point[1] <= max_y)


def is_int(a):
    b = math.floor(a + 0.5)
    # print(a, b, abs(a - b), sys.float_info.epsilon)
    return abs(a - b) < 0.001

def print_grid():
    for row in grid:
        print(''.join(row))

def part1bi(lines):
    ans = 0
    i = 0
    for yi, line in enumerate(lines):
        x,y = line.split(",")
        x = int(x.strip())
        y = int(y.strip())
        if i < 1024:
            grid[y][x]= '#'
        i += 1
    # print_grid()
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    start = (0, 0)
    end = (70, 70)
    q1 = set([start])
    q2 = set([end])
    #     steps node
    seen = set()
    seen.add(start)
    seen.add(end)
    stepz = 0

    while q1 and q2:
        if len(q1) > len(q2):
            q1,q2 = q2,q1

        q = set([])
        for curr_node in q1:
            for dx, dy in directions:
                nx = curr_node[0] + dx
                ny = curr_node[1] + dy
                if is_in_bounds((nx, ny), max_x, max_y) and grid[ny][nx] != '#':
                    if (nx, ny) in q2:
                        return stepz + 1
                    if (nx, ny)  not in seen:
                        seen.add((nx, ny))
                        q.add((nx, ny))
        q,q1 = q1,q
        stepz += 1

    # print_grid()
    return ans
def part1(lines):
    ans = 0
    i = 0
    for yi, line in enumerate(lines):
        x,y = line.split(",")
        x = int(x.strip())
        y = int(y.strip())
        if i < 1024:
            grid[y][x]= '#'
        i += 1
    # print_grid()
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    start = (0, 0)
    end = (70, 70)
    q = deque([])
    #     steps node
    q.append((0, start))
    seen = set()
    stepz = 0

    while q:
        q_len = len(q)
        for _ in range(q_len):
            steps, curr_node = q.popleft()
            seen.add(curr_node)
            if curr_node == end:
                ans = steps
                return steps

            for dx, dy in directions:
                nx = curr_node[0] + dx
                ny = curr_node[1] + dy
                if (nx, ny) not in seen and is_in_bounds((nx, ny), max_x, max_y) and grid[ny][nx] != '#':
                    seen.add((nx, ny))
                    q.append((steps + 1, (nx, ny)))
        stepz += 1

    # print_grid()
    return ans

def part2bi(lines):
    ans = 0
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    start = (0, 0)
    i = 0
    end = (max_x, max_y)
    for yi, line in enumerate(lines):
        x,y = line.split(",")
        x = int(x.strip())
        y = int(y.strip())
        grid[y][x]= '#'
        i += 1
        if i >= 1024:
            q1 = set([start])
            q2 = set([end])
            #     steps node
            seen = set()
            seen.add(start)
            seen.add(end)
            stepz = 0
            can_reach = False

            while q1 and q2:
                if len(q1) > len(q2):
                    q1,q2 = q2,q1

                q = set([])
                for curr_node in q1:
                    for dx, dy in directions:
                        nx = curr_node[0] + dx
                        ny = curr_node[1] + dy
                        if is_in_bounds((nx, ny), max_x, max_y) and grid[ny][nx] != '#':
                            if (nx, ny) in q2:
                                can_reach = True
                                break
                            if (nx, ny)  not in seen:
                                seen.add((nx, ny))
                                q.add((nx, ny))
                if can_reach:
                    break
                q,q1 = q1,q
                stepz += 1
            if can_reach == False:
                print(f"{x},{y}")
                exit()

    # print_grid()
    return ans
def part2(lines):
    ans = 0
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    start = (0, 0)
    i = 0
    end = (max_x, max_y)
    for yi, line in enumerate(lines):
        x,y = line.split(",")
        x = int(x.strip())
        y = int(y.strip())
        grid[y][x]= '#'
        i += 1
        if i >= 1024:
            q = deque([])
            #     steps node
            q.append((0, start))
            seen = set()

            can_reach = False
            while q:
                steps, curr_node = q.popleft()
                seen.add(curr_node)
                if curr_node == end:
                    can_reach = True
                    break
                for dx, dy in directions:
                    nx = curr_node[0] + dx
                    ny = curr_node[1] + dy
                    if (nx, ny) not in seen and is_in_bounds((nx, ny), max_x, max_y) and grid[ny][nx] != '#':
                        seen.add((nx, ny))
                        q.append((steps + 1, (nx, ny)))
            if can_reach == False:
                print(f"{x},{y}")
                exit()

    # print_grid()
    return ans


# print("ans pt1:", part1(i))
# print("ans pt1:", part1bi(i))
print("***********part 2***************")
# print(part2(i))
print(part2bi(i))
