use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::fmt;
use std::collections::HashSet;
use std::collections::VecDeque;

#[derive(Hash, Eq, PartialEq, Clone)]
enum Dir {
    Left(char),
    Right(char),
    Up(char),
    Down(char),
}
impl fmt::Display for Dir {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match *self {
            Dir::Left(c) => write!(f, "{}", c),
            Dir::Right(c) => write!(f, "{}", c),
            Dir::Up(c) => write!(f, "{}", c),
            Dir::Down(c) => write!(f, "{}", c),
        } 
    }
}
impl fmt::Debug for Dir {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match *self {
            Dir::Left(c) => write!(f, "{}", c),
            Dir::Right(c) => write!(f, "{}", c),
            Dir::Up(c) => write!(f, "{}", c),
            Dir::Down(c) => write!(f, "{}", c),
        } 
    }
}

#[derive(Debug, Hash, Eq, PartialEq, Clone)]
enum Tile {
    Wall(char),
    Floor(char),
}

#[derive(Debug, Hash, Eq, PartialEq, Clone)]
struct Pos {
    y: usize,
    x: usize,
    t: Tile,
    v: Vec<Dir>
}

#[derive(Debug, Hash, Eq, PartialEq, Clone)]
struct Pos2 {
    y: usize,
    x: usize,
}

fn pp(map: &Vec<Vec<Pos>>, player: &Pos) {
    for y in 0..map.len() {
        for x in 0..map[y].len() {
            match map[y][x].t {
                Tile::Wall(c) => print!("{}", c),
                Tile::Floor(_c) => {
                    if y == player.y && x == player.x {
                        print!("E");
                    } else if map[y][x].v.len() > 1 {
                        print!("{}", map[y][x].v.len());
                    } else if map[y][x].v.len() == 1 {
                        print!("{:?}", map[y][x].v[0]);
                    } else {
                        print!(".");
                    }
                },
            
            }
        }
        println!("")
    }
}

fn nm(h: usize, w: usize) -> Vec<Vec<Pos>> {
    let mut r : Vec<Vec<Pos>> = Vec::new();
    for y in 0..h {
        let mut row : Vec<Pos> = Vec::new();
        for x in 0..w {
            let mut t = Tile::Floor('.');
            if y == 0 || y == h - 1 {
                t = Tile::Wall('#')
            }
            if x == 0 || x == w - 1 {
                t = Tile::Wall('#')
            }
            if (y == 0 && x == 1) || (y == h - 1 && x == w - 2) {
                t = Tile::Floor('.')
            }
            row.push(Pos{y: y, x: x, v: Vec::new(), t: t});
        }
        r.push(row);
    }
    r
}

fn wind(map: &Vec<Vec<Pos>>) -> Vec<Vec<Pos>> {
    let h = map.len();
    let w = map[0].len();
    let mut r = nm(map.len(), w);
    for y in 0..h {
        for x in 0..w {
            let t = &map[y][x];
            for b in &t.v {
                match b {
                    Dir::Left(c) => {
                        if map[y][x-1].t == Tile::Wall('#') {
                            r[y][w-2].v.push(Dir::Left(*c));
                        } else {
                            r[y][x-1].v.push(Dir::Left(*c));
                        }
                    },
                    Dir::Right(c) => {
                        if map[y][x+1].t == Tile::Wall('#') {
                            r[y][1].v.push(Dir::Right(*c));
                        } else {
                            r[y][x+1].v.push(Dir::Right(*c));
                        }
                    },
                    Dir::Up(c) => {
                        if map[y-1][x].t == Tile::Wall('#') {
                            r[h-2][x].v.push(Dir::Up(*c));
                        } else {
                            r[y-1][x].v.push(Dir::Up(*c));
                        }
                    },
                    Dir::Down(c) => {
                        if map[y+1][x].t == Tile::Wall('#') {
                            r[1][x].v.push(Dir::Down(*c));
                        } else {
                            r[y+1][x].v.push(Dir::Down(*c));
                        }
                    },
                }
            }
        }
    }
    r
}

fn run(map0: &Vec<Vec<Pos>>, start: &Pos, dest: &Pos) -> usize {
    let mut map = map0.clone();
    let mut minutes = 0;
    let mut current : VecDeque<Option<Pos2>> = VecDeque::new();
    current.push_back(None);
    current.push_back(Some(Pos2{y: start.y, x: start.x}));
    loop {
        if current.len() < 1 {
            break;
        }
        let curo = current.remove(0).unwrap();
        match curo {
            None => {
                //println!("DN None");
                minutes += 1;
                map = wind(&map);
                let mut hs : HashSet<Pos2> = HashSet::new();
                for pp in &current {
                    match pp {
                        None => true,
                        Some(x) => hs.insert(x.clone()),
                    };
                }
                current = VecDeque::new();
                for h in &hs {
                    current.push_back(Some(h.clone()));
                }
                current.push_back(None);
                //println!("DN cur {:?}", current);
                continue
            },
            Some(cur) => {
                //println!("D some {:?}", cur);
                if cur.y == dest.y && cur.x == dest.x {
                    break;
                }
                if map[cur.y][cur.x].t != Tile::Floor('.') {
                    continue
                }
                if map[cur.y][cur.x].v.len() > 0 {
                    continue
                }
                let direction : Vec<Vec<i32>> = vec![vec![0,1], vec![0,-1], vec![1,0], vec![-1,0], vec![0,0]];
                for dir in &direction {
                    let y = (cur.y as i32 + dir[0]).rem_euclid(map.len() as i32);
                    let x = (cur.x as i32 + dir[1]).rem_euclid(map[0].len() as i32);
                    current.push_back(Some(Pos2{y: y as usize, x: x as usize}));
                }
                //println!("D NE {:?}", current);
                //println!("");
            }
        }
    }
    minutes
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let filename = args[1].clone();
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(&file);

    let mut map : Vec<Vec<Pos>> = Vec::new();
    let player : Pos = Pos{y:0, x: 1, t: Tile::Floor('.'), v: Vec::new()};
    let mut dest : Pos = Pos{y:0, x: 0, t: Tile::Floor('.'), v: Vec::new()};
    for (index, line) in reader.lines().enumerate() {
        let line = line.unwrap();
        let mut row : Vec<Pos> = Vec::new();
        for p in 0..line.len() {
            if &line[p..p+1] == "#" {
                row.push(Pos{y: index, x: p, t: Tile::Wall('#'), v: Vec::new()});
            } else if &line[p..p+1] == "." {
                row.push(Pos{y: index, x: p, t: Tile::Floor('.'), v: Vec::new()});
            } else if &line[p..p+1] == ">" {
                row.push(Pos{y: index, x: p, t: Tile::Floor('.'), v: vec![Dir::Right('>')]});
            } else if &line[p..p+1] == "v" {
                row.push(Pos{y: index, x: p, t: Tile::Floor('.'), v: vec![Dir::Down('v')]});
            } else if &line[p..p+1] == "<" {
                row.push(Pos{y: index, x: p, t: Tile::Floor('.'), v: vec![Dir::Left('<')]});
            } else if &line[p..p+1] == "^" {
                row.push(Pos{y: index, x: p, t: Tile::Floor('.'), v: vec![Dir::Up('^')]});
            }
        }
        map.push(row);
    }
    let last_row = map.len()-1;
    let last_col = map[last_row].len()-1;
    dest.y = map[last_row][last_col].y;
    dest.x = last_col - 1;
    println!("E: ({}, {}) F: ({}, {})", player.y, player.x, dest.y, dest.x);
    pp(&map, &player);

    let p1m = run(&map, &player, &dest);
    println!("p1: {}", p1m);

    let mut m2 = map.clone();
    for _i in 0..(p1m+0) {
        m2 = wind(&m2);
    }
    let p2m1 = run(&m2, &dest, &player);
    println!("p2_1 {}", p2m1);

    let mut m3 = m2.clone();
    for _i in 0..(p2m1+0) {
        m3 = wind(&m3);
    }
    let p2m2 = run(&m3, &player, &dest);
    println!("p2_2 {}", p2m2);
    println!("p2: {}", p2m2+p2m1+p1m);
}
