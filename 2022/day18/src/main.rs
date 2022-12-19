use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::collections::HashMap;

#[derive(Debug, Clone)]
struct Point {
    x: i32,
    y: i32,
    z: i32,
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let filename = args[1].clone();
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(&file);

    let mut minz : i32 = 0;
    let mut maxz : i32 = 0;
    let mut minx : i32 = 0;
    let mut maxx : i32 = 0;
    let mut miny : i32 = 0;
    let mut maxy : i32 = 0;

    let mut layers : HashMap<i32, Vec<Point>> = HashMap::new();
    for (index, line) in reader.lines().enumerate() {
        let line = line.unwrap();
        let co : Vec<&str> = line.split(",").collect::<Vec<&str>>();
        let x : i32 = co[0].parse().unwrap();
        let y : i32 = co[1].parse().unwrap();
        let z : i32 = co[2].parse().unwrap();
        layers.entry(z).or_insert(Vec::new());
        let cur = layers.get_mut(&z).unwrap();
        cur.push(Point{x: x, y: y, z: z});
        println!("{}, {}, {}", x, y, z);
        if z < minz {
            minz = z;
        }
        if z > maxz {
            maxz = z;
        }
        if x < minx {
            minx = x;
        }
        if x > maxx {
            maxx = x;
        }
        if y < miny {
            miny = y;
        }
        if y > maxy {
            maxy = y;
        }
    }
    if !layers.contains_key(&0) {
        minz = 1;
    }
    for ll in minz..maxz+1 {
        println!("{} {:?}", ll, layers.get(&ll));
    }
    println!("---------------------- {} {}", minz, maxz);

    let mut sp1 : usize = 0;
    let mut sp2 : usize = 0;
    let mut num : usize;
    for n in minz..maxz+1 {
        num = 0;
        //let mut last : Vec<Point> = Vec::new();
        let cur = layers.get(&n).unwrap();
        println!(":: {}, len: {}", n, cur.len());
        // absolute bottom
        if n == minz {
            num += cur.len();
        } else {
            let last = layers.get(&(n-1)).unwrap();
            // bottom
            for p1 in cur {
                let mut tmp = 2;
                for p2 in last {
                    if p1.x == p2.x && p1.y == p2.y {
                        tmp -= 2;
                        break;
                    }
                }
                num += tmp;
            }
        }
        // sides
        for p1 in cur {
            let mut tmp = 4;
            for p2 in cur {
                if p1.x == p2.x && p1.y == p2.y {
                    continue
                }
                if (p1.x - p2.x).abs() + (p1.y - p2.y).abs() == 1 {
                    tmp -= 1;
                    println!("-1 {:?} {:?}", p1, p2)
                }
            }
            println!("tmp {}", tmp);
            num += tmp;
        }
        // top
        if n == maxz{
            num += cur.len();
        }
        sp1 += num;
        sp2 += num;
        if n > minz && n < maxz && cur.len() > 3 {
            for x in minx..(maxx+1) {
                for y in miny..(maxy+1) {
                    let mut ne = 0;
                    let mut myself = false;
                    for p in cur {
                        if (p.y == y && (p.x == x-1 || p.x == x+1))
                            || (p.x == x && (p.y == y-1 || p.y == y+1)) {
                            ne += 1;
                        }
                        if p.x == x && p.y == y {
                            myself = true;
                        }
                    }
                    if !myself && ne == 4 {
                        sp2 -= 6;
                    }
                    if n == 5 {
                        println!("x: {} y:{} ne: {} my: {}", x, y, ne, myself);
                    }
                }
            }
        }
        println!("= {} (total p1: {} p2: {})", num, sp1, sp2);
    }
}
