import re
import sys
import heapq
import math
import time
from collections import deque, defaultdict, Counter

max_x = 101
max_y = 103
# max_x = 11
# max_y = 7
input = open("../../inputs/day14.txt").read().splitlines()


def is_in_bounds(point, max_x, max_y):
    return (0 <= point[0] <= max_x) and (0 <= point[1] <= max_y)


def is_int(a):
    b = math.floor(a + 0.5)
    # print(a, b, abs(a - b), sys.float_info.epsilon)
    return abs(a - b) < 0.001


# too low... 211692000
# 218695680 too high
def part1(lines):
    ans = 0
    x_mid = int(max_x // 2)
    y_mid = int(max_y // 2)
    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0
    for yi, line in enumerate(lines):
        print(line)
        pos, vel = line.split(" ")
        pos = pos.split("=")[-1].split(",")
        x_pos = int(pos[0])
        y_pos = int(pos[1])
        vel = vel.split("=")[-1].split(",")
        x_vel = int(vel[0])
        y_vel = int(vel[1])
        print(x_pos, y_pos, x_vel, y_vel)
        # print(x_vel, y_vel)
        # x_pos = 100
        # y_pos = 102
        # x_vel = 1
        # y_vel = 1
        new_x = (x_pos + 100 * x_vel) % (max_x)
        new_y = (y_pos + 100 * y_vel) % (max_y)
        # print(new_x, new_y)

        if new_y == y_mid or new_x == x_mid:
            # print(new_x, new_y)
            pass
        elif new_y < y_mid and new_x < x_mid:
            q1 += 1
        elif new_y < y_mid and new_x > x_mid:
            q2 += 1
        elif new_y > y_mid and new_x < x_mid:
            q3 += 1
        elif new_y > y_mid and new_x > x_mid:
            q4 += 1
        else:
            print("never should be here", new_x, new_y)
            pass
    print(q1, q2, q3, q4)

    return q1 * q2 * q3 * q4


def part2(lines):
    ans = 0
    x_mid = int(max_x // 2)
    y_mid = int(max_y // 2)
    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0
    # 5000 too low
    a = False
    for i in range(0, 10000):
        new_grid = [["." for _ in range(max_x)] for _ in range(max_y)]
        points = []
        for yi, line in enumerate(lines):
            # print(line)
            pos, vel = line.split(" ")
            pos = pos.split("=")[-1].split(",")
            x_pos = int(pos[0])
            y_pos = int(pos[1])
            vel = vel.split("=")[-1].split(",")
            x_vel = int(vel[0])
            y_vel = int(vel[1])
            # print(x_pos, y_pos, x_vel, y_vel)
            # print(x_vel, y_vel)
            # x_pos = 100
            # y_pos = 102
            # x_vel = 1
            # y_vel = 1
            new_x = (x_pos + i * x_vel) % (max_x)
            new_y = (y_pos + i * y_vel) % (max_y)
            points.append((new_x, new_y))
            # print(new_x, new_y)

            new_grid[new_y][new_x] = "#"

        # Did not originally ahve this idea, originally "binary searched" via the answer box 5000 (too low), 10000 (too high), 7500 (too high) and sat watching the if a == True and waiting till I saw it
        # Added this check after looking at solution thread and people saying this was a good check
        if len(points) == len(set(points)):
            print("=================")
            print(f"i = {i}")
            for row in new_grid:
                print("".join(row))
            print("=================")

            #
        if a == True:
            print("=================")
            print(f"i = {i}")
            for row in new_grid:
                print("".join(row))
            print("=================")
            time.sleep(0.3)

    return 0


print("ans pt1:", part1(input))
print("***********part 2***************")
print(part2(input))
