use regex::Regex;
use std::cmp;
use std::collections::HashMap;
use std::collections::HashSet;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let lines: Vec<String> = read_lines("../inputs/day3.txt")
        .unwrap()
        .map_while(Result::ok)
        .collect();
    part1(&lines);
}

fn test_nums(nums: Vec<i32>) -> bool {
    let window: Vec<i32> = nums.windows(2).map(|a| a[0] - a[1]).collect();
    let is_mono = window.iter().all(|&a| a > 0);
    let is_mono_dec = window.iter().all(|&a| a < 0);
    let is_in_bounds = window.iter().all(|&a| 1 <= a.abs() && a.abs() <= 3);
    (is_mono || is_mono_dec) && is_in_bounds
}
fn part1(lines: &[String]) {
    let ans: i32 = lines
        .iter()
        .map(|line| {
            let re = Regex::new(r"mul\((\d{1,3}),(\d{1,3})\)").unwrap();
            re.captures_iter(line)
                .map(|c| c[1].parse::<i32>().unwrap() * c[2].parse::<i32>().unwrap())
                .sum::<i32>()
        })
        .sum();
    println!("pt1: {}", ans);
}
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
