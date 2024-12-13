use std::cmp;
use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::VecDeque;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

use regex::Regex;

fn main() {
    let lines: Vec<String> = read_lines("../inputs/day13.txt")
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

fn part1(lines: &[String]) {
    let mut start_idx = 0;
    let mut ans = 0;
    let btn_re = Regex::new(r"X\+(\d+),\s*Y\+(\d+)").unwrap();
    let target_re = Regex::new(r"X=(\d+),\s*Y=(\d+)").unwrap();
    while start_idx <= lines.len() - 4 {
        let btn_a = lines.get(start_idx).unwrap().as_str();
        let u = btn_re.captures_iter(btn_a);
        let w: Vec<(i64, i64)> = u
            .map(|c| (c[1].parse::<i64>().unwrap(), c[2].parse::<i64>().unwrap()))
            .collect();
        let t = w.first().unwrap();
        let x1 = t.0 as f64;
        let y1 = t.1 as f64;
        let btn_b = lines.get(start_idx + 1).unwrap();
        let u = btn_re.captures_iter(btn_b);
        let w: Vec<(i64, i64)> = u
            .map(|c| (c[1].parse::<i64>().unwrap(), c[2].parse::<i64>().unwrap()))
            .collect();
        let t = w.first().unwrap();
        let x2 = t.0 as f64;
        let y2 = t.1 as f64;
        let target = lines.get(start_idx + 2).unwrap();
        let u = target_re.captures_iter(target);
        let w: Vec<(i64, i64)> = u
            .map(|c| (c[1].parse::<i64>().unwrap(), c[2].parse::<i64>().unwrap()))
            .collect();
        let t = w.first().unwrap();
        let A = t.0 as f64;
        let B = t.1 as f64;
        let Y = (B - (y1 * A) / x1) / (-((y1 * x2) / x1) + y2);
        let X = (A - (x2 * Y)) / x1;
        if is_int(Y) && is_int(X) {
            ans += X as i64 * 3 + Y as i64;
        }
        start_idx += 4;
    }
    println!("pt1: {}", ans);
}
fn part2(lines: &[String]) {
    let mut start_idx = 0;
    let mut ans = 0 as f64;
    let btn_re = Regex::new(r"X\+(\d+),\s*Y\+(\d+)").unwrap();
    let target_re = Regex::new(r"X=(\d+),\s*Y=(\d+)").unwrap();
    while start_idx <= lines.len() - 3 {
        let btn_a = lines.get(start_idx).unwrap().as_str();
        let u = btn_re.captures_iter(btn_a);
        let w: Vec<(i64, i64)> = u
            .map(|c| (c[1].parse::<i64>().unwrap(), c[2].parse::<i64>().unwrap()))
            .collect();
        let t = w.first().unwrap();
        let x1 = t.0 as f64;
        let y1 = t.1 as f64;
        let btn_b = lines.get(start_idx + 1).unwrap();
        let u = btn_re.captures_iter(btn_b);
        let w: Vec<(i64, i64)> = u
            .map(|c| (c[1].parse::<i64>().unwrap(), c[2].parse::<i64>().unwrap()))
            .collect();
        let t = w.first().unwrap();
        let x2 = t.0 as f64;
        let y2 = t.1 as f64;
        let target = lines.get(start_idx + 2).unwrap();
        let u = target_re.captures_iter(target);
        let w: Vec<(i64, i64)> = u
            .map(|c| (c[1].parse::<i64>().unwrap(), c[2].parse::<i64>().unwrap()))
            .collect();
        let t = w.first().unwrap();
        let A = (t.0 + 10000000000000) as f64;
        let B = (t.1 + 10000000000000) as f64;
        let Y = (B - (y1 * A) / x1) / (-((y1 * x2) / x1) + y2);
        let X = (A - (x2 * Y)) / x1;
        if is_int(Y) && is_int(X) {
            ans += X * 3.0 + Y;
        }
        start_idx += 4;
    }
    println!("pt2: {}", ans);
}
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
