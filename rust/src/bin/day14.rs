use std::char;
use std::cmp;
use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::VecDeque;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::usize;

use regex::Regex;

fn main() {
    let lines: Vec<String> = read_lines("../inputs/day14.txt")
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
    let max_x = 101;
    let max_y = 103;
    let mid_x = max_x / 2;
    let mid_y = max_y / 2;
    println!("{}, {}", mid_x, mid_y);
    let mut ans = 0;
    let mut q1 = 0 as i64;
    let mut q2 = 0 as i64;
    let mut q3 = 0 as i64;
    let mut q4 = 0 as i64;
    for line in lines.iter() {
        let mut game_line = line.split_whitespace();
        let pos_info = game_line.next().unwrap();
        let vel_info = game_line.next().unwrap();
        let mut pos = pos_info.split("=").last().unwrap().split(",");
        let pos_x = pos.next().unwrap().parse::<i32>().unwrap();
        let pos_y = pos.next().unwrap().parse::<i32>().unwrap();
        let mut vel = vel_info.split("=").last().unwrap().split(",");
        let vel_x = vel.next().unwrap().parse::<i32>().unwrap();
        let vel_y = vel.next().unwrap().parse::<i32>().unwrap();
        let new_x = (pos_x + 100 * vel_x).rem_euclid(max_x);
        let new_y = (pos_y + 100 * vel_y).rem_euclid(max_y);
        println!(
            "{} {} {} {} {} {}",
            pos_x, pos_y, vel_x, vel_y, new_x, new_y
        );

        if new_y == mid_y || new_x == mid_x {
            continue;
        } else if new_y < mid_y && new_x < mid_x {
            q1 += 1
        } else if new_y < mid_y && new_x > mid_x {
            q2 += 1
        } else if new_y > mid_y && new_x < mid_x {
            q3 += 1
        } else if new_y > mid_y && new_x > mid_x {
            q4 += 1
        }
    }

    let t = q1 * q2 * q3 * q4;
    println!("pt1: {}", q1 * q2 * q3 * q4);
}
fn part2(lines: &[String]) {
    let max_x = 101;
    let max_y = 103;
    let mut master_grid = Vec::new();
    (0..max_y).for_each(|_| {
        master_grid.push(vec!["."; max_x as usize]);
    });
    (0..1000000).for_each(|i| {
        let mut points = Vec::new();
        let mut points_h = HashSet::new();
        let mut new_grid = master_grid.clone();
        for line in lines.iter() {
            let mut game_line = line.split_whitespace();
            let pos_info = game_line.next().unwrap();
            let vel_info = game_line.next().unwrap();
            let mut pos = pos_info.split("=").last().unwrap().split(",");
            let pos_x = pos.next().unwrap().parse::<i32>().unwrap();
            let pos_y = pos.next().unwrap().parse::<i32>().unwrap();
            let mut vel = vel_info.split("=").last().unwrap().split(",");
            let vel_x = vel.next().unwrap().parse::<i32>().unwrap();
            let vel_y = vel.next().unwrap().parse::<i32>().unwrap();
            let new_x = (pos_x + i * vel_x).rem_euclid(max_x);
            let new_y = (pos_y + i * vel_y).rem_euclid(max_y);
            points.push((new_x, new_y));
            points_h.insert((new_x, new_y));
            let t = new_grid
                .get_mut(new_y as usize)
                .unwrap()
                .get_mut(new_x as usize)
                .unwrap();
            *t = "#";
        }
        if points.len() == points_h.len() {
            println!("i: {}", i);
            for row in new_grid.into_iter() {
                println!("{}", row.join(""));
            }
        }
    });
}
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
