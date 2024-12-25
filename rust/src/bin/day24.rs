use itertools::Itertools;
use rayon::prelude::*;
use std::cmp;
use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::VecDeque;
use std::fs::File;
use std::hash::Hash;
use std::io::stdin;
use std::io::{self, BufRead};
use std::path::Path;
use std::sync::Mutex;
use std::time::Instant;
use std::usize;

fn main() {
    let lines: Vec<String> = read_lines("../inputs/day24.txt")
        .unwrap()
        .map_while(Result::ok)
        .collect();
    let start = Instant::now();
    part2(&lines);
    let duration = start.elapsed();
    println!(
        "Time taken no i/o: {} seconds and {} nanos and {} millis and {} micros",
        duration.as_secs(),
        duration.as_nanos(),
        duration.as_millis(),
        duration.as_micros()
    );
}
fn print_vec(vec: Vec<i32>) {
    let t: Vec<String> = vec.into_iter().map(|i| i.to_string()).collect();
    println!("{}", t.join(""));
}
fn binary_addition(vec1: Vec<i32>, vec2: Vec<i32>) -> Vec<i32> {
    let mut result = vec![0; vec1.len()];
    let mut carry = 0;

    // Iterate from the least significant bit (LSB) to the most significant bit (MSB)
    for i in (0..vec1.len()).rev() {
        let sum = vec1[i] + vec2[i] + carry;
        result[i] = sum % 2; // Current bit
        carry = sum / 2; // Carry to the next bit
    }

    // If there's an overflow carry, prepend it
    if carry > 0 {
        let mut with_carry = vec![carry];
        with_carry.extend(result);
        return with_carry;
    }

    result
}
fn part2(lines: &[String]) {
    let swap_pool = [
        "z18", "kfp", "hbs", "z22", "frm", "ftw", "bng", "dhq", "qdb", "z28", "dwb", "qjd", "psk",
        "pdg", "jcp", "z27", "ckj",
    ];
    // let swap_pool = ["z18", "hbs", "kfp", "z22", "z27", "jcp", "dhq", "pdg"];
    let two_combos = swap_pool.into_iter().combinations(2);
    let mut validCombo = Vec::new();
    for tcb in two_combos {
        validCombo.push(tcb);
    }
    println!("len_two_combos: {}", validCombo.len());
    let mut mycount = 0;
    let for_combos = validCombo.into_iter().combinations(4);
    // let mut for_combos = Vec::new();
    // let mut for_combos_inner = Vec::new();
    // for_combos_inner.push(vec!["z27", "dhq"]);
    // for_combos_inner.push(vec!["z18", "pdg"]);
    // for_combos_inner.push(vec!["hbs", "kfp"]);
    // for_combos_inner.push(vec!["z22", "jcp"]);
    // for_combos.push(for_combos_inner);
    for four_combo in for_combos {
        mycount += 1;
        if mycount % 100000 == 0 && mycount >= 100000 {
            println!("at: {}", mycount);
        }
        let mut hmap = HashSet::new();
        for pair in four_combo.clone() {
            hmap.insert(pair[1]);
            hmap.insert(pair[0]);
        }
        if hmap.len() != 8 {
            continue;
        }
        if !hmap.contains("z18") || !hmap.contains("z27") || !hmap.contains("z22") {
            continue;
        }
        let mut m = HashMap::new();
        let mut games = HashMap::new();
        let mut adj = HashMap::new();
        let mut in_degrees: HashMap<&str, i32> = HashMap::new();
        let mut x_num: i32 = 0;
        let mut x_num_v = Vec::new();
        let mut xidx = 0;
        let mut y_num: i32 = 0;
        let mut y_num_v = Vec::new();
        let mut yidx = 0;
        let mut failed_run = false;
        lines.into_iter().for_each(|line| {
            if line.contains(":") {
                let mut tmp = line.split(":");
                let key = tmp.next().unwrap();
                let mut num = tmp.next().unwrap().trim().parse::<i32>().unwrap();
                m.insert(key, num);
                if key.starts_with("y") {
                    y_num_v.push(num);
                    let to_add = num << yidx;
                    y_num = y_num | to_add;
                    yidx += 1
                }
                if key.starts_with("x") {
                    x_num_v.push(num);
                    let to_add = num << xidx;
                    x_num = x_num | to_add;
                    yidx += 1
                }
            } else if line.contains("->") {
                let mut tmp = line.split("->");
                let mut game = tmp.next().unwrap();
                let mut result = tmp.next().unwrap().trim();
                let mut tmp = game.split_whitespace();
                let mut a = tmp.next().unwrap().trim();
                let mut op = tmp.next().unwrap().trim();
                let mut b = tmp.next().unwrap().trim();
                for cmbo in four_combo.clone() {
                    let mut inner_l = Vec::new();
                    if cmbo.contains(&result) {
                        for ee in cmbo {
                            if ee != result {
                                inner_l.push(ee);
                            }
                        }
                        result = inner_l[0];
                    }
                }
                games.insert(result, (a, b, op));
                adj.entry(result).or_insert(HashSet::new()).insert(a);
                adj.entry(result).or_insert(HashSet::new()).insert(b);
                adj.entry(a).or_insert(HashSet::new()).insert(result);
                adj.entry(b).or_insert(HashSet::new()).insert(result);
                in_degrees.insert(result, 2);
                if m.contains_key(a) {
                    *in_degrees.entry(result).or_insert(2) -= 1;
                }
                if m.contains_key(b) {
                    *in_degrees.entry(result).or_insert(2) -= 1;
                }
            }
        });
        let mut zero_in = Vec::new();
        for (k, v) in in_degrees.iter() {
            if *v == 0 {
                zero_in.push(*k);
            }
        }
        x_num_v.reverse();
        y_num_v.reverse();
        // print_vec(x_num_v.clone());
        // print_vec(y_num_v.clone());
        let mut combo = binary_addition(x_num_v, y_num_v);
        // print_vec(combo.clone());
        // let mut ip = String::new();
        // stdin().read_line(&mut ip);
        // let combo = x_num + y_num;
        let mut known_z = HashMap::new();
        for (i, l) in combo.iter().rev().enumerate() {
            let zid = format!("z{:02}", i);
            known_z.insert(zid, l.to_string().trim().parse::<i32>().unwrap());
        }

        // let mut ip = String::new();
        // stdin().read_line(&mut ip);
        let mut idx = 0;
        let mut zeros = HashMap::new();
        let mut in_copy = in_degrees.clone();
        while !zero_in.is_empty() {
            zeros.insert(idx, zero_in.clone());
            let mut net_zero = Vec::new();
            for z in zero_in.into_iter() {
                if !games.contains_key(z) {
                    continue;
                }
                // println!("z: {}", z);
                let (a, b, op) = games.get(z).unwrap();
                let mut r = 0;
                if *op == "AND" {
                    r = m.get(a).unwrap() & m.get(b).unwrap();
                }
                if *op == "OR" {
                    r = m.get(a).unwrap() | m.get(b).unwrap();
                }
                if *op == "XOR" {
                    r = m.get(a).unwrap() ^ m.get(b).unwrap();
                }
                if known_z.contains_key(z) {
                    if known_z[z] != r {
                        failed_run = true;
                        // println!("known_z: {}, z: {}, r: {}", known_z[z], z, r);
                        break;
                    }
                }
                m.entry(z).or_insert(r);
                for nei in adj.get(z).unwrap() {
                    if *nei == "z11" {
                        // println!("I found 11 z: {} and: {}", z, in_copy.get(*nei).unwrap());
                    }
                    *in_copy.entry(*nei).or_insert(2) -= 1;
                    if *in_copy.get(nei).unwrap() == 0 {
                        net_zero.push(*nei);
                    }
                }
            }
            if failed_run == true {
                break;
            }
            // for (k, v) in known_z.clone().into_iter() {
            //     if !m.contains_key(k.as_str()) {
            //         failed_run = true;
            //         println!("fialing xx");
            //         println!("k: {}, v: {}", k, v);
            //
            //         break;
            //         // println!("m: {:?}", m);
            //     }
            //     if m[k.as_str()] != v {
            //         failed_run = true;
            //         println!("fialing yy");
            //         break;
            //     }
            // }
            if failed_run == true {
                break;
            }
            zero_in = net_zero;
            idx += 1;
        }
        for (k, v) in known_z.clone().into_iter() {
            if !m.contains_key(k.as_str()) {
                failed_run = true;

                break;
            }
            if m[k.as_str()] != v {
                failed_run = true;
                break;
            }
        }
        if failed_run == true {
            continue;
        }
        let mut kkeys = Vec::new();
        for k in known_z.keys() {
            kkeys.push(k);
        }
        let mut wires_used = Vec::new();
        for combins in four_combo.clone() {
            for com in combins {
                wires_used.push(com);
            }
        }
        wires_used.sort();
        // not right csk,frm,gpk,hbs,kfp,scq,z10,z18
        //           csk,frm,gpk,hbs,kfp,scq,z10,z18

        println!("Wires: {}", wires_used.join(","));
        let mut ip = String::new();
        stdin().read_line(&mut ip);
        kkeys.sort();
    }
    // let mut filtered = HashMap::new();
    // for (k, v) in zeros.iter() {
    //     if v.len() > 1 {
    //         filtered.insert(*k, v);
    //     }
    // }
    // let mut pairs = HashSet::new();
    // for (k, v) in filtered.into_iter() {
    //     for cc in v.into_iter().combinations(2) {
    //         if cc[0] == cc[1] {
    //             continue;
    //         }
    //         if k == 0 {
    //             let (a, b, op) = games.get(cc[0]).unwrap();
    //             let (aa, bb, opp) = games.get(cc[1]).unwrap();
    //             let mut r = 0;
    //             let mut rr = 0;
    //             if *op == "AND" {
    //                 r = m.get(a).unwrap() & m.get(b).unwrap();
    //             }
    //             if *op == "OR" {
    //                 r = m.get(a).unwrap() | m.get(b).unwrap();
    //             }
    //             if *op == "XOR" {
    //                 r = m.get(a).unwrap() ^ m.get(b).unwrap();
    //             }
    //             if *opp == "AND" {
    //                 rr = m.get(aa).unwrap() & m.get(bb).unwrap();
    //             }
    //             if *opp == "OR" {
    //                 rr = m.get(aa).unwrap() | m.get(bb).unwrap();
    //             }
    //             if *opp == "XOR" {
    //                 rr = m.get(aa).unwrap() ^ m.get(bb).unwrap();
    //             }
    //             if r != rr {
    //                 if (*cc[0]).starts_with("z") && known_z[&cc[0].to_string()] != rr {
    //                     continue;
    //                 }
    //                 if (*cc[1]).starts_with("z") && known_z[&cc[1].to_string()] != r {
    //                     continue;
    //                 }
    //                 pairs.insert((*cc[0], *cc[1]));
    //             }
    //         } else {
    //             pairs.insert((*cc[0], *cc[1]));
    //         }
    //     }
    // }
    // let mut start_zeros = Vec::new();
    // for (k, v) in in_degrees.iter() {
    //     if *v == 0 {
    //         start_zeros.push(*k);
    //     }
    // }
    // let mut qqq = 0;
    // let mut start = Instant::now();
    // let total_combinations = pairs.len();
    //
    // for attempt in pairs.into_iter().combinations(4) {
    //     // qqq += 1;
    //     // if qqq % 1000000 == 0 && qqq >= 1000000 {
    //     //     let duration = start.elapsed();
    //     //     println!("on: {}", qqq);
    //     //     println!("time: {}", duration.as_millis());
    //     //     start = Instant::now();
    //     // }
    //     let mut ss = HashSet::new();
    //     for pair in attempt.clone().into_iter() {
    //         ss.insert(pair.0);
    //         ss.insert(pair.1);
    //     }
    //     // not right cnr,frm,gpk,kfp,mwv,psk,qjd,z18
    //     // also not right is with the two pairs and not cnr and below
    //
    //     // "z18"
    //     // "sgq"
    //     // "scq" or "kfp"
    //     // "hbs" or "gpk" or ("z10" and "csk")
    //     // ("z19" and "bng") or ("dhq" and "qdb") or  "vmg"
    //     // "jdm" or *("pdg" and "gkg")
    //     // "cnr"
    //     if !ss.contains("z18")
    //         || !ss.contains("kfp")
    //         || !ss.contains("hbs") // maybe? it has indegree of 0 and impacts an indegree of 1
    //         || !ss.contains("gpk") // maybe not??
    //         || !ss.contains("vtp") // maybe
    //         || !ss.contains("btp") // maybe
    //         || !ss.contains("fwt") // maybe
    //         || !ss.contains("jdm") // maybe
    //         || !ss.contains("bch") // maybe
    //         // || !ss.contans("frm") // I think this one doesnt need swap
    //         // || !ss.contains("dhq") // dhq and qdb are paired
    //         // || !ss.contains("qdb")
    //         // || !ss.contains("pdg") // pdg and qdb gkg paired
    //         // || !ss.contains("gkg")
    //         || !ss.contains("cnr")
    //         || !ss.contains("qjd")
    //         || !ss.contains("psk")
    //         || !ss.contains("mwv")
    //
    //         || ss.len() != 8
    //     {
    //         continue;
    //     }
    //     for pair in attempt.clone().into_iter() {
    //         if let (Some(value1), Some(value2)) = (games.remove(pair.0), games.remove(pair.1)) {
    //             games.insert(pair.0, value2);
    //             games.insert(pair.1, value1);
    //         }
    //     }
    //     let mut idx = 0;
    //     let mut in_copy = in_degrees.clone();
    //     let mut should_skip_attempt = false;
    //     let mut zero_in = start_zeros.clone();
    //     while !zero_in.is_empty() {
    //         let mut net_zero = Vec::new();
    //         for z in zero_in.into_iter() {
    //             let (a, b, op) = games.get(z).unwrap();
    //             let mut r = 0;
    //             if *op == "AND" {
    //                 r = m.get(a).unwrap() & m.get(b).unwrap();
    //             }
    //             if *op == "OR" {
    //                 r = m.get(a).unwrap() | m.get(b).unwrap();
    //             }
    //             if *op == "XOR" {
    //                 r = m.get(a).unwrap() ^ m.get(b).unwrap();
    //             }
    //             m.entry(z).or_insert(r);
    //             if z.starts_with("z") {
    //                 if known_z[z] != r {
    //                     should_skip_attempt = true;
    //                     break;
    //                 }
    //             }
    //             for nei in adj.get(z).unwrap() {
    //                 *in_copy.entry(*nei).or_insert(2) -= 1;
    //                 if *in_copy.get(*nei).unwrap() == 0 {
    //                     net_zero.push(*nei);
    //                 }
    //             }
    //         }
    //         if should_skip_attempt {
    //             break;
    //         }
    //         zero_in = net_zero;
    //         idx += 1;
    //     }
    //     if should_skip_attempt {
    //         for pair in attempt {
    //             if let (Some(value1), Some(value2)) = (games.remove(pair.0), games.remove(pair.1)) {
    //                 games.insert(pair.0, value2);
    //                 games.insert(pair.1, value1);
    //             }
    //         }
    //         continue;
    //     }
    //     let mut l = Vec::new();
    //     for (a, b) in attempt.into_iter() {
    //         l.push(a);
    //         l.push(b);
    //     }
    //     l.sort();
    //     println!("answer: {}", l.join(","));
    //     let mut ip = String::new();
    //     stdin().read_line(&mut ip);
    // }
    let ans = 0;

    println!("Ans: {}", ans);
}
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
