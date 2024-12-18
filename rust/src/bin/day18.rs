use rayon::prelude::*;
use std::cmp;
use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::VecDeque;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::time::Instant;
use std::usize;

fn main() {
    let lines: Vec<String> = read_lines("../inputs/day18.txt")
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
    let start = Instant::now();
    part2bi(&lines);
    let duration = start.elapsed();
    println!(
        "Time taken no i/o: {} seconds and {} nanos and {} millis and {} micros",
        duration.as_secs(),
        duration.as_nanos(),
        duration.as_millis(),
        duration.as_micros()
    )
}
fn is_in_bounds(xi: i32, yi: i32, max_x: i32, max_y: i32) -> bool {
    (0 <= xi && xi <= max_x) && (0 <= yi && yi <= max_y)
}
fn bfspt2bi(i: usize, xi: i32, yi: i32, end: (i32, i32), grid: Vec<Vec<char>>) -> Option<i32> {
    let mut dy = -1i32;
    let mut dx = 0i32;
    let max_y = (grid.len() - 1) as i32;
    let max_x = (grid[0].len() - 1) as i32;
    let mut seen: HashSet<(i32, i32)> = HashSet::new();
    let directions = [(1, 0), (-1, 0), (0, 1), (0, -1)];
    let mut q1: HashSet<(i32, i32)> = HashSet::new();
    let mut q2: HashSet<(i32, i32)> = HashSet::new();
    let mut q = VecDeque::new();
    q1.insert((0, 0));
    q2.insert(end);
    seen.insert((0, 0));
    seen.insert(end);

    q.push_back((xi, yi));
    while !q1.is_empty() && !q2.is_empty() {
        if q1.len() > q2.len() {
            (q1, q2) = (q2, q1);
        }
        let mut q = HashSet::new();
        for &(cx, cy) in &q1 {
            for (dx, dy) in directions {
                let nx = cx + dx;
                let ny = cy + dy;
                if is_in_bounds(nx, ny, max_x, max_y) && grid[ny as usize][nx as usize] != '#' {
                    if q2.contains(&(nx, ny)) {
                        return None;
                    }
                    if !seen.contains(&(nx, ny)) {
                        q.insert((nx, ny));
                        seen.insert((nx, ny));
                    }
                }
            }
        }
        (q, q1) = (q1, q);
    }
    Some(i as i32)
}
fn bfspt2(i: usize, xi: i32, yi: i32, end: (i32, i32), grid: Vec<Vec<char>>) -> Option<i32> {
    let mut dy = -1i32;
    let mut dx = 0i32;
    let max_y = (grid.len() - 1) as i32;
    let max_x = (grid[0].len() - 1) as i32;
    let mut seen: HashSet<(i32, i32)> = HashSet::new();
    let directions = [(1, 0), (-1, 0), (0, 1), (0, -1)];
    let mut q = VecDeque::new();

    q.push_back((xi, yi));
    while !q.is_empty() {
        let (cx, cy) = q.pop_front().unwrap();
        seen.insert((cx, cy));
        if (cx, cy) == end {
            return None;
        }
        for (dx, dy) in directions {
            let nx = cx + dx;
            let ny = cy + dy;
            if !seen.contains(&(nx, ny))
                && is_in_bounds(nx, ny, max_x, max_y)
                && grid[ny as usize][nx as usize] != '#'
            {
                q.push_back((nx, ny));
                seen.insert((nx, ny));
            }
        }
    }
    Some(i as i32)
}

fn part2bi(lines: &[String]) {
    let max_x = 70;
    let points: Vec<(i32, i32)> = lines
        .iter()
        .enumerate()
        .map(|(i, line)| {
            let mut split = line.split(",");
            let x = split.next().unwrap().parse::<i32>().unwrap();
            let y = split.next().unwrap().parse::<i32>().unwrap();
            (x, y)
        })
        .collect();
    let mut answers: Vec<i32> = (1024..points.len())
        .into_par_iter()
        .filter_map(|i| {
            let mut master_grid = Vec::new();
            (0..(max_x + 1)).for_each(|_| {
                master_grid.push(vec!['.'; max_x + 1 as usize]);
            });
            (0..=i).for_each(|x| {
                let point = points[x];
                let t = master_grid
                    .get_mut(point.1 as usize)
                    .unwrap()
                    .get_mut(point.0 as usize)
                    .unwrap();
                *t = '#';
            });
            bfspt2bi(i, 0, 0, (70, 70), master_grid)
        })
        .collect();
    answers.sort();
    let ans = points[*answers.first().unwrap() as usize];
    println!("pt2: {:?}", ans);
}
fn part2(lines: &[String]) {
    let max_x = 70;
    let points: Vec<(i32, i32)> = lines
        .iter()
        .enumerate()
        .map(|(i, line)| {
            let mut split = line.split(",");
            let x = split.next().unwrap().parse::<i32>().unwrap();
            let y = split.next().unwrap().parse::<i32>().unwrap();
            (x, y)
        })
        .collect();
    let mut answers: Vec<i32> = (1024..points.len())
        .into_par_iter()
        .filter_map(|i| {
            let mut master_grid = Vec::new();
            (0..(max_x + 1)).for_each(|_| {
                master_grid.push(vec!['.'; max_x + 1 as usize]);
            });
            (0..=i).for_each(|x| {
                let point = points[x];
                let t = master_grid
                    .get_mut(point.1 as usize)
                    .unwrap()
                    .get_mut(point.0 as usize)
                    .unwrap();
                *t = '#';
            });
            bfspt2(i, 0, 0, (70, 70), master_grid)
        })
        .collect();
    answers.sort();
    let ans = points[*answers.first().unwrap() as usize];
    println!("pt2: {:?}", ans);
}
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
