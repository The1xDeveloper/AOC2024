import re
import sys
import heapq
import math
import time
from collections import deque, defaultdict, Counter

i = open("../../inputs/day17.txt").read().splitlines()


def is_in_bounds(point, max_x, max_y):
    return (0 <= point[0] <= max_x) and (0 <= point[1] <= max_y)


def is_int(a):
    b = math.floor(a + 0.5)
    # print(a, b, abs(a - b), sys.float_info.epsilon)
    return abs(a - b) < 0.001

def get_combo_operand(operand, A, B, C) -> int:
    assert operand != 7
    if operand in [0, 1, 2, 3]:
        return operand
    if operand == 4:
        return A
    if operand == 5:
        return B
    if operand == 6:
        return C
    return -1
def part1(lines):
    A = 0
    B = 0
    C = 0
    program = []

    ans = 0
    for yi, line in enumerate(lines):
        if line.startswith("Register A"):
            A = int(line.split(":")[-1])
        if line.startswith("Register B"):
            B = int(line.split(":")[-1])
        if line.startswith("Register C"):
            C = int(line.split(":")[-1])
        if line.startswith("Program"):
            program = [int(x) for x in line.split(":")[-1].split(",")]
        

    i = 0
    print(A, B, C)
    print(program)
    max_i = len(program)
    outputs = []
    while i < max_i - 1:
        opcode = program[i]
        operand = program[i+1]
        # print(i, opcode, operand, A, B, C)
        # input()

        if opcode == 0:
            num = A
            comb = get_combo_operand(operand, A, B, C)
            den = 2**comb
            A = num//den
        if opcode == 1:
            B = B ^ operand
        if opcode == 2:
            B = get_combo_operand(operand, A, B, C) % 8
            assert B != -1
        if opcode == 3:
            if A != 0:
                i = operand
                continue
        if opcode == 4:
            B = B ^ C
        if opcode == 5:
            t = get_combo_operand(operand, A, B, C) % 8
            outputs.append(t)
        if opcode == 6:
            num = A
            comb = get_combo_operand(operand, A, B, C)
            den = 2**comb
            B = num//den
        if opcode == 7:
            num = A
            comb = get_combo_operand(operand, A, B, C)
            den = 2**comb
            C = num//den
        i += 2



    print(','.join([str(x) for x in outputs]))


    return ans

def play(program, left, ans: int):
    if not left:
        return ans
    max_i = len(program)
    A = 0
    B = 0
    C = 0

    for t in range(8):
        output = 0
        tmp = ans << 3 | t
        A = ans << 3 | t
        i = 0
        while i < max_i - 1:
            opcode = program[i]
            operand = program[i+1]

            if opcode == 0:
                num = A
                comb = get_combo_operand(operand, A, B, C)
                den = 2**comb
                A = num//den
            if opcode == 1:
                B = B ^ operand
            if opcode == 2:
                B = get_combo_operand(operand, A, B, C) % 8
                assert B != -1
            if opcode == 3:
                if A != 0:
                    i = operand
                    continue
            if opcode == 4:
                B = B ^ C
            if opcode == 5:
                t = get_combo_operand(operand, A, B, C) % 8
                output = t
                break
                # outputs.append(t)
            if opcode == 6:
                num = A
                comb = get_combo_operand(operand, A, B, C)
                den = 2**comb
                B = num//den
            if opcode == 7:
                num = A
                comb = get_combo_operand(operand, A, B, C)
                den = 2**comb
                C = num//den
            i += 2
        if output == left[-1]:
            sub = play(program, left[:-1], tmp)
            if sub is None: continue
            return sub

def part2(lines):
    program = []

    for yi, line in enumerate(lines):
        if line.startswith("Register A"):
            A = int(line.split(":")[-1])
        if line.startswith("Register B"):
            B = int(line.split(":")[-1])
        if line.startswith("Register C"):
            C = int(line.split(":")[-1])
        if line.startswith("Program"):
            program = [int(x) for x in line.split(":")[-1].split(",")]
        
    return play(program, program, 0)



print("ans pt1:", part1(i))
print("***********part 2***************")
print(part2(i))
