use std::cmp;
use std::collections::HashMap;
use std::collections::HashSet;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let lines: Vec<String> = read_lines("../inputs/day2.txt")
        .unwrap()
        .map_while(Result::ok)
        .collect();
    part1(lines.clone());
    part2(lines.clone());
}

fn test_nums(nums: Vec<i32>) -> bool {
    let window: Vec<i32> = nums.windows(2).map(|a| a[0] - a[1]).collect();
    let is_mono = window.iter().all(|&a| a > 0);
    let is_mono_dec = window.iter().all(|&a| a < 0);
    let is_in_bounds = window.iter().all(|&a| 1 <= a.abs() && a.abs() <= 3);
    (is_mono || is_mono_dec) && is_in_bounds
}
fn part1(lines: Vec<String>) {
    let ans: i32 = lines
        .into_iter()
        .map(|line| {
            let nums = line
                .split_whitespace()
                .map(|a| a.parse::<i32>().unwrap())
                .collect();
            if test_nums(nums) {
                1
            } else {
                0
            }
        })
        .sum();
    println!("pt1: {}", ans);
}
fn part2(lines: Vec<String>) {
    let ans: i32 = lines
        .into_iter()
        .map(|line| {
            let nums: Vec<i32> = line
                .split_whitespace()
                .map(|a| a.parse::<i32>().unwrap())
                .collect();
            let sub_nums: Vec<Vec<i32>> = (0..nums.len())
                .map(|i| {
                    let mut sub_num = nums.clone();
                    sub_num.remove(i);
                    sub_num
                })
                .collect();
            if test_nums(nums) || sub_nums.iter().any(|a| test_nums(a.clone())) {
                1
            } else {
                0
            }
        })
        .sum();
    println!("pt2: {}", ans);
}
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
