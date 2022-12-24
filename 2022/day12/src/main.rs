use std::env;
use std::cmp::Ordering;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::collections::HashMap;
use std::collections::BinaryHeap;

#[derive(Debug, Eq, Hash, Copy, Clone)]
struct Pos {
    x: usize,
    y: usize,
    v: u32,
}
impl PartialEq for Pos {
    fn eq(&self, other: &Self) -> bool {
        self.x == other.x && self.y == other.y && self.v == other.v
    }
}

#[derive(Clone, Eq, PartialEq)]
struct State {
    cost: usize,
    pos: Pos,
}
impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        other.cost.cmp(&self.cost)
            .then_with(|| self.pos.x.cmp(&other.pos.x))
            .then_with(|| self.pos.y.cmp(&other.pos.y))
    }
}
impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn is_valid(a: &Pos, b: &Pos) -> bool {
    let v = b.v as i32 - a.v as i32;
    v <= 1
}

fn get_ne(map: &Vec<Vec<Pos>>, pos: &Pos) -> Vec<Pos> {
    let mut rv: Vec<Pos> = Vec::new();
    // top
    if pos.y > 0 {
        let p = Pos{y: pos.y - 1, x: pos.x, v: map[pos.y-1][pos.x].v};
        if is_valid(&pos, &p) {
            rv.push(p);
        }
    }
    // right
    if pos.x < map[0].len()-1 {
        let p = Pos{y: pos.y, x: pos.x+1, v: map[pos.y][pos.x+1].v};
        if is_valid(&pos, &p) {
            rv.push(p);
        }
    }
    // bot
    if pos.y < map.len()-1 {
        let p = Pos{y: pos.y + 1, x: pos.x, v: map[pos.y+1][pos.x].v};
        if is_valid(&pos, &p) {
            rv.push(p);
        }
    }
    // left
    if pos.x > 0 {
        let p = Pos{y: pos.y, x: pos.x-1, v: map[pos.y][pos.x-1].v};
        if is_valid(&pos, &p) {
            rv.push(p);
        }
    }
    rv
}

fn cost(a: &Pos, b: &Pos) -> usize {
    let x = (a.x as i32) - (b.x as i32);
    let y = (a.y as i32) - (b.y as i32);
    (x.abs() + y.abs()) as usize
}

fn gp(cf: &HashMap<Pos, Option<Pos>>, start: &Pos, end: &Pos) -> Vec<Pos> {
    let mut path : Vec<Pos> = Vec::new();
    let mut cur = end.clone();
    if !cf.contains_key(&end) {
        return Vec::new();
    }
    while &cur != start {
        path.push(cur.clone());
        let x = cf.get(&cur).unwrap().clone();
        cur = x.unwrap();
    }
    //opt. path.push(start.clone());
    path.reverse();
    path
}

fn dijkstra(map: &Vec<Vec<Pos>>, start: &Pos, end: &Pos) -> HashMap<Pos, Option<Pos>> {
    let mut frontier = BinaryHeap::new();
    frontier.push(State{cost: 0, pos: start.clone()});
    let mut came_from : HashMap<Pos, Option<Pos>> = HashMap::new();
    let mut costs : HashMap<Pos, usize> = HashMap::new();
    came_from.insert(start.clone(), None);
    costs.insert(start.clone(), 0);

    while frontier.len() > 0 {
        let cur = frontier.pop().unwrap();
        if cur.pos.x == end.x && cur.pos.y == end.y {
            break
        }
        let neighbors = get_ne(&map, &cur.pos);
        for n in &neighbors {
            let new_cost = costs.get(&cur.pos).unwrap() + cost(&cur.pos, &n);
            if !costs.contains_key(&n) || new_cost < *costs.get(&n).unwrap() {
                costs.insert(n.clone(), new_cost);
                came_from.insert(n.clone(), Some(cur.pos.clone()));
                frontier.push(State{cost: new_cost, pos: n.clone()});
            }
        }
    }
    came_from
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let filename = args[1].clone();
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(&file);

    let start = 0;
    let end = 27;
    let mut start_pos = Pos{y: 0, x: 0, v: start};
    let mut end_pos = Pos{y: 0, x: 0, v: end};
    let mut map : Vec<Vec<Pos>> = Vec::new();
    let mut p2p : Vec<Pos> = Vec::new();
    for (y, line) in reader.lines().enumerate() {
        let line = line.unwrap();
        let mut row : Vec<Pos> = Vec::new();
        let mut x = 0;
        for c in line.chars() {
            let cc : u32;
            if c == 'S' {
                cc = start;
                start_pos.y = y;
                start_pos.x = x;
            } else if c == 'E' {
                cc = end;
                end_pos.y = y;
                end_pos.x = x;
            } else {
                cc = (c as u32) - 96;
            }
            if cc < 10 {
                print!(" {} ", cc);
            } else {
                print!("{} ", cc);
            }
            let pp = Pos{ x: x, y: y, v: cc};
            row.push(pp);
            if cc == 1 {
                p2p.push(pp.clone());
            }
            x += 1;
        }
        map.push(row);
        println!("");
    }

    let cf = dijkstra(&map, &start_pos, &end_pos);
    let p = gp(&cf, &start_pos, &end_pos);
    println!("p1: {}", p.len());

    let mut min_cost = p.len();
    for s in &p2p {
        let cf = dijkstra(&map, &s, &end_pos);
        let p = gp(&cf, &s, &end_pos);
        if p.len() > 0 && p.len() < min_cost {
            min_cost = p.len();
        }
    }
    println!("p2: {}", min_cost);
}
