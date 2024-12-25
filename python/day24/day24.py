import re
import sys
import heapq
import math
import time
from collections import deque, defaultdict, Counter
from functools import cache
from itertools import combinations

sys.setrecursionlimit(100000)
i = open("../../inputs/day24.txt").read().splitlines()


def manhat(curr, end):
    return abs(curr[0] - end[0]) + abs(curr[1] - end[1])


def is_in_bounds(point, max_x, max_y):
    return (0 <= point[0] <= max_x) and (0 <= point[1] <= max_y)


def is_int(a):
    b = math.floor(a + 0.5)
    # print(a, b, abs(a - b), sys.float_info.epsilon)
    return abs(a - b) < 0.001


def part1(lines):
    m = defaultdict(int)
    ans = 0
    games = defaultdict(tuple)
    adj = defaultdict(set)
    in_degrees = defaultdict(int)
    for yi, line in enumerate(lines):
        if ":" in line:
            key, num = line.split(":")
            num = int(num)
            m[key] = num
        elif line == "\n":
            continue
        elif "->" in line:
            game, result = line.split("->")
            a, op, b = game.split()
            a = a.strip()
            op = op.strip()
            b = b.strip()
            result = result.strip()
            games[result] = (a, b, op)
            adj[result].add(a)
            adj[result].add(b)
            adj[a].add(result)
            adj[b].add(result)
            in_degrees[result] = 2
            if a in m:
                in_degrees[result] -= 1
            if b in m:
                in_degrees[result] -= 1
    zero_in = [k for k, v in in_degrees.items() if v == 0]
    while zero_in:
        new_zero = []
        for z in zero_in:
            a, b, op = games[z]
            # print(a, b, op)
            r = 0
            if op == "AND":
                r = m[a] & m[b]
            if op == "OR":
                r = m[a] | m[b]
            if op == "XOR":
                r = m[a] ^ m[b]
            m[z] = r
            for nei in adj[z]:
                in_degrees[nei] -= 1
                if in_degrees[nei] == 0:
                    new_zero.append(nei)
        zero_in = new_zero

    zs = sorted([(k, v) for k, v in m.items() if k.startswith("z")], reverse=True)
    ans = 0
    for z in zs:
        ans = ans << 1
        ans = ans + z[1]

    return ans


def part2(lines):
    # print(m["z18"])
    # print(m["sgq"])
    # print(m["scq"], m["kfp"])
    # print(m["hbs"], m["gpk"], m["z10"], m["csk"])
    # print(m["vmg"], m["z19"], m["bng"], m["dhq"], m["qdb"])
    # print(m["jdm"], m["pdg"], m["gkg"])
    # print(m["cnr"])
    # wrong 'ckj,fwt,gpk,jcp,jpm,scq,z18,z27'
    # trying ckj,fwt,hbs,jcp,jpm,scq,z18,z27
    # wrong 'ckj,fwt,hbs,jcp,jpm,scq,z18,z27'

    golden_combos = [
        ("z18", "hbs"),
        ("kfp", "z22"),
        ("z27", "jcp"),
        ("dhq", "pdg"),
    ]
    all_wires = list()
    for line in lines:
        if "->" in line:
            wire = line.split("->")[-1].strip()
            all_wires.append(wire)
    print(all_wires)

    swap_pool = [
        "z18",
        "hbs",
        "kfp",
        "z22",
        "z27",
        "jcp",
        "dhq",
        "pdg",
    ]
    # "z18"
    # "scq" or "kfp"
    # "hbs" or "gpk" or ("z10" and "csk")
    # "frm" or ("z11" and "btr")
    # "ftw" ("z19" and "bng") or ** no ("dhq" and "qdb") ** or  "vmg"
    # "cjk" or ("z28" and "dwb") or "qjd"
    # ("vhg" and "z29") or "psk"
    # "jdm" or *("pdg" and "gkg")
    # "cnr"
    two_combos = combinations(swap_pool, 2)
    two_combo_valid = set()
    for cw in two_combos:
        two_combo_valid.add(cw)
    #     if cw[0] == "z10" and cw[1] != "csk":
    #         continue
    #     if cw[1] == "z10" and cw[0] != "csk":
    #         continue
    #     if cw[0] == "z11" and cw[1] != "btr":
    #         continue
    #     if cw[1] == "z11" and cw[0] != "btr":
    #         continue
    #     if cw[0] == "z19" and cw[1] != "bng":
    #         continue
    #     if cw[1] == "z19" and cw[0] != "bng":
    #         continue
    #     if cw[0] == "z10" and cw[1] != "csk":
    #         continue
    #     if cw[1] == "z10" and cw[0] != "csk":
    #         continue
    #     if cw[0] == "dhq" and cw[1] != "qdb":
    #         continue
    #     if cw[1] == "dhq" and cw[0] != "qdb":
    #         continue
    #     if cw[0] == "pdg" and cw[1] != "gkg":
    #         continue
    #     if cw[1] == "pdg" and cw[0] != "gkg":
    #         continue
    #     if cw[0] == "z28" and cw[1] != "dwb":
    #         continue
    #     if cw[1] == "z28" and cw[0] != "dwb":
    #         continue
    #     if cw[0] == "z29" and cw[1] != "vhg":
    #         continue
    #     if cw[1] == "z29" and cw[0] != "vhg":
    #         continue
    #
    # print(len(two_combo_valid))
    # print(two_combo_valid)
    four_combos = combinations(two_combo_valid, 4)
    tracker = 0
    timer = time.time()
    for combo in four_combos:
        # for try_this_wire in all_wires:
        # if try_this_wire.startswith("z"):
        #     continue
        # in_this_set = set([x for y in golden_combos for x in y if x != "xxx"])
        # in_this_set.add(try_this_wire)
        # if len(in_this_set) != 8:
        #     continue
        # this_run_golen = []
        # for gdn in golden_combos:
        #     if gdn[1] == "xxx":
        #         this_run_golen.append((gdn[0], try_this_wire))
        #     else:
        #         this_run_golen.append((gdn[0], gdn[1]))
        tracker += 1
        tmp = set([x for xx in combo for x in xx])
        if len(tmp) != 8:
            continue
        if tracker % 10000 == 0 and tracker >= 10000:
            print("on: ", tracker, "took: ", time.time() - timer)
            timer = time.time()
        m = defaultdict(int)
        ans = 0
        games = defaultdict(tuple)
        adj = defaultdict(set)
        in_degrees = defaultdict(int)
        backwards = defaultdict(set)
        o_wires = set()
        x_num = 0
        xidx = 0
        y_num = 0
        yidx = 0
        failed_run = False
        for yi, line in enumerate(lines):
            if ":" in line:
                key, num = line.split(":")
                num = int(num)
                m[key] = num
                if key.startswith("y"):
                    to_add = num << yidx
                    y_num = y_num | to_add
                    yidx += 1
                if key.startswith("x"):
                    to_add = num << xidx
                    x_num = x_num | to_add
                    xidx += 1
            elif line == "\n":
                continue
            elif "->" in line:
                game, result = line.split("->")
                a, op, b = game.split()
                a = a.strip()
                op = op.strip()
                b = b.strip()
                result = result.strip()
                for cmbo in combo:
                    l = []
                    if result in cmbo:
                        for ee in cmbo:
                            if ee != result:
                                l.append(ee)
                        result = l[0]
                games[result] = (a, b, op)
                adj[result].add(a)
                adj[result].add(b)
                backwards[result].add(a)
                backwards[result].add(b)
                adj[a].add(result)
                adj[b].add(result)
                o_wires.add(result)
                in_degrees[result] = 2
                if a in m:
                    in_degrees[result] -= 1
                if b in m:
                    in_degrees[result] -= 1
        zero_in = [k for k, v in in_degrees.items() if v == 0]
        # print(bin(x_num))
        # print(bin(y_num))
        comboo = bin(x_num + y_num)[2:]
        # print(combo)
        # input()
        known_z = defaultdict(int)
        for i, l in enumerate(comboo[::-1]):
            zid = f"z{i:02}"
            known_z[zid] = int(l)

        c = 0
        z_in_size = []
        zeros = defaultdict(list)
        idx = 0
        in_copy = in_degrees.copy()
        while zero_in:
            z_in_size.append(len(zero_in))
            zeros[idx].extend(zero_in)
            new_zero = []
            # print(zero_in)
            # input()
            for z in zero_in:
                a, b, op = games[z]
                # print(a, b, op)
                r = 0
                if op == "AND":
                    r = m[a] & m[b]
                if op == "OR":
                    r = m[a] | m[b]
                if op == "XOR":
                    r = m[a] ^ m[b]
                # if z == "qgt" or z == "gwq":
                #     print(z, a, m[a], b, m[b], op, r)
                #     input()
                if z in known_z.keys():
                    if known_z[z] != r:
                        failed_run = True
                        break
                m[z] = r
                for nei in adj[z]:
                    in_copy[nei] -= 1
                    if in_copy[nei] == 0:
                        new_zero.append(nei)
            if failed_run:
                break
            zero_in = new_zero
            c += 1
            idx += 1

        if failed_run:
            continue
        kkeys = []
        for k, v in known_z.items():
            kkeys.append(k)
        kkeys.sort()
        if all(known_z[k] == m[k] for k in kkeys):
            print("winner")
            print(combo)
            wires_used = sorted([y for x in combo for y in x])
            print(",".join(wires_used))
            input()

    return 0
    # "z18"
    # "sgq"
    # "scq" or "kfp"
    # "hbs" or "gpk" or ("z10" and "csk")
    # ("z19" and "bng") or ("dhq" and "qdb") or  "vmg"
    # "jdm" or *("pdg" and "gkg")
    # "cnr"
    print(m["z18"])
    print(m["sgq"])
    print(m["scq"], m["kfp"])
    print(m["hbs"], m["gpk"], m["z10"], m["csk"])
    print(m["vmg"], m["z19"], m["bng"], m["dhq"], m["qdb"])
    print(m["jdm"], m["pdg"], m["gkg"])
    print(m["cnr"])
    input()
    filtered = {k: v for k, v in zeros.items() if len(v) > 0}
    print([len(x) for k, x in filtered.items()])
    for k, v in filtered.items():
        print(len(v), v)
        if len(v) > 10:
            continue
        for mm in v:
            if mm.startswith("z"):
                print(combo)
                print(str(combo)[::-1][int(mm[1:])])
                # print(combo[int(mm[1:])])
        for mm in v:
            print(mm, games[mm], m[games[mm][0]], m[games[mm][1]])
        input()
    print([(len(x), x) for k, x in filtered.items()])
    input()
    # test = [x for x in filtered[0] if x.startswith("z")]
    # for t in test:
    #     print(games[t])
    #     print(t, m[t], known_z[t])
    #     input()
    # print([x for x in filtered[0] if x.startswith("z")])
    # input()
    pairs = set()
    for k, v in filtered.items():
        cs = combinations(v, 2)
        for cc in cs:
            if cc[0] == cc[1]:
                continue
            # was 4051 potentials
            # if k != 0:
            #     print(pairs)
            #     input()
            if k == 0:
                a, b, op = games[cc[0]]
                aa, bb, opp = games[cc[1]]
                # print(a, b, op)
                r = 0
                rr = 0
                if op == "AND":
                    r = m[a] & m[b]
                if op == "OR":
                    r = m[a] | m[b]
                if op == "XOR":
                    r = m[a] ^ m[b]
                if opp == "AND":
                    rr = m[aa] & m[bb]
                if opp == "OR":
                    rr = m[aa] | m[bb]
                if opp == "XOR":
                    rr = m[aa] ^ m[bb]
                if r != rr:
                    if cc[0].startswith("z") and known_z[cc[0]] != rr:
                        continue
                    if cc[1].startswith("z") and known_z[cc[1]] != r:
                        continue
                    pairs.add(cc)
            else:
                pairs.add(cc)
    # print(pairs)
    print(len(pairs))
    # input()
    qqq = 0
    start = time.time()
    cs = combinations(pairs, 4)
    start_zeros = [k for k, v in in_degrees.items() if v == 0]

    for attempt in cs:
        ss = set()
        if qqq % 100000 == 0 and qqq >= 100000:
            print(qqq, " took ", time.time() - start)
            print(qqq)
            print(attempt)
            start = time.time()
        for pair in attempt:
            ss.add(pair[0])
            ss.add(pair[1])
        if "z18" not in ss or len(ss) != 8:
            qqq += 1
            for pair in attempt:
                games[pair[0]], games[pair[1]] = games[pair[1]], games[pair[0]]
            continue
        for pair in attempt:
            games[pair[0]], games[pair[1]] = games[pair[1]], games[pair[0]]
        idx = 0
        in_copy = in_degrees.copy()
        should_skip_attempt = False
        zero_in = start_zeros
        while zero_in:
            new_zero = []
            # print(zero_in)
            # input()
            for z in zero_in:
                a, b, op = games[z]
                # print(a, b, op)
                r = 0
                if op == "AND":
                    r = m[a] & m[b]
                if op == "OR":
                    r = m[a] | m[b]
                if op == "XOR":
                    r = m[a] ^ m[b]
                m[z] = r
                if z.startswith("z"):
                    if known_z[z] != r:
                        # print(z, r, known_z)
                        # print(known_z[z], z in known_z)
                        # input()
                        should_skip_attempt = True
                        break
                for nei in adj[z]:
                    in_copy[nei] -= 1
                    if in_copy[nei] == 0:
                        new_zero.append(nei)
            if should_skip_attempt:
                break
            zero_in = new_zero
            c += 1
            idx += 1
        if should_skip_attempt:
            qqq += 1
            for pair in attempt:
                games[pair[0]], games[pair[1]] = games[pair[1]], games[pair[0]]
            continue
        print(attempt)
        l = []
        for a, b in attempt:
            l.append(a)
            l.append(b)
        print("".join(sorted(l)))
        input("This is your answer ^")
        # zs = sorted([(k, v) for k, v in m.items() if k.startswith("z")], reverse=True)
        # ans = 0
        # potentials = defaultdict(set)
        # failed = False
        # for z in zs:
        #     ans = ans << 1
        #     ans = ans + z[1]
        #     if known_z[z[0]] != z[1]:
        #         failed = True
        #         break
        #         # potentials[z[0]] = bfs(z[0], backwards)
        # # swap back
        for pair in attempt:
            games[pair[0]], games[pair[1]] = games[pair[1]], games[pair[0]]
        qqq += 1
        # if not failed:
        #     print(attempt)
        #     l = []
        #     for a, b in attempt:
        #         l.append(a)
        #         l.append(b)
        #     print("".join(sorted(l)))
        #     input("This is your answer ^")

    for k, v in potentials.items():
        print(k, v)
        input()
    print(combo)
    print(bin(ans)[2:])
    print("tst1231")
    fours = set()
    for cc in cs:
        fours.add(cc)
    print("fours")
    print(len(fours))
    input()

    print("in degrees not euqla to zero")
    e = [k for k, v in in_degrees.items() if v > 0]
    print(e)
    input()
    print(e)
    print(c)
    print(z_in_size)
    zs = sorted([(k, v) for k, v in m.items() if k.startswith("z")], reverse=True)
    ans = 0
    potentials = defaultdict(set)
    for z in zs:
        ans = ans << 1
        ans = ans + z[1]
        print(z)
        if known_z[z[0]] != z[1]:
            potentials[z[0]] = bfs(z[0], backwards)

    for k, v in potentials.items():
        print(k, v)
        input()
    print(combo)
    print(bin(ans)[2:])
    print(len(games.keys()))
    return ans


def part2b(lines):
    # print(m["z18"])
    # print(m["sgq"])
    # print(m["scq"], m["kfp"])
    # print(m["hbs"], m["gpk"], m["z10"], m["csk"])
    # print(m["vmg"], m["z19"], m["bng"], m["dhq"], m["qdb"])
    # print(m["jdm"], m["pdg"], m["gkg"])
    # print(m["cnr"])
    swap_pool = [
        "z18",
        "sgq",
        "scq",
        "kfp",
        "hbs",
        "gpk",
        "z10",
        "csk",
        "vmg",
        "z19",
        "bng",
        "dhq",
        "qdb",
        "jdm",
        "pdg",
        "gkg",
        "cnr",
    ]
    # "z18"
    # "sgq"
    # "scq" or "kfp"
    # "hbs" or "gpk" or ("z10" and "csk")
    # ("z19" and "bng") or ("dhq" and "qdb") or  "vmg"
    # "jdm" or *("pdg" and "gkg")
    # "cnr"
    m = defaultdict(int)
    ans = 0
    games = defaultdict(tuple)
    adj = defaultdict(set)
    in_degrees = defaultdict(int)
    backwards = defaultdict(set)
    o_wires = set()
    x_num = 0
    xidx = 0
    y_num = 0
    yidx = 0
    failed_run = False
    for yi, line in enumerate(lines):
        if ":" in line:
            key, num = line.split(":")
            num = int(num)
            m[key] = num
            if key.startswith("y"):
                to_add = num << yidx
                y_num = y_num | to_add
                yidx += 1
            if key.startswith("x"):
                to_add = num << xidx
                x_num = x_num | to_add
                xidx += 1
        elif line == "\n":
            continue
        elif "->" in line:
            game, result = line.split("->")
            a, op, b = game.split()
            a = a.strip()
            op = op.strip()
            b = b.strip()
            result = result.strip()
            games[result] = (a, b, op)
            adj[result].add(a)
            adj[result].add(b)
            backwards[result].add(a)
            backwards[result].add(b)
            adj[a].add(result)
            adj[b].add(result)
            o_wires.add(result)
            in_degrees[result] = 2
            if a in m:
                in_degrees[result] -= 1
            if b in m:
                in_degrees[result] -= 1
    zero_in = [k for k, v in in_degrees.items() if v == 0]
    # print(bin(x_num))
    # print(bin(y_num))
    combo = bin(x_num + y_num)[2:]
    print(combo)
    known_z = defaultdict(int)
    for i, l in enumerate(combo[::-1]):
        zid = f"z{i:02}"
        known_z[zid] = int(l)

    c = 0
    z_in_size = []
    zeros = defaultdict(list)
    idx = 0
    in_copy = in_degrees.copy()
    tmp_seen = set()
    is_wrong = set()
    while zero_in:
        z_in_size.append(len(zero_in))
        zeros[idx].extend(zero_in)
        new_zero = []
        # print(zero_in)
        # input()
        for z in zero_in:
            a, b, op = games[z]
            # print(a, b, op)
            r = 0
            if op == "AND":
                r = m[a] & m[b]
            if op == "OR":
                r = m[a] | m[b]
            if op == "XOR":
                r = m[a] ^ m[b]
            # if z == "qgt" or z == "gwq":
            #     print(z, a, m[a], b, m[b], op, r)
            #     input()
            m[z] = r
            for nei in adj[z]:
                in_copy[nei] -= 1
                if in_copy[nei] == 0:
                    new_zero.append(nei)
        for i in range(0, 46):
            zid = f"z{i:02}"
            if zid in m and zid not in tmp_seen:
                tmp_seen.add(zid)
                if known_z[zid] != m[zid]:
                    is_wrong.add(zid)
                # print(idx, zid, m[zid], known_z[zid])
                # input()
        zero_in = new_zero
        c += 1
        idx += 1

    print(is_wrong)
    # "z18"
    # "sgq"
    # "scq" or "kfp"
    # "hbs" or "gpk" or ("z10" and "csk")
    # ("z19" and "bng") or ("dhq" and "qdb") or  "vmg"
    # "jdm" or *("pdg" and "gkg")
    # "cnr"
    # print(m["sgq"])
    # print(m["scq"], m["kfp"])
    # print(m["hbs"], m["gpk"], m["z10"], m["csk"])
    # print(m["vmg"], m["z19"], m["bng"], m["dhq"], m["qdb"])
    # print(m["jdm"], m["pdg"], m["gkg"])
    # print(m["cnr"])
    print(zeros)
    filtered = {k: v for k, v in zeros.items()}  # if len(v) > 0}
    print([len(x) for k, x in filtered.items()])
    for k, v in filtered.items():
        print(len(v), v)
        # if len(v) > 10:
        #     continue
        for mm in v:
            if mm.startswith("z"):
                print(combo)
                print(str(combo)[::-1][int(mm[1:])])
                # print(combo[int(mm[1:])])
        for mm in v:
            print(mm, games[mm], m[games[mm][0]], m[games[mm][1]])
        input()
    print([(len(x), x) for k, x in filtered.items()])
    input()
    # test = [x for x in filtered[0] if x.startswith("z")]
    # for t in test:
    #     print(games[t])
    #     print(t, m[t], known_z[t])
    #     input()
    # print([x for x in filtered[0] if x.startswith("z")])
    # input()
    pairs = set()
    for k, v in filtered.items():
        cs = combinations(v, 2)
        for cc in cs:
            if cc[0] == cc[1]:
                continue
            # was 4051 potentials
            # if k != 0:
            #     print(pairs)
            #     input()
            if k == 0:
                a, b, op = games[cc[0]]
                aa, bb, opp = games[cc[1]]
                # print(a, b, op)
                r = 0
                rr = 0
                if op == "AND":
                    r = m[a] & m[b]
                if op == "OR":
                    r = m[a] | m[b]
                if op == "XOR":
                    r = m[a] ^ m[b]
                if opp == "AND":
                    rr = m[aa] & m[bb]
                if opp == "OR":
                    rr = m[aa] | m[bb]
                if opp == "XOR":
                    rr = m[aa] ^ m[bb]
                if r != rr:
                    if cc[0].startswith("z") and known_z[cc[0]] != rr:
                        continue
                    if cc[1].startswith("z") and known_z[cc[1]] != r:
                        continue
                    pairs.add(cc)
            else:
                pairs.add(cc)
    # print(pairs)
    print(len(pairs))
    # input()
    qqq = 0
    start = time.time()
    cs = combinations(pairs, 4)
    start_zeros = [k for k, v in in_degrees.items() if v == 0]

    for attempt in cs:
        ss = set()
        if qqq % 100000 == 0 and qqq >= 100000:
            print(qqq, " took ", time.time() - start)
            print(qqq)
            print(attempt)
            start = time.time()
        for pair in attempt:
            ss.add(pair[0])
            ss.add(pair[1])
        if "z18" not in ss or len(ss) != 8:
            qqq += 1
            for pair in attempt:
                games[pair[0]], games[pair[1]] = games[pair[1]], games[pair[0]]
            continue
        for pair in attempt:
            games[pair[0]], games[pair[1]] = games[pair[1]], games[pair[0]]
        idx = 0
        in_copy = in_degrees.copy()
        should_skip_attempt = False
        zero_in = start_zeros
        while zero_in:
            new_zero = []
            # print(zero_in)
            # input()
            for z in zero_in:
                a, b, op = games[z]
                # print(a, b, op)
                r = 0
                if op == "AND":
                    r = m[a] & m[b]
                if op == "OR":
                    r = m[a] | m[b]
                if op == "XOR":
                    r = m[a] ^ m[b]
                m[z] = r
                if z.startswith("z"):
                    if known_z[z] != r:
                        # print(z, r, known_z)
                        # print(known_z[z], z in known_z)
                        # input()
                        should_skip_attempt = True
                        break
                for nei in adj[z]:
                    in_copy[nei] -= 1
                    if in_copy[nei] == 0:
                        new_zero.append(nei)
            if should_skip_attempt:
                break
            zero_in = new_zero
            c += 1
            idx += 1
        if should_skip_attempt:
            qqq += 1
            for pair in attempt:
                games[pair[0]], games[pair[1]] = games[pair[1]], games[pair[0]]
            continue
        print(attempt)
        l = []
        for a, b in attempt:
            l.append(a)
            l.append(b)
        print("".join(sorted(l)))
        input("This is your answer ^")
        # zs = sorted([(k, v) for k, v in m.items() if k.startswith("z")], reverse=True)
        # ans = 0
        # potentials = defaultdict(set)
        # failed = False
        # for z in zs:
        #     ans = ans << 1
        #     ans = ans + z[1]
        #     if known_z[z[0]] != z[1]:
        #         failed = True
        #         break
        #         # potentials[z[0]] = bfs(z[0], backwards)
        # # swap back
        for pair in attempt:
            games[pair[0]], games[pair[1]] = games[pair[1]], games[pair[0]]
        qqq += 1
        # if not failed:
        #     print(attempt)
        #     l = []
        #     for a, b in attempt:
        #         l.append(a)
        #         l.append(b)
        #     print("".join(sorted(l)))
        #     input("This is your answer ^")

    for k, v in potentials.items():
        print(k, v)
        input()
    print(combo)
    print(bin(ans)[2:])
    print("tst1231")
    fours = set()
    for cc in cs:
        fours.add(cc)
    print("fours")
    print(len(fours))
    input()

    print("in degrees not euqla to zero")
    e = [k for k, v in in_degrees.items() if v > 0]
    print(e)
    input()
    print(e)
    print(c)
    print(z_in_size)
    zs = sorted([(k, v) for k, v in m.items() if k.startswith("z")], reverse=True)
    ans = 0
    potentials = defaultdict(set)
    for z in zs:
        ans = ans << 1
        ans = ans + z[1]
        print(z)
        if known_z[z[0]] != z[1]:
            potentials[z[0]] = bfs(z[0], backwards)

    for k, v in potentials.items():
        print(k, v)
        input()
    print(combo)
    print(bin(ans)[2:])
    print(len(games.keys()))
    return ans


def bfs(node, adj):
    q = deque([])
    q.append(node)
    seen = set()
    seen.add(node)
    while q:
        curr_node = q.popleft()
        for nei in adj[curr_node]:
            if nei not in seen:
                q.append(nei)
                seen.add(nei)
    seen.remove(node)
    return seen


print("ans pt1:", part1(i))
print("***********part 2***************")
print(part2(i))
