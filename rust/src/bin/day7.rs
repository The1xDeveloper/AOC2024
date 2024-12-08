use std::cmp;
use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::VecDeque;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let lines: Vec<String> = read_lines("../inputs/day7.txt")
        .unwrap()
        .map_while(Result::ok)
        .collect();
    part1(&lines);
    part2(&lines);
}
fn is_in_bounds(xi: i64, yi: i64, max_x: i64, max_y: i64) -> bool {
    (0 <= xi && xi <= max_x) && (0 <= yi && yi <= max_y)
}

fn part1(lines: &[String]) {
    let mut ans = 0;
    lines.iter().for_each(|line| {
        let mut splits = line.split(":");
        let target: i64 = splits.next().unwrap().parse::<i64>().unwrap();
        let nums_s = splits.next().unwrap();
        let mut nums: Vec<i64> = Vec::new();
        nums_s.split_whitespace().for_each(|num| {
            nums.push(num.parse::<i64>().unwrap());
        });
        let idx = 1i64;
        let mut q: VecDeque<(i64, i64)> = VecDeque::new();
        q.push_back((nums[0], idx));
        while !q.is_empty() {
            let (sub_s, c_idx) = q.pop_front().unwrap();
            if c_idx >= nums.len() as i64 {
                continue;
            }
            let r = nums[c_idx as usize];
            let add = sub_s + r;
            let mul = sub_s * r;
            if (c_idx == (nums.len() - 1) as i64) && (target == add || target == mul) {
                ans += target;
                break;
            }
            if add <= target {
                q.push_back((add, c_idx + 1));
            }
            if mul <= target {
                q.push_back((mul, c_idx + 1));
            }
        }
    });
    println!("ans: {}", ans);
}
fn part2(lines: &[String]) {
    let mut ans = 0;
    lines.iter().for_each(|line| {
        let mut splits = line.split(":");
        let target: i64 = splits.next().unwrap().parse::<i64>().unwrap();
        let nums_s = splits.next().unwrap();
        let mut nums: Vec<i64> = Vec::new();
        nums_s.split_whitespace().for_each(|num| {
            nums.push(num.parse::<i64>().unwrap());
        });
        let idx = 1i64;
        let mut q: VecDeque<(i64, i64)> = VecDeque::new();
        q.push_back((nums[0], idx));
        while !q.is_empty() {
            let (sub_s, c_idx) = q.pop_front().unwrap();
            if c_idx >= nums.len() as i64 {
                continue;
            }
            let r = nums[c_idx as usize];
            let add = sub_s + r;
            let mul = sub_s * r;
            let comb: i64 = format!("{}{}", sub_s, r).parse().unwrap();
            if (c_idx == (nums.len() - 1) as i64)
                && (target == add || target == mul || target == comb)
            {
                ans += target;
                break;
            }
            if add <= target {
                q.push_back((add, c_idx + 1));
            }
            if mul <= target {
                q.push_back((mul, c_idx + 1));
            }
            if comb <= target {
                q.push_back((comb, c_idx + 1));
            }
        }
    });
    println!("ans: {}", ans);
}
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
