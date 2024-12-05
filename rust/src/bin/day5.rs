use std::cmp;
use std::collections::HashMap;
use std::collections::HashSet;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let lines: Vec<String> = read_lines("../inputs/day5.txt")
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
    let mut m: HashMap<i32, HashSet<i32>> = HashMap::new();
    let mut games: Vec<Vec<i32>> = Vec::new();

    lines.iter().for_each(|(line)| {
        if line.contains('|') {
            let mut t = line.split('|');
            let a = t.next().unwrap().parse::<i32>().unwrap();
            let b = t.next().unwrap().parse::<i32>().unwrap();
            m.entry(b).or_insert_with(HashSet::new).insert(a);
        } else if line.contains(',') {
            games.push(line.split(',').map(|i| i.parse::<i32>().unwrap()).collect());
        }
    });
    let ans: i32 = games
        .iter()
        .map(|game| {
            let mut h: HashSet<_> = game.iter().copied().collect();
            for n in game {
                h.remove(n);
                let t = m.entry(*n).or_default();
                if !h.is_disjoint(t) {
                    return 0;
                }
            }
            game[game.len() / 2]
        })
        .sum();
    println!("pt1: {}", ans);
}
fn part2(lines: &[String]) {
    let mut in_degrees: HashMap<i32, HashSet<i32>> = HashMap::new();
    let mut graph: HashMap<i32, Vec<i32>> = HashMap::new();
    let mut games: Vec<Vec<i32>> = Vec::new();

    lines.iter().for_each(|(line)| {
        if line.contains('|') {
            let mut t = line.split('|');
            let a = t.next().unwrap().parse::<i32>().unwrap();
            let b = t.next().unwrap().parse::<i32>().unwrap();
            in_degrees.entry(b).or_insert_with(HashSet::new).insert(a);
            graph.entry(b).or_insert_with(Vec::new).push(a);
            graph.entry(a).or_insert_with(Vec::new).push(b);
        } else if line.contains(',') {
            games.push(line.split(',').map(|i| i.parse::<i32>().unwrap()).collect());
        }
    });
    let ans: i32 = games
        .iter()
        .map(|game| {
            let mut h: HashSet<_> = game.iter().copied().collect();
            let mut must_fix = false;
            for n in game {
                h.remove(n);
                let t = in_degrees.entry(*n).or_default();
                if !h.is_disjoint(t) {
                    must_fix = true;
                }
            }
            if must_fix {
                let mut game_set: HashSet<_> = game.iter().copied().collect();
                let empty_set = HashSet::new();
                let mut l: HashMap<i32, HashSet<i32>> = game_set
                    .iter()
                    .map(|&a| {
                        let in_degree_set = in_degrees.get(&a).unwrap_or(&empty_set);
                        let intersection: HashSet<_> =
                            game_set.intersection(in_degree_set).copied().collect();
                        (a, intersection)
                    })
                    .collect();
                let mut zero = *l.iter().filter(|&x| x.1.is_empty()).next().unwrap().0;
                let mut new_game: Vec<i32> = Vec::new();
                while (zero) != -1 {
                    let mut new_zero = false;
                    new_game.push(zero);
                    let mut nz = 1;
                    for &nei in graph.get(&zero).unwrap() {
                        if (game_set.contains(&nei)) && (l.get_mut(&nei).unwrap().contains(&zero)) {
                            l.get_mut(&nei).unwrap().remove(&zero);
                            if l.get(&nei).unwrap().is_empty() {
                                nz = nei;
                                new_zero = true;
                            }
                        }
                    }
                    if !new_zero {
                        zero = -1;
                    } else {
                        zero = nz;
                    }
                }
                new_game[new_game.len() / 2]
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
