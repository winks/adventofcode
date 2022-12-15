use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::collections::HashSet;

#[derive(Clone, Copy, Debug)]
struct Point {
    x: i32,
    y: i32,
    s: char,
}

fn pp(m : Vec<Vec<char>>) {
    for y in 0..m.len() {
        for x in 0..m[0].len() {
            print!("{}", m[y][x]);
        }
        println!("");
    }
}

fn pp2(m : Vec<Vec<char>>, v: HashSet<(i32, i32)>, h: Point, t: Point) {
    let mut mx = m.clone();
    for y in 0..m.len() {
        for x in 0..m[0].len() {
            let mut cur = mx[y][x];
            for vv in v.iter() {
                if vv == &(y as i32, x as i32)  {
                    cur = '#';
                }
            }
            if t.x == x as i32 && t.y == y as i32 {
                if cur == '#' {
                    cur = 't';
                } else {
                    cur = 'T';
                }
            }
            if h.x == x as i32 && h.y == y as i32 {
                if cur == '#' {
                    cur = 'h';
                } else {
                    cur = 'H';
                }
            }
            print!("{}", cur);
        }
        println!("");
    }
}

fn close(h: Point, t: Point) -> bool {
    if h.x.abs_diff(t.x ) <= 1 {
        if h.y.abs_diff(t.y) <= 1 {
            return true
        }
    }
    return false
}

fn main() {
	let args: Vec<String> = env::args().collect();
    let filename = args[1].clone();
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(&file);

    let w = 11;
    let h = 11;
    let s_x : i32 = w-6;
    let s_y : i32 = h/2;

    let mut p_h = Point{x: s_x, y: s_y, s: 'H'};
    let mut p_t = Point{x: s_x, y: s_y, s: 'T'};

    let mut visi : HashSet<(i32, i32)> = HashSet::new();
    visi.insert((p_t.y, p_t.x));

    let mut map : Vec<Vec<char>> = Vec::new();
    for y in 0..h {
        let mut row = vec!['.'];
        for x in 0..(w-1) {
            if y == s_y && x == s_x {
                row.push('H');
            } else {
                row.push('.');
            }
        }
        map.push(row);
    }
    let map0 = map.clone();
    
    let mr = Point{x: 1,  y: 0,  s: 'R'};
    let ml = Point{x: -1, y: 0,  s: 'L'};
    let md = Point{x: 0,  y: 1,  s: 'D'};
    let mu = Point{x: 0,  y: -1, s: 'U'};

    pp(map);
    
    for (_index, line) in reader.lines().enumerate() {
        let line = line.unwrap();
        let parts = line.split(" ").collect::<Vec<&str>>();
        let dir = parts[0];
        let steps : usize = parts[1].parse().unwrap();
        println!("### {} {}", dir, steps);

        if dir == "R" {
            for i in 0..steps {
                println!("R {}", i);
                p_h.x += mr.x;
                p_h.y += mr.y;
                if !close(p_h, p_t) {
                    println!("Moving: H {:?} T {:?}", p_h, p_t);
                    p_t.x = p_h.x;
                    p_t.y = p_h.y;
                    p_t.x += ml.x;
                    p_t.y += ml.y;                   
                    println!("Moved : H {:?} T {:?}", p_h, p_t);
                } else {
                    println!("Nomov : H {:?} T {:?}", p_h, p_t);
                }
                visi.insert((p_t.y, p_t.x));
            }
        } else if dir == "L" {
            for i in 0..steps {
                println!("L {}", i);
                p_h.x += ml.x;
                p_h.y += ml.y;
                if !close(p_h, p_t) {
                    println!("Moving: H {:?} T {:?}", p_h, p_t);
                    p_t.x = p_h.x;
                    p_t.y = p_h.y;
                    p_t.x += mr.x;
                    p_t.y += mr.y;                   
                    println!("Moved : H {:?} T {:?}", p_h, p_t);
                } else {
                    println!("Nomov : H {:?} T {:?}", p_h, p_t);
                }
                visi.insert((p_t.y, p_t.x));
            }
        } else if dir == "U" {
            for i in 0..steps {
                println!("U {}", i);
                p_h.x += mu.x;
                p_h.y += mu.y;
                if !close(p_h, p_t) {
                    println!("Moving: H {:?} T {:?}", p_h, p_t);
                    p_t.x = p_h.x;
                    p_t.y = p_h.y;
                    p_t.x += md.x;
                    p_t.y += md.y;                   
                    println!("Moved : H {:?} T {:?}", p_h, p_t);
                } else {
                    println!("Nomov : H {:?} T {:?}", p_h, p_t);
                }
                visi.insert((p_t.y, p_t.x));
            }
        } else if dir == "D" {
            for i in 0..steps {
                println!("D {}", i);
                p_h.x += md.x;
                p_h.y += md.y;
                if !close(p_h, p_t) {
                    println!("Moving: H {:?} T {:?}", p_h, p_t);
                    p_t.x = p_h.x;
                    p_t.y = p_h.y;
                    p_t.x += mu.x;
                    p_t.y += mu.y;                   
                    println!("Moved : H {:?} T {:?}", p_h, p_t);
                } else {
                    println!("Nomov : H {:?} T {:?}", p_h, p_t);
                }
                visi.insert((p_t.y, p_t.x));
            }
        }
        println!("");
        //break
	}

    //for v in visi.collect() {
    //    println!("{:?}", v);
    //}
    let visi2 = visi.clone();
    pp2(map0, visi, p_h, p_t);
    //println!("{:?}", visi2);
    println!("p1: {}", visi2.len());
}
