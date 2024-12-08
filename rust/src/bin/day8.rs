use rayon::prelude::*;
use regex::Regex;
use std::cmp;
use std::collections::HashMap;
use std::collections::HashSet;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let lines: Vec<String> = read_lines("../inputs/day8.txt")
        .unwrap()
        .map_while(Result::ok)
        .collect();
    part1(&lines);
    part2(&lines);
}

fn is_in_bounds(xi: i32, yi: i32, max_x: i32, max_y: i32) -> bool {
    (0 <= xi && xi <= max_x) && (0 <= yi && yi <= max_y)
}
fn part1(lines: &[String]) {
    let max_y = lines.len() - 1;
    let max_x = lines.get(0).unwrap().len() - 1;
    let mut antennas = HashMap::new();
    lines.iter().enumerate().for_each(|(yi, line)| {
        line.chars().enumerate().for_each(|(xi, chr)| {
            if chr != '.' {
                antennas.entry(chr).or_insert_with(Vec::new).push((xi, yi));
            }
        })
    });
    let mut nodes = HashSet::new();
    antennas.iter().for_each(|(_, locs)| {
        for i in 0..locs.len() {
            for j in i..locs.len() {
                if i == j {
                    continue;
                }
                let a = locs.get(i).unwrap();
                let b = locs.get(j).unwrap();
                let change = (a.0 - b.0, a.1 - b.1);
                let pOne = (a.0 + change.0, a.1 + change.1);
                let pTwo = (b.0 - change.0, b.1 - change.1);
                if is_in_bounds(pOne.0 as i32, pOne.1 as i32, max_x as i32, max_y as i32) {
                    nodes.insert(pOne);
                }
                if is_in_bounds(pTwo.0 as i32, pTwo.1 as i32, max_x as i32, max_y as i32) {
                    nodes.insert(pTwo);
                }
            }
        }
    });
    println!("pt1: {}", nodes.len());
}
fn part2(lines: &[String]) {
    let max_y = lines.len() - 1;
    let max_x = lines.get(0).unwrap().len() - 1;
    let mut antennas = HashMap::new();
    lines.iter().enumerate().for_each(|(yi, line)| {
        line.chars().enumerate().for_each(|(xi, chr)| {
            if chr != '.' {
                antennas.entry(chr).or_insert_with(Vec::new).push((xi, yi));
            }
        })
    });
    let mut nodes = HashSet::new();
    antennas.iter().for_each(|(_, locs)| {
        for i in 0..locs.len() {
            for j in i..locs.len() {
                if i == j {
                    continue;
                }
                let a = locs.get(i).unwrap();
                let b = locs.get(j).unwrap();
                let change = (a.0 - b.0, a.1 - b.1);
                let mut pOne = (a.0 + change.0, a.1 + change.1);
                let mut pTwo = (b.0 - change.0, b.1 - change.1);
                nodes.insert(*a);
                nodes.insert(*b);
                while is_in_bounds(pOne.0 as i32, pOne.1 as i32, max_x as i32, max_y as i32) {
                    nodes.insert(pOne);
                    pOne = (pOne.0 + change.0, pOne.1 + change.1)
                }
                while is_in_bounds(pTwo.0 as i32, pTwo.1 as i32, max_x as i32, max_y as i32) {
                    nodes.insert(pTwo);
                    pTwo = (pTwo.0 - change.0, pTwo.1 - change.1)
                }
            }
        }
    });
    println!("pt2: {}", nodes.len());
}
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
