use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::collections::HashMap;
use std::collections::HashSet;

#[derive(Debug, PartialEq, Clone, Eq, Hash)]
struct Pos {
    y: usize,
    x: usize,
}

fn filler(border: usize, middle: usize) -> Vec<char> {
    let mut row : Vec<char> = Vec::new();
    for b2 in 0..(2*border) {
        row.push('.');
    }
    for b2 in 0..middle {
        row.push('.');
    }
    return row
}

fn pp(map: &Vec<Vec<char>>) {
    for y in 0..map.len() {
        for x in 0..map[0].len() {
            print!("{}", map[y][x]);
        }
        println!("");
    }
}

fn getelf(map: &Vec<Vec<char>>) -> Vec<Pos> {
    let mut rv : Vec<Pos> = Vec::new();
    for y in 0..map.len() {
        for x in 0..map[y].len() {
            if map[y][x] == '#' {
                rv.push(Pos{y: y, x: x});
            }
        }
    }
    rv
}

fn is_adj(a: &Pos, b: &Pos) -> bool {
    if a.x == b.x && a.y == b.y {
        return true
    } else if (a.x as i32 - b.x as i32).abs() <= 1
        && (a.y as i32 - b.y as i32).abs() <= 1 {
        return true
    }
    false
}

fn getne(map: &Vec<Vec<char>>, cur: &Pos, dir: usize) -> Vec<Pos> {
    let mut rv : Vec<Pos> = Vec::new();
    // NW, N, NE
    if dir == 0 {
        for x in (cur.x-1)..(cur.x+2) {
            if map[cur.y-1][x] == '#' {
                rv.push(Pos{y: cur.y-1, x: x});
            }
        }
    } else if dir == 1 {
        // SW, S, SE
        for x in (cur.x-1)..(cur.x+2) {
            if map[cur.y+1][x] == '#' {
                rv.push(Pos{y: cur.y+1, x: x});
            }
        }
        
    } else if dir == 2 {
        // NW, W, SW
        for y in (cur.y-1)..(cur.y+2) {
            if map[y][cur.x-1] == '#' {
                rv.push(Pos{y: y, x: cur.x-1});
            }
        }
    } else {
        // E, NE, SE
        for y in (cur.y-1)..(cur.y+2) {
            if map[y][cur.x+1] == '#' {
                rv.push(Pos{y: y, x: cur.x+1});
            }
        }
    }
    rv
}
fn mov(p: &Pos, dir: usize) -> Pos {
    if dir == 0 {
        return Pos{y: p.y-1, x: p.x}
    } else if dir == 1 {
        return Pos{y: p.y+1, x: p.x}
    } else if dir == 2 {
        return Pos{y: p.y, x: p.x-1}
    }
    Pos{y: p.y, x: p.x+1}
}

fn count(m: &Vec<Vec<char>>) -> usize {
    let mut miy = 1000;
    let mut mix = 1000;
    let mut max = 0;
    let mut may = 0;
    for y in 0..m.len() {
        for x in 0..m[y].len() {
            if m[y][x] == '#' {
                if y < miy {
                    miy = y;
                }
                if y > may {
                    may = y;
                }
                if x < mix {
                    mix = x;
                }
                if x > max {
                    max = x;
                }
            }
        }
    }
    let mut rv = 0;
    for y in miy..may+1 {
        for x in mix..max+1 {
            if m[y][x] != '#' {
                rv += 1;
            }
        }
    }
    //println!("{} {} {} {}", miy, mix, may, max);
    rv
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let filename = args[1].clone();
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(&file);

    let mut map : Vec<Vec<char>> = Vec::new();
    let border = 60;
    let mut pre : Vec<char> = Vec::new();
    for (index, line) in reader.lines().enumerate() {
        let line = line.unwrap();
        //println!("{} {} {}", index, border, line);
        if index == 0 {
            pre = filler(border, line.len());
            for bp in 0..border {
                map.push(pre.clone());
            }
        }
        let mut row : Vec<char> = Vec::new();
        for b in 0..border {
            row.push('.');
        }
        for c in line.chars() {
            row.push(c)
        }
        for b2 in 0..border {
            row.push('.');
        }
        
        map.push(row.clone());
    }
    for bp in 0..border {
        map.push(pre.clone());
    }
    //pp(&map);
    let mut running = true;
    let mut dd = vec![0,1,2,3];
    let mut step = 1;
    let mut p1r = 0;
    let mut p2r = 0;
    loop {
        if !running {
            break;
        }
        //println!("STEP {} [{:?}]", step, dd);
        let elves = getelf(&map);
        //println!("{:?}", elves);
        let mut elves_active : HashSet<Pos> = HashSet::new();
        'outer: for e1 in &elves {
            let mut x = false;
            for e2 in &elves {
                if e1 == e2 {
                    continue
                }
                x = is_adj(&e1, &e2);
                if x {
                    //println!("{:?} {:?} {}", e1, e2, x);
                    elves_active.insert(e2.clone());
                    elves_active.insert(e1.clone());
                    continue 'outer
                }
            }
        }
        //println!("A {} {:?}", elves_active.len(), elves_active);
        let mut elves_next : HashMap<usize, Vec<Pos>> = HashMap::new();
        for i in 0..4 {
            elves_next.entry(i).or_insert(Vec::new());
        }
        for e in elves_active {
            for i in dd.clone() {
                let n = getne(&map, &e, i);
                //println!("Nx {:?} {} [{}]", e, i, n.len());
                if n.len() == 0 {
                    elves_next.get_mut(&i).unwrap().push(e.clone());
                    break;
                }
            }
        }
        let mut dest : HashMap<Pos, Vec<Pos>> = HashMap::new();
        //println!("{:?}", elves_next);
        for i in 0..4 {
            let s = elves_next.get(&i).unwrap();
            for e in s {
                let e2 = mov(&e, i);
                //println!("moving? {:?} -> {:?}", e, e2);
                dest.entry(e2.clone()).or_insert(Vec::new());
                dest.get_mut(&e2).unwrap().push(e.clone());
            }
        }
        //println!("{:?}", dest);
        let m2 = map.clone();
        for k in dest.keys() {
            let v = dest.get(k).unwrap();
            if v.len() == 1 {
                //println!("moving! {:?}", v);
                let e = v.first().unwrap();
                map[e.y][e.x] = ',';
                map[k.y][k.x] = '#';
            }
        }
        //pp(&map);
        if m2 == map {
            //println!("p2 {}", step);
            p2r = step;
            running = false;
        }
        
        let df = dd.remove(0);
        dd.push(df);
        step += 1;
        if step == 11 {
            p1r = count(&map);
        }
    }
    //pp(&map);
    count(&map);
    println!("p1: {}", p1r);
    println!("p2: {}", p2r);
}
