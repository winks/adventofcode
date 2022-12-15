use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::cmp;

#[derive(Debug, Eq, Hash, PartialEq)]
struct Pos {
    x: i32,
    y: i32,
}

fn dist(a: &Pos, b: &Pos) -> i32 {
    let dy = cmp::max(a.y, b.y) - cmp::min(a.y, b.y);
    let dx = cmp::max(a.x, b.x) - cmp::min(a.x, b.x);
    (dy + dx) as i32
}

fn f(pairs: &Vec<Vec<Pos>>, p1s: i32) -> Vec<Vec<i32>> {
    let mut row : Vec<Vec<i32>> = Vec::new();
    for p in pairs {
        let d = dist(&p[0], &p[1]);
        let mut vert = p[0].y - p1s;
        if vert < 0 {
            vert = p1s - p[0].y;
        }
        if vert <= d {
            let side = d - vert;
            let lo = cmp::min(p[0].x-side, p[0].x+side);
            let hi = cmp::max(p[0].x-side, p[0].x+side);
            row.push(vec![lo, hi]);
        }
    }
    row
}

fn main() {
	let args: Vec<String> = env::args().collect();
    let filename = args[1].clone();
    let mut test = false;
    if args.len() > 2 {
        test = true;
    }
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(&file);
    let mut pairs: Vec<Vec<Pos>> = Vec::new();

    for (_index, line) in reader.lines().enumerate() {
        let line = line.unwrap();
        let parts = line.split(": closest beacon is at ").collect::<Vec<&str>>();
        let pas = parts[0].split(", y=").collect::<Vec<&str>>();
        let sy : i32 = pas[1].parse().unwrap();
        let sx : i32 = pas[0].replace("Sensor at x=", "").parse().unwrap();
        let pab = parts[1].split(", ").collect::<Vec<&str>>();
        let bx : i32 = pab[0].replace("x=", "").parse().unwrap();
        let by : i32 = pab[1].replace("y=", "").parse().unwrap();
        let d = dist(&Pos{x: sx, y: sy}, &Pos{x: bx, y: by});
        println!("parts {:?} {},{} {},{} = {}", parts, sx, sy, bx, by, d);
        pairs.push(vec![Pos{x: sx, y: sy}, Pos{x: bx, y: by}]);
	}
    println!("----");
    let p2s = 0;
    let mut p1s : i32 = 2000000;
    let mut p2m : i32 = 4000000;
    if test {
        p1s = 10;
        p2m = 20;
    }

    let mut row : Vec<Vec<i32>> = f(&pairs, p1s);
    row.sort_by(|a,b| {
        if a[0] == b[0] {
            if a[1] < b[1]  { return cmp::Ordering::Less }
            return cmp::Ordering::Greater
        } else if a[0] < b[0] { return cmp::Ordering::Less }
        return cmp::Ordering::Greater
    });
    //println!("xx {:?}", row);
    let mi = row[0][0];
    let mut ma = row[0][1];
    for v in 1..row.len() {
        if ma + 1 < row[v][0] {
            panic!("aaa");
        }
        ma = cmp::max(ma, row[v][1]);
    }
    println!("p1: {}", (ma-mi));

    'out: for yy in p2s..p2m {
        //println!("! {:?}", yy);
        let mut row : Vec<Vec<i32>> = f(&pairs, yy);
        row.sort_by(|a,b| {
            if a[0] == b[0] {
                if a[1] < b[1]  { return cmp::Ordering::Less }
                return cmp::Ordering::Greater
            } else if a[0] < b[0] { return cmp::Ordering::Less }
            return cmp::Ordering::Greater
        });
        //println!("xx {:?}", row);
        let mut ma = row[0][1];
        for v in 1..row.len() {
            //println!("a {} {}", ma, row[v][0]);
            if ma + 1 < row[v][0]
                    && (ma+1) >= p2s
                    && (ma+1) <= p2m {
                let foo : i64 = ((ma+1) as i64)*4000000 + yy as i64;
                println!("p2: {}", foo);
                break 'out;
            }
            ma = cmp::max(ma, row[v][1]);
        }
    }
}
