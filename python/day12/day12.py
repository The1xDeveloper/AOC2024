import re
import heapq
from collections import deque, defaultdict, Counter


input = open("../../inputs/day12.test").read().splitlines()


def is_in_bounds(point, max_x, max_y):
    return (0 <= point[0] <= max_x) and (0 <= point[1] <= max_y)


def part1(lines):
    ans = 0
    seen = set()
    directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    max_x = len(lines[0]) - 1
    max_y = len(lines) - 1
    l = []
    for yi, line in enumerate(lines):
        for xi, chr in enumerate(line):
            if (xi, yi) in seen:
                continue
            target = lines[yi][xi]
            seen.add((xi, yi))
            q = deque([(xi, yi)])
            perim = 0
            area = 0
            while q:
                cx, cy = q.popleft()
                area += 1

                l_p = 4
                for dx, dy in directions:
                    px = cx + dx
                    py = cy + dy
                    if is_in_bounds((px, py), max_x, max_y) and lines[py][px] == target:
                        l_p -= 1
                        if (px, py) not in seen:
                            seen.add((px, py))
                            q.append((px, py))
                perim += l_p

            l.append(perim * area)
    return sum(l)


def part2(lines):
    ans = 0
    seen = set()
    directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    diags = [(-1, 1), (-1, -1), (1, 1), (1, -1)]
    max_x = len(lines[0]) - 1
    max_y = len(lines) - 1
    l = []
    for yi, line in enumerate(lines):
        for xi, chr in enumerate(line):
            if (xi, yi) in seen:
                continue
            target = lines[yi][xi]
            seen.add((xi, yi))
            q = deque([(xi, yi)])
            area = 0
            start = (0, 0)
            y_to_x = defaultdict(set)
            x_to_y = defaultdict(set)
            point_count = defaultdict(int)
            corners = 0
            f = set()
            c = 0
            points = set()
            while q:
                cx, cy = q.popleft()
                points.add((cx, cy))
                area += 1
                # graveyard of failed ideas
                # all ideas around the concept the edges == vertexes
                # tried to get by looking at "diags" and adding/subtracting potential
                # corners
                for dx, dy in diags:
                    px = cx + dx
                    py = cy + dy
                    if (px, py) in f:  # or (
                        # is_in_bounds((px, py), max_x, max_y) and lines[py][px] == target
                        # ):
                        c -= 1
                    else:
                        c += 1
                    f.add((px, py))

                    # if not is_in_bounds((px, py), max_x, max_y):
                    #     c += 1
                    # elif lines[py][px] != target:
                    #     c += 1
                # c here was some attempt at counting if we are either a corner edge out alone
                # or of we are an inner corner edge
                if c == 1 or c == 3:
                    corners += 1

                # attempted to line up the x's and y's fixed and travel along the horiz or vert line
                # counting contiguous edges, each would represent an edge. But failed on A A A A
                # couldnt figure out how to discount the x = 1, 2, 3 and respective y = 0 for each counting
                # as an edge, tried playing around with if I had > 1 el but that fails below:
                # A
                # A
                # for dx, dy in directions:
                #     px = cx + dx
                #     py = cy + dy
                #     if px in y_to_x[py]:
                #         y_to_x[py].remove(px)
                #     else:
                #         y_to_x[py].add(px)
                #     if py in x_to_y[px]:
                #         x_to_y[px].remove(py)
                #     else:
                #         x_to_y[px].add(py)
                #     if is_in_bounds((px, py), max_x, max_y) and lines[py][px] == target:
                #         if (px, py) not in seen:
                #             seen.add((px, py))
                #             q.append((px, py))
                for dx, dy in directions:
                    px = cx + dx
                    py = cy + dy
                    if dx == 0 and not ((0 <= py <= max_y) and lines[py][px] == target):
                        y_to_x[py].add(px)
                    elif (
                        not ((0 <= px <= max_x) and lines[py][px] == target) and dy == 0
                    ):
                        x_to_y[px].add(py)
                    if is_in_bounds((px, py), max_x, max_y) and lines[py][px] == target:
                        if (px, py) not in seen:
                            seen.add((px, py))
                            q.append((px, py))
            sides = 0
            print(y_to_x)
            print(x_to_y)
            for y, xs in y_to_x.items():
                # if y == yi or len(xs) <= 1:
                #     continue
                # print(y, xs)
                for x in xs:
                    if x + 1 not in xs:
                        sides += 1
            print("***")
            for x, ys in x_to_y.items():
                # if x == xi or len(ys) == 1:
                #     continue
                # print(x, ys)
                for y in ys:
                    if y + 1 not in ys:
                        sides += 1
            # verts = sum(1 for x in point_count.values() if x == 1)

            # print(c, area)
            corners = 0
            # finally an idea worked, just do all the cornering tests....
            for point in points:
                x = point[0]
                y = point[1]
                left_and_up = (x - 1, y) not in points and (x, y - 1) not in points
                left_up_diag = (
                    (x - 1, y) in points
                    and (x, y - 1) in points
                    and (x - 1, y - 1) not in points
                )
                left_and_down = (x - 1, y) not in points and (x, y + 1) not in points
                left_down_diag = (
                    (x - 1, y) in points
                    and (x, y + 1) in points
                    and (x - 1, y + 1) not in points
                )
                right_and_up = (x + 1, y) not in points and (x, y - 1) not in points
                right_up_diag = (
                    (x + 1, y) in points
                    and (x, y - 1) in points
                    and (x + 1, y - 1) not in points
                )
                right_and_down = (x + 1, y) not in points and (x, y + 1) not in points
                right_down_diag = (
                    (x + 1, y) in points
                    and (x, y + 1) in points
                    and (x + 1, y + 1) not in points
                )
                corners += (
                    left_and_up
                    + left_up_diag
                    + left_and_down
                    + left_down_diag
                    + right_and_up
                    + right_up_diag
                    + right_and_down
                    + right_down_diag
                )

            print(target, sides, corners)
            l.append(sides * area)
    return sum(l)


print("ans pt1:", part1(input))
print("***********part 2***************")
print(part2(input))
