use rayon::iter::IntoParallelIterator;
use rayon::iter::ParallelIterator;
use regex::Regex;
use std::char;
use std::cmp;
use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::VecDeque;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::usize;

fn main() {
    let lines: Vec<String> = read_lines("../inputs/day17.txt")
        .unwrap()
        .map_while(Result::ok)
        .collect();
    part1(&lines);
    part2(&lines);
}
fn is_int(a: f64) -> bool {
    let b = (a + 0.5).floor();
    (a - b).abs() < 0.001
}
fn is_in_bounds(xi: i64, yi: i64, max_x: i64, max_y: i64) -> bool {
    (0 <= xi && xi <= max_x) && (0 <= yi && yi <= max_y)
}

fn get_combo_operand(operand: i64, A: i64, B: i64, C: i64) -> i64 {
    if [0, 1, 2, 3].contains(&operand) {
        return operand;
    }
    if operand == 4 {
        return A;
    }
    if operand == 5 {
        return B;
    }
    if operand == 6 {
        return C;
    }
    return 7;
}
fn part1(lines: &[String]) {
    let mut A = 0;
    let mut B = 0;
    let mut C = 0;
    let mut program = Vec::new();

    for line in lines.iter() {
        if line.starts_with("Register A") {
            A = line
                .split(":")
                .last()
                .unwrap()
                .trim()
                .parse::<i64>()
                .unwrap();
        }
        if line.starts_with("Register B") {
            B = line
                .split(":")
                .last()
                .unwrap()
                .trim()
                .parse::<i64>()
                .unwrap();
        }
        if line.starts_with("Register C") {
            C = line
                .split(":")
                .last()
                .unwrap()
                .trim()
                .parse::<i64>()
                .unwrap();
        }
        if line.starts_with("Program") {
            line.split(":").last().unwrap().split(",").for_each(|ch| {
                program.push(ch.trim().parse::<i64>().unwrap());
            });
        }
    }
    let mut i = 0;
    let max_i = program.len();
    let mut outputs = Vec::new();
    while i < max_i - 1 {
        let opcode = program[i];
        let operand = program[i + 1];

        if opcode == 0 {
            let num = A;
            let comb = get_combo_operand(operand, A, B, C);
            let den = (2 as i64).pow(comb as u32);
            A = num / den;
        }
        if opcode == 1 {
            B = B ^ operand;
        }
        if opcode == 2 {
            B = get_combo_operand(operand, A, B, C).rem_euclid(8);
        }
        if opcode == 3 {
            if A != 0 {
                i = operand as usize;
                continue;
            }
        }
        if opcode == 4 {
            B = B ^ C;
        }
        if opcode == 5 {
            let t = get_combo_operand(operand, A, B, C).rem_euclid(8);
            outputs.push(t);
        }
        if opcode == 6 {
            let num = A;
            let comb = get_combo_operand(operand, A, B, C);
            let den = (2 as i64).pow(comb as u32);
            B = num / den;
        }

        if opcode == 7 {
            let num = A;
            let comb = get_combo_operand(operand, A, B, C);
            let den = (2 as i64).pow(comb as u32);
            C = num / den;
        }
        i += 2
    }
    let os: Vec<String> = outputs.iter().map(|&c| c.to_string()).collect();
    println!("{}", os.join(","));
    println!("{} {} {} {:?}", A, B, C, program)
}
// 100000000 too low
// 10000000000 too low
// 100000000000 too low
fn part2(lines: &[String]) {
    let mut program = Vec::new();
    for line in lines.iter() {
        if line.starts_with("Program") {
            line.split(":").last().unwrap().split(",").for_each(|ch| {
                program.push(ch.trim().parse::<i64>().unwrap());
            });
        }
    }
    (35_184_372_088_832..281_474_976_710_656)
        .into_par_iter()
        .for_each(|a| {
            if (a as i64).rem_euclid(10_000_000_000) == 0 {
                println!("at: {}", a);
            }

            let a_val = 1;
            let a_div = a / a_val;
            let w = (a_div % 8) ^ 3;
            let xy = 1 << ((a_div % 8) ^ 5);
            let x: i64 = (a / (a_val * (xy)));
            let zz = (w ^ x) % 8;
            if zz != program[0] {
                return;
            }
            let a_val = 8;
            let a_div = a / a_val;
            let w = (a_div % 8) ^ 3;
            let xy = 1 << ((a_div % 8) ^ 5);
            let x: i64 = (a / (a_val * (xy)));
            let zz = (w ^ x) % 8;
            if zz != program[1] {
                return;
            }
            let a_val = 64;
            let a_div = a / a_val;
            let w = (a_div % 8) ^ 3;
            let xy = 1 << ((a_div % 8) ^ 5);
            let x: i64 = (a / (a_val * (xy)));
            let zz = (w ^ x) % 8;
            if zz != program[2] {
                return;
            }
            let a_val = 512;
            let a_div = a / a_val;
            let w = (a_div % 8) ^ 3;
            let xy = 1 << ((a_div % 8) ^ 5);
            let x: i64 = (a / (a_val * (xy)));
            let zz = (w ^ x) % 8;
            if zz != program[3] {
                return;
            }
            let a_val = 4096;
            let a_div = a / a_val;
            let w = (a_div % 8) ^ 3;
            let xy = 1 << ((a_div % 8) ^ 5);
            let x: i64 = (a / (a_val * (xy)));
            let zz = (w ^ x) % 8;
            if zz != program[4] {
                return;
            }
            let a_val = 32768;
            let a_div = a / a_val;
            let w = (a_div % 8) ^ 3;
            let xy = 1 << ((a_div % 8) ^ 5);
            let x: i64 = (a / (a_val * (xy)));
            let zz = (w ^ x) % 8;
            if zz != program[5] {
                return;
            }
            let a_val = 262144;
            let a_div = a / a_val;
            let w = (a_div % 8) ^ 3;
            let xy = 1 << ((a_div % 8) ^ 5);
            let x: i64 = (a / (a_val * (xy)));
            let zz = (w ^ x) % 8;
            if zz != program[6] {
                return;
            }
            let a_val = 2097152;
            let a_div = a / a_val;
            let w = (a_div % 8) ^ 3;
            let xy = 1 << ((a_div % 8) ^ 5);
            let x: i64 = (a / (a_val * (xy)));
            let zz = (w ^ x) % 8;
            if zz != program[7] {
                return;
            }
            let a_val = 16777216;
            let a_div = a / a_val;
            let w = (a_div % 8) ^ 3;
            let xy = 1 << ((a_div % 8) ^ 5);
            let x: i64 = (a / (a_val * (xy)));
            let zz = (w ^ x) % 8;
            if zz != program[8] {
                return;
            }
            let a_val = 134217728;
            let a_div = a / a_val;
            let w = (a_div % 8) ^ 3;
            let xy = 1 << ((a_div % 8) ^ 5);
            let x: i64 = (a / (a_val * (xy)));
            let zz = (w ^ x) % 8;
            if zz != program[9] {
                return;
            }
            let a_val = 1073741824;
            let a_div = a / a_val;
            let w = (a_div % 8) ^ 3;
            let xy = 1 << ((a_div % 8) ^ 5);
            let x: i64 = (a / (a_val * (xy)));
            let zz = (w ^ x) % 8;
            if zz != program[10] {
                return;
            }
            let a_val = 8589934592;
            let a_div = a / a_val;
            let w = (a_div % 8) ^ 3;
            let xy = 1 << ((a_div % 8) ^ 5);
            let x: i64 = (a / (a_val * (xy)));
            let zz = (w ^ x) % 8;
            if zz != program[11] {
                return;
            }
            let a_val = 68719476736;
            let a_div = a / a_val;
            let w = (a_div % 8) ^ 3;
            let xy = 1 << ((a_div % 8) ^ 5);
            let x: i64 = (a / (a_val * (xy)));
            let zz = (w ^ x) % 8;
            if zz != program[12] {
                return;
            }
            let a_val = 549755813888;
            let a_div = a / a_val;
            let w = (a_div % 8) ^ 3;
            let xy = 1 << ((a_div % 8) ^ 5);
            let x: i64 = (a / (a_val * (xy)));
            let zz = (w ^ x) % 8;
            if zz != program[13] {
                return;
            }
            let a_val = 4398046511104;
            let a_div = a / a_val;
            let w = (a_div % 8) ^ 3;
            let xy = 1 << ((a_div % 8) ^ 5);
            let x: i64 = (a / (a_val * (xy)));
            let zz = (w ^ x) % 8;
            if zz != program[14] {
                return;
            }
            let a_val = 35184372088832;
            let a_div = a / a_val;
            let w = (a_div % 8) ^ 3;
            let xy = 1 << ((a_div % 8) ^ 5);
            let x: i64 = (a / (a_val * (xy)));
            let zz = (w ^ x) % 8;
            if zz != program[15] {
                return;
            }
            println!("Ans: {}", a);
        })
}
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
