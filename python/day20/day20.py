import re
import sys
import heapq
import math
import time
from collections import deque, defaultdict, Counter
from functools import cache

i = open("../../inputs/day20.txt").read().splitlines()
z = 100


def is_in_bounds(point, max_x, max_y):
    return (0 <= point[0] <= max_x) and (0 <= point[1] <= max_y)


def is_int(a):
    b = math.floor(a + 0.5)
    # print(a, b, abs(a - b), sys.float_info.epsilon)
    return abs(a - b) < 0.001

def bfs_from_end(grid, start, end):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    max_x = len(grid[0]) - 1
    max_y = len(grid) - 1


    q = deque([])
    #     steps node path
    q.append((0, end, [start]))
    seen = set()

    m = dict()
    can_reach = False
    while q:
        steps, curr_node, path = q.popleft()
        seen.add(curr_node)
        m[curr_node] = steps

        for dx, dy in directions:
            nx = curr_node[0] + dx
            ny = curr_node[1] + dy
            if (nx, ny) not in seen and is_in_bounds((nx, ny), max_x, max_y) and grid[ny][nx] != '#':
                seen.add((nx, ny))
                q.append((steps + 1, (nx, ny), path + [(nx, ny)]))

    return m
def bfs(grid, start, end):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    max_x = len(grid[0]) - 1
    max_y = len(grid) - 1


    q = deque([])
    #     steps node path
    q.append((0, start, [start]))
    seen = set()

    can_reach = False
    while q:
        steps, curr_node, path = q.popleft()
        seen.add(curr_node)
        if curr_node == end:
            return steps, path
            can_reach = True
            break
        for dx, dy in directions:
            nx = curr_node[0] + dx
            ny = curr_node[1] + dy
            if (nx, ny) not in seen and is_in_bounds((nx, ny), max_x, max_y) and grid[ny][nx] != '#':
                seen.add((nx, ny))
                q.append((steps + 1, (nx, ny), path + [(nx, ny)]))

    return None, None
def manhat(curr, end):
    return abs(curr[0] - end[0]) + abs(curr[1] - end[1])
def A_with_hacks2(grid, start, end, max_steps, golden_path):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    max_x = len(grid[0]) - 1
    max_y = len(grid) - 1
    q = []
    #     steps node
    heapq.heappush(q, (0, manhat(start, end),  -1, start, set()))

    can_reach = False
    ans = 0
    anser = []
    while q:
        steps, dist, hack, curr_node, seen = heapq.heappop(q)
        # print(steps, hack, curr_node, seen)
        # input()
        seen.add((curr_node[0], curr_node[1]))
        if curr_node == end:
            anser.append(steps)
            print(len(anser), steps, max_steps, z)
            if steps > max_steps - z:
                return anser

            ans += 1

            continue
        if steps + 1 <= max_steps - z:
            for dx, dy in directions:
                nx = curr_node[0] + dx
                ny = curr_node[1] + dy
                sx = curr_node[0] + 2*dx
                sy = curr_node[1] + 2*dy
                if (nx, ny) not in seen and is_in_bounds((nx, ny), max_x, max_y) and grid[ny][nx] != '#':
                    seen.add((nx, ny))
                    q.append((steps + 1, manhat((nx, ny), end), hack,(nx, ny), seen))
                    # else:
                    #     print(steps + 1, max_steps, max_steps - t + 1)
                elif hack < 0 and (sx, sy) not in seen and is_in_bounds((sx, sy), max_x, max_y) and grid[sy][sx] != '#':
                    if (sx, sy) in golden_path:
                        hack_set = seen.copy()
                        hack_set.add((sx, sy))
                        q.append((steps + 2, manhat((sx, sy), end), hack + 1, (sx, sy), hack_set))
                    # else:
                    #     print(steps + 1, max_steps, max_steps - t + 1)
    return anser

    return anser
def A_with_hacks(grid, start, end, max_steps, golden_path):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    max_x = len(grid[0]) - 1
    max_y = len(grid) - 1
    q = []
    #     steps node
    heapq.heappush(q, (manhat(start, end), 0, -1, start, set()))

    can_reach = False
    ans = 0
    anser = []
    while q:
        dist, steps, hack, curr_node, seen = heapq.heappop(q)
        # print(steps, hack, curr_node, seen)
        # input()
        seen.add((curr_node[0], curr_node[1]))
        if curr_node == end:
            anser.append(steps)
            print(len(anser), steps, max_steps, z)
            if steps > max_steps - z:
                return anser

            ans += 1

            continue
        if steps + 1 <= max_steps - z:
            for dx, dy in directions:
                nx = curr_node[0] + dx
                ny = curr_node[1] + dy
                sx = curr_node[0] + 2*dx
                sy = curr_node[1] + 2*dy
                if (nx, ny) not in seen and is_in_bounds((nx, ny), max_x, max_y) and grid[ny][nx] != '#':
                    seen.add((nx, ny))
                    q.append((manhat((nx, ny), end), steps + 1, hack,(nx, ny), seen))
                    # else:
                    #     print(steps + 1, max_steps, max_steps - t + 1)
                elif hack < 0 and (sx, sy) not in seen and is_in_bounds((sx, sy), max_x, max_y) and grid[sy][sx] != '#':
                    if (sx, sy) in golden_path:
                        hack_set = seen.copy()
                        hack_set.add((sx, sy))
                        q.append((manhat((sx, sy), end), steps + 2, hack + 1, (sx, sy), hack_set))
                    # else:
                    #     print(steps + 1, max_steps, max_steps - t + 1)
    return anser


def bfs_cheats(grid, start, end, target, m):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    max_x = len(grid[0]) - 1
    max_y = len(grid) - 1


    q = deque([])
    #     steps node path
    q.append((0, start))
    seen = set()

    ans = 0
    while q:
        steps, curr_node = q.popleft()
        seen.add(curr_node)
        if curr_node == end:
            continue
            # return steps, path
        for dx, dy in directions:
            nx = curr_node[0] + dx
            ny = curr_node[1] + dy
            sx = curr_node[0] + 2*dx
            sy = curr_node[1] + 2*dy
            if (nx, ny) not in seen and is_in_bounds((nx, ny), max_x, max_y) and grid[ny][nx] != '#':
                seen.add((nx, ny))
                q.append((steps + 1, (nx, ny)))
            elif is_in_bounds((sx, sy), max_x, max_y) and grid[sy][sx] != '#':
                if steps + 2 + m[(sx, sy)] <= target - z:
                    ans += 1


    return ans



def bfs_with_hacks(grid, start, end, max_steps):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    max_x = len(grid[0]) - 1
    max_y = len(grid) - 1


    q = deque([])
    #     steps node
    q.append((0, 1, start, set()))

    can_reach = False
    ans = 0
    anser = []
    t = 100
    while q:
        steps, hack, curr_node, seen = q.popleft()
        # print(steps, hack, curr_node, seen)
        # input()
        seen.add((curr_node[0], curr_node[1], hack))
        if curr_node == end:
            ans += 1
            anser.append(steps)
            if steps > max_steps - t + 1:
                return anser
            continue
        for dx, dy in directions:
            nx = curr_node[0] + dx
            ny = curr_node[1] + dy
            sx = curr_node[0] + 2*dx
            sy = curr_node[1] + 2*dy
            if (nx, ny, hack) not in seen and is_in_bounds((nx, ny), max_x, max_y) and grid[ny][nx] != '#':
                if steps + 1 <= max_steps - t + 1:
                    seen.add((nx, ny, hack))
                    q.append((steps + 1, hack, (nx, ny), seen))
                # else:
                #     print(steps + 1, max_steps, max_steps - t + 1)
            elif hack > 0 and (sx, sy, hack) not in seen and is_in_bounds((sx, sy), max_x, max_y) and grid[sy][sx] != '#':
                hack_set = seen.copy()
                if steps + 1 <= max_steps - t + 1:
                    hack_set.add((sx, sy, hack-1))
                    q.append((steps + 1, hack - 1, (sx, sy), hack_set))
                # else:
                #     print(steps + 1, max_steps, max_steps - t + 1)
    return anser


def part1b(lines):
    ans = 0
    start = None
    end = None

    for yi, line in enumerate(lines):
        for xi, ch in enumerate(line):
            if ch == 'S':
                start = (xi, yi)
            if ch == 'E':
                end = (xi,yi)
    grid_steps = bfs_from_end(lines, start, end)
    ans = bfs_cheats(lines, start, end, grid_steps[start], grid_steps)
    # ans = A_with_hacks2(lines, start, end, max_steps, set(golden_path))
    # ans = [max_steps - x  for x in ans if (max_steps - x ) >= z]
    # from collections import Counter
    # c = Counter(ans)
    # print(c)
    # print(len(ans))
    # ans = bfs_with_hacks(lines, start, end, max_steps)
    # ans = [max_steps - x - 1 for x in ans if (max_steps - x - 1) >= s]
    # from collections import Counter
    # c = Counter(ans)
    # print(c)
    # print(len(ans))

    return ans

def part1(lines):
    ans = 0
    print(lines)
    start = None
    end = None

    for yi, line in enumerate(lines):
        for xi, ch in enumerate(line):
            if ch == 'S':
                start = (xi, yi)
            if ch == 'E':
                end = (xi,yi)
    max_steps, golden_path = bfs(lines, start, end)
    print(start, end, max_steps, len(set(golden_path)))
    ans = A_with_hacks2(lines, start, end, max_steps, set(golden_path))
    ans = [max_steps - x  for x in ans if (max_steps - x ) >= z]
    from collections import Counter
    c = Counter(ans)
    print(c)
    print(len(ans))
    # ans = bfs_with_hacks(lines, start, end, max_steps)
    # ans = [max_steps - x - 1 for x in ans if (max_steps - x - 1) >= s]
    # from collections import Counter
    # c = Counter(ans)
    # print(c)
    # print(len(ans))

    return len(ans)

def bfs_cheats_2(grid, start, end, target, m):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    max_x = len(grid[0]) - 1
    max_y = len(grid) - 1


    q = deque([])
    #     steps node path
    q.append((0, start))
    seen = set()

    ans = 0
    while q:
        steps, curr_node = q.popleft()
        if m[curr_node] < z:
            break
        seen.add(curr_node)
        if curr_node == end:
            continue
            # return steps, path
        for dx, dy in directions:
            nx = curr_node[0] + dx
            ny = curr_node[1] + dy
            if (nx, ny) not in seen and is_in_bounds((nx, ny), max_x, max_y) and grid[ny][nx] != '#':
                seen.add((nx, ny))
                q.append((steps + 1, (nx, ny)))
            # mini bfs 20 squares from curr_node and do math
        mini_q = deque([])
        mini_seen = set()
        # mini_seen.add(curr_node)
        mini_q.append((0, curr_node))
        while mini_q:
            # print(len(mini_q))
            mini_steps, mini_curr = mini_q.popleft()
            if grid[mini_curr[1]][mini_curr[0]] != '#':
                if mini_steps + steps + m[mini_curr] <= target - z:
                    ans += 1
            mini_seen.add(mini_curr)
            if mini_steps + 1 <= 20:
                for dx, dy in directions:
                    minx = mini_curr[0] + dx
                    miny = mini_curr[1] + dy
                    if (minx, miny) not in mini_seen and is_in_bounds((minx, miny), max_x, max_y):
                        mini_q.append((mini_steps + 1, (minx, miny)))
                        mini_seen.add((minx, miny))



    return ans
# 863253 too low
# 903253 too low
# 1263253 too high
def part2(lines):
    ans = 0
    start = None
    end = None

    for yi, line in enumerate(lines):
        for xi, ch in enumerate(line):
            if ch == 'S':
                start = (xi, yi)
            if ch == 'E':
                end = (xi,yi)
    grid_steps = bfs_from_end(lines, start, end)
    ans = bfs_cheats_2(lines, start, end, grid_steps[start], grid_steps)
    # ans = A_with_hacks2(lines, start, end, max_steps, set(golden_path))
    # ans = [max_steps - x  for x in ans if (max_steps - x ) >= z]
    # from collections import Counter
    # c = Counter(ans)
    # print(c)
    # print(len(ans))
    # ans = bfs_with_hacks(lines, start, end, max_steps)
    # ans = [max_steps - x - 1 for x in ans if (max_steps - x - 1) >= s]
    # from collections import Counter
    # c = Counter(ans)
    # print(c)
    # print(len(ans))

    return ans


print("ans pt1:", part1b(i))
print("***********part 2***************")
print(part2(i))
