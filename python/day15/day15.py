import re
import sys
import heapq
import math
import time
import copy
from collections import deque, defaultdict, Counter

i = open("../../inputs/day15.txt").read().splitlines()



def is_in_bounds(point, max_x, max_y):
    return (0 <= point[0] <= max_x) and (0 <= point[1] <= max_y)


def is_int(a):
    b = math.floor(a + 0.5)
    # print(a, b, abs(a - b), sys.float_info.epsilon)
    return abs(a - b) < 0.001

grid = dict()
def dfs(point, direction, max_x, max_y):
    if not is_in_bounds(point, max_x, max_y) or grid[point] == '#':
        return 0
    if grid[(point)] == '.':
        return 1
    new_pt = (point[0] + direction[0], point[1] + direction[1])
    rtn = dfs(new_pt, direction, max_x, max_y)
    if rtn:
        grid[new_pt] = grid[point]
        grid[point] = '.'
    return rtn
def dfs2_no_move(points, direction, max_x, max_y):
    any_not_in_bounds = any(not is_in_bounds(point, max_x, max_y) for point in points)
    any_pound = any(grid[point] == '#' for point in points)
    all_dot = all(grid[point] == '.' for point in points)
    # print(points, any_not_in_bounds, any_pound, all_dot)
    if any_not_in_bounds or any_pound:
        return 0
    if all_dot:
        return 1
    p0 = points[0]
    # is_at = len(points) == 1 and grid[p0[1][p0[0]]] == '@'
    move_dir_1 = ()
    move_dir_2 = None
    l = []
    if len(points) == 1:
        if direction == (1, 0) or direction == (-1, 0):
            c_p = (p0[0] + direction[0], p0[1] + direction[1])

            while grid[c_p] in ["[", "]"]:
                l.append(c_p)
                c_p = (c_p[0] + direction[0], c_p[1] + direction[1])
            rtn = dfs2([c_p], direction, max_x, max_y)


            # move_dir_1 = (p0[0] + direction[0], p0[1] + direction[1])
            # print(move_dir_1)
            # if grid[(move_dir_1[0], move_dir_1[1])] in ["[", "]"]:
            #     move_dir_2 = (p0[0] + 2*direction[0], p0[1] + 2*direction[1])
        elif direction == (0, 1) or direction == (0, -1):
            move_dir_1 = (p0[0] + direction[0], p0[1] + direction[1])
            if grid[(move_dir_1[0], move_dir_1[1])] == "[":
                move_dir_2 = (p0[0] + 1, p0[1] + direction[1])
            elif grid[(move_dir_1[0], move_dir_1[1])] == "]":
                move_dir_2 = (p0[0] - 1, p0[1] + direction[1])
            if not move_dir_2:
                rtn = dfs2([move_dir_1], direction, max_x, max_y)
            else:
                next_dir_1 = (move_dir_1[0] + direction[0], move_dir_1[1] + direction[1])
                next_dir_2 = (move_dir_2[0] + direction[0], move_dir_2[1] + direction[1])
                while grid[move_dir_1] == grid[next_dir_1] and grid[move_dir_2] == grid[next_dir_2]:
                    l.append(next_dir_1)
                    l.append(next_dir_2)
                    next_dir_1 = (next_dir_1[0] + direction[0], next_dir_1[1] + direction[1])
                    next_dir_2 = (next_dir_2[0] + direction[0], next_dir_2[1] + direction[1])
                rtn = dfs2([next_dir_1], direction, max_x, max_y) * dfs2([next_dir_2], direction, max_x, max_y)


        # elif direction == (0, -1):
        #     move_dir_1 = (p0[0] + direction[0], p0[1] + direction[1])
        #     if grid[(move_dir_1[0], move_dir_1[1])] == "[":
        #         move_dir_2 = (p0[0] + 1, p0[1] + direction[1])
        #     elif grid[(move_dir_1[0], move_dir_1[1])] == "]":
        #         move_dir_2 = (p0[0] - 1, p0[1] + direction[1])

        # if move_dir_2:
        #     n = [move_dir_2, move_dir_1]
        # else:
        #     n = [move_dir_1]
    else:
        print("HSOULD NEVER BE HERE")
        if direction == (1, 0) or direction == (-1, 0):
            move_dir_1 = (p0[0] + direction[0], p0[1] + direction[1])
            move_dir_2 = (points[1][0] + direction[0], points[1][1] + direction[1])
            n = [move_dir_2, move_dir_1]
            n = [x for x in n if x not in points]
        else:
            move_dir_1 = (p0[0] + direction[0], p0[1] + direction[1])
            if grid[p0] == "[" and grid[move_dir_1] == "]":
                return 0
            if grid[p0] == "]" and grid[move_dir_1] == "[":
                return 0
            move_dir_2 = (points[1][0] + direction[0], points[1][1] + direction[1])
            if grid[points[1]] == "[" and grid[move_dir_2] == "]":
                return 0
            if grid[points[1]] == "]" and grid[move_dir_2] == "[":
                return 0
            n = [move_dir_2, move_dir_1]

    return rtn

def dfs2(points, direction, max_x, max_y):
    any_not_in_bounds = any(not is_in_bounds(point, max_x, max_y) for point in points)
    any_pound = any(grid[point] == '#' for point in points)
    all_dot = all(grid[point] == '.' for point in points)
    # print(points, any_not_in_bounds, any_pound, all_dot)
    if any_not_in_bounds or any_pound:
        return 0
    if all_dot:
        return 1
    p0 = points[0]
    # is_at = len(points) == 1 and grid[p0[1][p0[0]]] == '@'
    move_dir_1 = ()
    move_dir_2 = None
    l = []
    if direction == (1, 0) or direction == (-1, 0):
        c_p = (p0[0] + direction[0], p0[1] + direction[1])

        while grid[c_p] in ["[", "]"]:
            l.append(c_p)
            c_p = (c_p[0] + direction[0], c_p[1] + direction[1])
        rtn = dfs2([c_p], direction, max_x, max_y)

    elif direction == (0, 1) or direction == (0, -1):
        move_dir_1 = (p0[0] + direction[0], p0[1] + direction[1])
        if grid[(move_dir_1[0], move_dir_1[1])] == "[":
            l.append(move_dir_1)
            move_dir_2 = (p0[0] + 1, p0[1] + direction[1])
        elif grid[(move_dir_1[0], move_dir_1[1])] == "]":
            l.append(move_dir_1)
            move_dir_2 = (p0[0] - 1, p0[1] + direction[1])
        if not move_dir_2:
            rtn = dfs2([move_dir_1], direction, max_x, max_y)
        else:
            l.append(move_dir_2)
            # print(move_dir_1, move_dir_2)
            next_dir_1 = (move_dir_1[0] + direction[0], move_dir_1[1] + direction[1])
            next_dir_2 = (move_dir_2[0] + direction[0], move_dir_2[1] + direction[1])
            while grid[move_dir_1] == grid[next_dir_1] and grid[move_dir_2] == grid[next_dir_2]:
                # print(next_dir_1, next_dir_2)
                # input()
                l.append(next_dir_1)
                l.append(next_dir_2)
                next_dir_1 = (next_dir_1[0] + direction[0], next_dir_1[1] + direction[1])
                next_dir_2 = (next_dir_2[0] + direction[0], next_dir_2[1] + direction[1])
            rtn1 = 1
            rtn2 = 1
            if grid[next_dir_1] == "]" and grid[move_dir_1] == "[":
                tmp = (next_dir_1[0] - 1, next_dir_1[1])
                l.append(tmp)
                rtn1 = dfs2_no_move([next_dir_1], direction, max_x, max_y) * dfs2_no_move([tmp], direction, max_x, max_y)
            elif grid[next_dir_1] == "[" and grid[move_dir_1] == "]":
                tmp = (next_dir_1[0] + 1, next_dir_1[1])
                l.append(tmp)
                rtn1 = dfs2_no_move([next_dir_1], direction, max_x, max_y) * dfs2_no_move([tmp], direction, max_x, max_y)
            else:
                rtn1 = dfs2_no_move([next_dir_1], direction, max_x, max_y)
            if grid[next_dir_2] == "]" and grid[move_dir_2] == "[":
                tmp = (next_dir_2[0] - 1, next_dir_2[1])
                l.append(tmp)
                rtn2 = dfs2_no_move([next_dir_2], direction, max_x, max_y) * dfs2_no_move([tmp], direction, max_x, max_y)
            elif grid[next_dir_2] == "[" and grid[move_dir_2] == "]":
                tmp = (next_dir_1[0] + 1, next_dir_2[1])
                l.append(tmp)
                rtn2 = dfs2_no_move([next_dir_2], direction, max_x, max_y) * dfs2_no_move([tmp], direction, max_x, max_y)
            else:
                rtn2 = dfs2_no_move([next_dir_2], direction, max_x, max_y)


            rtn = rtn1 * rtn2
            if rtn:
                if grid[next_dir_1] == "]" and grid[move_dir_1] == "[":
                    tmp = (next_dir_1[0] - 1, next_dir_1[1])
                    rtn1 = dfs2([next_dir_1], direction, max_x, max_y) * dfs2([tmp], direction, max_x, max_y)
                elif grid[next_dir_1] == "[" and grid[move_dir_1] == "]":
                    tmp = (next_dir_1[0] + 1, next_dir_1[1])
                    rtn1 = dfs2([next_dir_1], direction, max_x, max_y) * dfs2([tmp], direction, max_x, max_y)
                else:
                    rtn1 = dfs2([next_dir_1], direction, max_x, max_y)
                if grid[next_dir_2] == "]" and grid[move_dir_2] == "[":
                    tmp = (next_dir_2[0] - 1, next_dir_2[1])
                    rtn2 = dfs2([next_dir_2], direction, max_x, max_y) * dfs2([tmp], direction, max_x, max_y)
                elif grid[next_dir_2] == "[" and grid[move_dir_2] == "]":
                    tmp = (next_dir_2[0] + 1, next_dir_2[1])
                    rtn2 = dfs2([next_dir_2], direction, max_x, max_y) * dfs2([tmp], direction, max_x, max_y)
                else:
                    rtn2 = dfs2([next_dir_2], direction, max_x, max_y)

                # dfs2([next_dir_1], direction, max_x, max_y) 
                # dfs2([next_dir_2], direction, max_x, max_y)



        # elif direction == (0, -1):
        #     move_dir_1 = (p0[0] + direction[0], p0[1] + direction[1])
        #     if grid[(move_dir_1[0], move_dir_1[1])] == "[":
        #         move_dir_2 = (p0[0] + 1, p0[1] + direction[1])
        #     elif grid[(move_dir_1[0], move_dir_1[1])] == "]":
        #         move_dir_2 = (p0[0] - 1, p0[1] + direction[1])

        # if move_dir_2:
        #     n = [move_dir_2, move_dir_1]
        # else:
        #     n = [move_dir_1]
    if rtn:
        for point in l[::-1]:
            # print(f"moving point {point} in l")
            # print_grid(max_x, max_y)
            new_pt = (point[0] + direction[0], point[1] + direction[1])
            if grid[point] != '.':
                grid[new_pt] = grid[point]
                grid[point] = '.'
            # print_grid(max_x, max_y)

        c_p = (p0[0] + direction[0], p0[1] + direction[1])
        # print(f"moving c_p {c_p}")
        # print_grid(max_x, max_y)
        if grid[points[0]] != '.':
            grid[c_p] = grid[points[0]] 
            grid[points[0]] = '.' 
        # print_grid(max_x, max_y)

    return rtn

def print_grid(max_x, max_y):
    l = [['.']*(max_x + 1) for y in range(max_y + 1)]
    # print(l)
    for k, v in grid.items():
        l[k[1]][k[0]] = v
    for row in l:
        print(''.join(row))
def invrt():
    for k, v in grid.items():
        if v == '[' and grid[(k[0] + 1, k[1])] != ']':
            return False
    return True

def print_gridc(c, max_x, max_y):
    l = [['.']*(max_x + 1) for y in range(max_y + 1)]
    # print(l)
    for k, v in c.items():
        l[k[1]][k[0]] = v
    for row in l:
        print(''.join(row))
def part1(lines):
    ans = 0
    directions = {
        ">": (1, 0),
        "<": (-1, 0),
        "^": (0, -1),
        "v": (0, 1),
    }
    max_x = 0
    max_y = 0
    moves = []
    cur_pos = (0, 0)
    for yi, line in enumerate(lines):
        move = []
        for xi, ch in enumerate(line):
            if ch == '@':
                cur_pos = (xi, yi)
            if line and line[0] == "#":
                grid[(xi, yi)] = ch
                max_x = max(max_x, xi)
                max_y = max(max_y, yi)
            elif line and line[0] in directions.keys():
                move.append(ch)
        if move:
            moves.extend(move)
    print(cur_pos)

    for move in moves:
        # print_grid(max_x, max_y)
        dx, dy = directions[move]

        has_moved = dfs(cur_pos, directions[move], max_x, max_y)
        if has_moved:
            cur_pos = (cur_pos[0] + dx, cur_pos[1] + dy)
    # print_grid(max_x, max_y)
    print(cur_pos)
    for k, v in grid.items():
        if v == "O":
            ans += k[0]  + k[1] * 100



    return ans


# 1435520 too low
def part2(lines):
    ans = 0
    directions = {
        ">": (1, 0),
        "<": (-1, 0),
        "^": (0, -1),
        "v": (0, 1),
    }
    max_x = 0
    max_y = 0
    moves = []
    cur_pos = (0, 0)
    y_carry = 0
    for yi, line in enumerate(lines):
        x_carry = 0
        move = []
        for xi, ch in enumerate(line):
            if ch == '@':
                cur_pos = (xi+x_carry, yi)
            if line and line[0] == "#":
                if ch == "#":
                    grid[(xi+x_carry, yi + y_carry)] = ch
                    grid[(xi+x_carry +1, yi + y_carry)] = ch
                elif ch == "O":
                    grid[(xi+x_carry, yi + y_carry)] = "["
                    grid[(xi+x_carry +1, yi + y_carry)] = "]"
                elif ch == ".":
                    grid[(xi+x_carry, yi + y_carry)] = ch
                    grid[(xi+x_carry +1, yi + y_carry)] = ch
                elif ch == "@":
                    grid[(xi+x_carry, yi + y_carry)] = ch
                    grid[(xi+x_carry +1, yi + y_carry)] = "."
                x_carry += 1
                max_x = max(max_x, xi + x_carry)
                max_y = max(max_y, yi)
            elif line and line[0] in directions.keys():
                move.append(ch)
        if move:
            moves.extend(move)
    mx = 0
    my = 0
    for k, v in grid.items():
        mx = max(mx, k[0])
        my = max(my, k[1])


    for move in moves:
        # print_grid(max_x, max_y)
        dx, dy = directions[move]
        pre_move = copy.deepcopy(grid)

        has_moved = dfs2([cur_pos], directions[move], max_x, max_y)
        if has_moved:
            cur_pos = (cur_pos[0] + dx, cur_pos[1] + dy)
            if not invrt():
                print(f"{move} took us from, {cur_pos}")
                print_gridc(pre_move, max_x, max_y)
                print_grid(max_x, max_y)
                input()
        # input()
    # print(" final print grid")
    print_grid(max_x, max_y)
    # print(cur_pos)
    for k, v in grid.items():
        if v == "[":
            ans += k[0]  + k[1] * 100



    return ans


# print("ans pt1:", part1(i))
grid = dict()
print("***********part 2***************")
print(part2(i))
