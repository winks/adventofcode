use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};

#[derive(Debug, Clone)]
struct Tile {
    w: usize,
    h: usize,
    s: Vec<Vec<char>>,
}

#[derive(Debug, Eq, Hash, PartialEq)]
struct Pos {
    y: usize,
    x: usize,
    v: char,
}

fn pp(m : &Vec<Vec<char>>) {
    for y in (0..m.len()).rev() {
        for x in 0..m[y].len() {
            print!("{}", m[y][x]);
        }
        println!("");
    }
}
fn ppx(m : &Vec<Vec<char>>, mov: &Vec<Pos>) {
    for y in (0..m.len()).rev() {
        for x in 0..m[y].len() {
            let mut is_mov = false;
            for mm in mov {
                if y == mm.y && x == mm.x {
                    print!("{}", mm.v);
                    is_mov = true;
                    break;
                }
            }
            if !is_mov {
                print!("{}", m[y][x]);
            }
        }
        println!("");
    }
}
fn solid(m : &Vec<Vec<char>>, mov: &Vec<Pos>) -> Vec<Vec<char>> {
    let mut rv : Vec<Vec<char>> = Vec::new();
    for y in 0..m.len() {
        let mut row : Vec<char> = Vec::new();
        for x in 0..m[y].len() {
            let mut rock = false;
            for p in mov {
                if y == p.y && x == p.x && p.v == '@' {
                    row.push('#');
                    rock = true;
                    break;
                }
            }
            if !rock {
                row.push(m[y][x]);
            }
        }
        rv.push(row);
    }
    rv
}
fn collision(m : &Vec<Vec<char>>, v: &Vec<Pos>) -> bool {
    for y in 0..m.len() {
        for x in 0..m[y].len() {
            for p in v {
                if x == p.x && y == p.y && m[y][x] == '#' {
                    if p.v == '.' {
                        continue;
                    }
                    return true;
                }
            }
        }
    }
    return false
}
fn newmax(m : &Vec<Vec<char>>) -> usize {
    let mut rv = 0;
    for y in 0..m.len() {
        let mut block = false;
        for x in 0..m[y].len() {
            if m[y][x] != '.' {
                block = true;
                break;
            }
        }
        if block {
            rv = y;
        }
    }
    rv
}
fn maxx(v: &Vec<Pos>) -> usize {
    let mut r = v[0].x;
    for p in v {
        if p.x > r {
            r = p.x;
        }
    }
    r
}
fn minx(v: &Vec<Pos>) -> usize {
    let mut r = v[0].x;
    for p in v {
        if p.x < r {
            r = p.x;
        }
    }
    r
}

fn sl(v: &Vec<Pos>) -> Vec<Pos> {
    let mut rv : Vec<Pos> = Vec::new();
    for p in v {
        rv.push(Pos{y: p.y, x: p.x-1, v: p.v});
    }
    rv
}
fn sr(v: &Vec<Pos>) -> Vec<Pos> {
    let mut rv : Vec<Pos> = Vec::new();
    for p in v {
        rv.push(Pos{y: p.y, x: p.x+1, v: p.v});
    }
    rv
}
fn sd(v: &Vec<Pos>) -> Vec<Pos> {
    let mut rv : Vec<Pos> = Vec::new();
    for p in v {
        rv.push(Pos{y: p.y-1, x: p.x, v: p.v});
    }
    rv
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let filename = args[1].clone();
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(&file);

    let line_length = 7;
    let empty = vec!['.','.','.','.','.','.','.'];
    let mut tiles : Vec<Tile> = Vec::new();
    let tile_minus = Tile{w:4, h:1, s: vec![
        vec!['@','@','@','@'],
        ]};
    tiles.push(tile_minus);
    let tile_plus = Tile{w:3, h:3, s: vec![
        vec!['.','@','.'],
        vec!['@','@','@'],
        vec!['.','@','.'],
        ]};
    tiles.push(tile_plus);
    let tile_angle = Tile{w:3, h:3, s: vec![
        vec!['@','@','@'],
        vec!['.','.','@'],
        vec!['.','.','@'],
        ]};
    tiles.push(tile_angle);
    let tile_pipe = Tile{w:1, h:4, s: vec![
        vec!['@'],
        vec!['@'],
        vec!['@'],
        vec!['@'],
        ]};
    tiles.push(tile_pipe);
    let tile_block = Tile{w:2, h:2, s: vec![
        vec!['@','@'],
        vec!['@','@'],
    ]};
    tiles.push(tile_block);

    let mut map : Vec<Vec<char>> = vec![vec!['#','#','#','#','#','#','#']];
    for _i in 0..3 {
        map.push(empty.clone());
    }
    let mut ld : String;
    let mut dir = "";
    let mut dir_idx : usize = 0;
    for (_index, line) in reader.lines().enumerate() {
        ld = line.unwrap().clone();
        dir = &ld;
    }
    println!("dir {} {}", dir, dir.len());
    //pp(&map);

    let mut max_rock : u32 = 0;
    let mut has_coll : bool;
    let mut start : u32;
    let mut moving : Vec<Pos> = Vec::new();
    let mut next : Vec<Pos>;
    for step in 0..2022 {
        start = max_rock + 4;
        has_coll = false;
        println!("--------------------------- new - tile: {} max_rock: {} len: {}", step, max_rock, map.len());
        for n in 0..tiles[step%5].h {
            if max_rock < 10 || max_rock as usize + 6 + n > map.len() {
                map.push(empty.clone());
            }
            let y = start + n as u32;
            for z in 0..tiles[step%5].w {
                let x = 2 + z;
                moving.push(Pos{y: y as usize, x: x, v: tiles[step%5].s[n][z]});
            }
        }
        //ppx(&map, &moving);
        loop {
            if &dir[dir_idx..dir_idx+1] == "<" {
                print!("left? ");
                if minx(&moving) < 1 {
                    println!("... no");
                } else if !collision(&map, &sl(&moving)) {
                    println!("... yes");
                    moving = sl(&moving);
                } else {
                    println!("... no");
                }
            } else {
                print!("right?");
                if maxx(&moving) + 1 >= line_length {
                    println!("... no");
                } else if !collision(&map, &sr(&moving)) {
                    println!("... yes");
                    moving = sr(&moving);
                } else {
                    println!("... no");
                }
            }
            
            next = sd(&moving);
            if collision(&map, &next) {
                has_coll = true;
                println!("bottom!");
                map = solid(&map, &moving);
                moving = Vec::new();
                max_rock = newmax(&map) as u32;
            } else {
                println!("down");
                moving = sd(&moving);
            }
            dir_idx += 1;
            if dir_idx >= dir.len() {
                dir_idx = 0;
            }
            
            println!("==========");
            if has_coll {
                break;
            }
        }
        //ppx(&map, &moving);
    }
    //pp(&map);
    println!("p1: {}", max_rock);
}
