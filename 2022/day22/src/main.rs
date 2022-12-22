use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};

#[derive(Debug)]
struct Pos {
    y: usize,
    x: usize,
    dir: String,
}

#[derive(Debug)]
struct Way {
    len: usize,
    dir: String,
}

fn pp(map: &Vec<String>, cur: &Pos) {
    for y in 0..map.len() {
        for x in 0..map[y].len() {
            if y == cur.y && x == cur.x {
                print!("{}", cur.dir);
            } else {
                print!("{}", &map[y][x..x+1]);
            }
        }
        println!("");
    }
}

fn turn(cur: String, next: &str) -> String {
    let turns = "RDLU";
    let i = turns.find(&cur).unwrap();
    let mut j = i;
    if next == "R" {
        j += 1;
        if j >= turns.len() {
            j = 0;
        }
    } else {
        if i > 0 {
            j -= 1;
        } else {
            j = turns.len()-1;
        }
    }

    turns[j..j+1].to_string()
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let filename = args[1].clone();
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(&file);
    
    let mut map : Vec<String> = Vec::new();
    for (_index, line) in reader.lines().enumerate() {
        let line = line.unwrap();
        if line.len() < 1 {
            continue
        }
        map.push(line);
    }
    let ins = map.pop().unwrap();
    //let ins = "2L7R".to_string();
    let mut llen = map[0].len();
    for y in 0..map.len() {
        if map[y].len() > llen {
            llen = map[y].len();
        }
    }
    for y in 0..map.len() {
        if map[y].len() < llen {
            for _x in 0..(llen-map[y].len()) {
                map[y].push(' ');
            }
        }
    }

    let mut inst : Vec<Way> = Vec::new();
    let mut i = 1;
    let mut last = 0;
    while i < ins.len() {
        let c = &ins[i..i+1];
        if c == "R" || c == "D" || c == "L" || c == "U" {
            let len : usize = ins[last..i].parse().unwrap();
            let w = Way{len: len, dir: c.to_string()};
            inst.push(w);
            i += 2;
            last = i-1;
            continue
        }
        i += 1;
    }
    //println!("I {}", ins);
    //println!("I {:?}", inst);
    //println!("{:?}", map);
    
    let mut cur = Pos{y: 0, x: 0, dir: "R".to_owned() };
    'start: for y in 0..map.len() {
        if map[y].contains(".") {
            for x in 0..map[y].len() {
                if &map[y][x..x+1] == "." {
                    cur.y = y;
                    cur.x = x;
                    break 'start;
                }
            }
        }
    }
    pp(&map, &cur);
    for i in 0..inst.len() {
        //println!("CUR {:?}", cur);
        //println!("NOW {:?}", inst[i]);
        for _s in 0..inst[i].len {
            if cur.dir == "R" {
                let mut next = " ";
                if cur.x + 2 <= map[cur.y].len() {
                    next = &map[cur.y][cur.x+1..cur.x+2];    
                }
                //println!("next R: {} ({},{})", next, cur.y, cur.x);
                if next == "." {
                    cur.x += 1;
                } else if next == "#" {
                    break;
                } else if next == " " {
                    //println!("overflow");
                    let pos_floor = map[cur.y].find(".").unwrap();
                    let pos_wall  = map[cur.y].find("#").unwrap();
                    if pos_floor < pos_wall {
                        cur.x = pos_floor;
                    }
                } else {
                    panic!("aaa");
                }
            } else if cur.dir == "L" {
                let mut next = " ";
                if cur.x >= 1 {
                    next = &map[cur.y][cur.x-1..cur.x];    
                }
                //println!("next L: {}", next);
                if next == "." {
                    cur.x -= 1;
                } else if next == "#" {
                    break;
                } else if next == " " {
                    //println!("overflow");
                    let pos_floor = map[cur.y].rfind(".").unwrap();
                    let pos_wall  = map[cur.y].rfind("#").unwrap();
                    if pos_floor > pos_wall {
                        cur.x = pos_floor;
                    }
                } else {
                    panic!("aaa");
                }
            } else if cur.dir == "D" {
                let mut next = " ";
                if cur.y + 1 < map.len() {
                    next = &map[cur.y+1][cur.x..cur.x+1];
                }
                //println!("next D: {} ({},{})", next, cur.y, cur.x);
                if next == "." {
                    cur.y += 1;
                } else if next == "#" {
                    break;
                } else if next == " " {
                    //println!("overflow");
                    let mut tmp_row = String::new();
                    for y in 0..cur.y+1 {
                        let cx = &map[y][cur.x..cur.x+1].chars().next().unwrap();
                        tmp_row.push(*cx);
                    }
                    //println!("T|{}|", tmp_row);
                    let pos_floor = tmp_row.find(".").unwrap();
                    let pos_wall  = tmp_row.find("#").unwrap();
                    if pos_floor < pos_wall {
                        cur.y = pos_floor;
                    }
                } else {
                    panic!("aaa");
                }
            } else if cur.dir == "U" {
                let mut next = " ";
                if cur.y >= 1 {
                    next = &map[cur.y-1][cur.x..cur.x+1];
                }
                //println!("next U: {} ({},{})", next, cur.y, cur.x);
                if next == "." {
                    cur.y -= 1;
                } else if next == "#" {
                    break;
                } else if next == " " {
                    //println!("overflow");
                    let mut tmp_row = String::new();
                    for y in 0..map.len() {
                        let cx = &map[y][cur.x..cur.x+1].chars().next().unwrap();
                        tmp_row.push(*cx);
                    }
                    //println!("T|{}|", tmp_row);
                    let pos_floor = tmp_row.rfind(".").unwrap();
                    let pos_wall  = tmp_row.rfind("#").unwrap();
                    if pos_floor > pos_wall {
                        cur.y = pos_floor;
                    }
                } else {
                    panic!("aaa");
                }
            }
        }
        let nd = turn(cur.dir, &inst[i].dir);
        cur.dir = nd;
        //println!("CUR {:?}", cur);
        //println!("");
        //pp(&map, &cur);
    }
    let mut f = 0;
    if cur.dir == "D" {
        f = 1;
    } else if cur.dir == "L" {
        f = 2;
    } else if cur.dir == "U" {
        f = 3;
    }
    println!("p1: {}", 1000 * (cur.y+1) + 4 * (cur.x+1) + f);
}
