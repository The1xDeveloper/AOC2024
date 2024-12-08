use rayon::prelude::*;
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
    part2(&lines);
}
fn find_all(s: &str, sub: &str, start: i32) -> Vec<i32> {
    let idx_o = s[(start as usize)..].find(sub).map(|i| i as i32 + start);
    if idx_o.is_none() {
        return Vec::new();
    }
    let idx = idx_o.unwrap();
    let more = find_all(s, sub, idx + 1);

    let mut rtn = Vec::new();
    rtn.push(idx);
    if !more.is_empty() {
        rtn.extend(more.iter());
    }
    rtn
}
fn find_closest(idx: i32, nums: &[i32]) -> i32 {
    nums.iter()
        .filter_map(|x| {
            let t = idx - x;
            if t > 0 {
                Some(t)
            } else {
                None
            }
        })
        .min()
        .unwrap_or(99999999)
}

fn part2(lines: &[String]) {
    let full_string: String = lines.par_iter().cloned().collect();
    let mut potentials: Vec<(i32, i32)> = Vec::new();
    let re = Regex::new(r"mul\((\d{1,3}),(\d{1,3})\)").unwrap();
    let potentials: Vec<(i32, i32)> = lines
        .par_iter()
        .flat_map(|line| {
            re.captures_iter(line)
                .map(|c| (c[1].parse::<i32>().unwrap(), c[2].parse::<i32>().unwrap()))
                .collect::<Vec<_>>()
        })
        .collect();
    let mut dos: Vec<i32> = Vec::new();
    dos.push(0);
    let t = find_all(full_string.as_str(), "do()", 0);
    if !t.is_empty() {
        dos.extend(t.iter());
    }
    let donts = find_all(full_string.as_str(), "don't()", 0);
    let ans: i32 = potentials
        .par_iter()
        .filter_map(|(x, y)| {
            let idx = full_string.find(format!("mul({x},{y}").as_str()).unwrap() as i32;
            let closest_do = find_closest(idx, &dos);
            let closest_dont = find_closest(idx, &donts);
            if closest_do < closest_dont {
                Some(x * y)
            } else {
                None
            }
        })
        .sum();

    println!("pt2: {}", ans);
}
fn part1(lines: &[String]) {
    let re = Regex::new(r"mul\((\d{1,3}),(\d{1,3})\)").unwrap();
    let ans: i32 = lines
        .par_iter()
        .map(|line| {
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
