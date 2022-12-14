use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};

#[derive(Debug, PartialEq, Clone)]
enum Mat {
    Rock,
    Sand,
    Air,
}

#[derive(Debug, PartialEq, Clone)]
struct Pos {
    v: Mat,
}

fn pp(map: &Vec<Vec<Pos>>, my: usize, mx: usize) {
    if my > 20 {
        return
    }
    for y in 0..map.len() {
        for x in (mx-120)..map[0].len()-5 {
            let mut v = ".";
            if map[y][x].v == Mat::Rock {
                v = "#";
            } else if map[y][x].v == Mat::Sand {
                v = "o";
            }
            print!("{}", v);
        }
        println!("");
    }
}

fn main() {
	let args: Vec<String> = env::args().collect();
    let filename = args[1].clone();
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(&file);

    let mut map : Vec<Vec<Pos>> = Vec::new();
    let mut my = 175;
    let mut mx = 680;
    let mut max_y = 0;
    if args.len() > 2 && args[2] == "0" {
        my = 13;
        mx = 520;
    }
    for _y in 0..my {
        let mut r : Vec<Pos> = Vec::new();
        for _x in 0..mx {
            r.push(Pos{v: Mat::Air});
        }
        map.push(r);
    }
    for (_index, line) in reader.lines().enumerate() {
        let line = line.unwrap();
        let p = line.split(" -> ").collect::<Vec<&str>>();
        //println!("{:?}", p);
        for i in 1..p.len() {
            let s = p[i-1].split(",").collect::<Vec<&str>>();
            let e = p[i].split(",").collect::<Vec<&str>>();
            //println!("{} {:?} {:?}", i, s, e);
            let sy : usize = s[1].parse().unwrap();
            let sx : usize = s[0].parse().unwrap();
            let ey : usize = e[1].parse().unwrap();
            let ex : usize = e[0].parse().unwrap();
            if sy > max_y {
                max_y = sy;
            }
            if ey > max_y {
                max_y = ey;
            }
            if ey > sy {
                for ty in sy..ey+1 {
                    let tp = &mut map[ty];
                    tp[sx].v = Mat::Rock;
                }
            } else if sy > ey {
                for ty in ey..sy+1 {
                    let tp = &mut map[ty];
                    tp[sx].v = Mat::Rock;
                }
            } else if ey == sy {
                //println!("  {} {:?} {:?}", i, s, e);
                if sx > ex {
                    let tp = &mut map[sy];
                    //println!("{:?}", tp[ex]);
                    for tx in ex..sx+1 {
                        tp[tx].v = Mat::Rock;
                    }
                } else if ex > sx {
                    let tp = &mut map[sy];
                    for tx in sx..ex+1 {
                        tp[tx].v = Mat::Rock;
                    }
                } else if sx == ex {
                    panic!("foo");
                }
            }
        }
	}
    let tp = &mut map[max_y+2];
    for aa in 0..mx {
        tp[aa].v = Mat::Rock;
    }
    pp(&map, my, mx);
    println!("======");

    let mut falling = false;
    let mut cury = 0;
    let mut curx = 0;
    let mut num = 0;
    let mut p1 = 0;
    let mut p2 = 0;

    for step in 0..3310000 {
        println!("step: {} falling:{}", step, falling);
        if map[0][500].v == Mat::Sand && !falling {
            p2 = num;
            break;
        }
        if !falling {
            cury = 0;
            curx = 500;
            let trow1 = &mut map[cury];
            trow1[curx].v = Mat::Sand;
            falling = true;
            num += 1;
            println!(": new sand");
        } else {
            if map[cury+1][curx].v == Mat::Air {
                // down is empty
                println!("  down");
                let trow1 = &mut map[cury];
                trow1[curx].v = Mat::Air;
                let trow2 = &mut map[cury+1];
                trow2[curx].v = Mat::Sand;
                cury = cury+1;
            } else if map[cury+1][curx].v == Mat::Rock
                || map[cury+1][curx].v == Mat::Sand {
                print!("  flow?");
                // down left is empty
                if map[cury+1][curx-1].v == Mat::Air {
                    println!(" left");
                    let trow1 = &mut map[cury];
                    trow1[curx].v = Mat::Air;
                    let trow2 = &mut map[cury+1];
                    trow2[curx-1].v = Mat::Sand;
                    cury = cury + 1;
                    curx = curx - 1;
                } else if (map[cury+1][curx-1].v == Mat::Sand
                        || map[cury+1][curx-1].v == Mat::Rock)
                        && map[cury+1][curx+1].v == Mat::Air {
                    // down left is rock/sand, down right is empty
                    println!(" right");
                    let trow1 = &mut map[cury];
                    trow1[curx].v = Mat::Air;
                    let trow2 = &mut map[cury+1];
                    trow2[curx+1].v = Mat::Sand;
                    cury = cury + 1;
                    curx = curx + 1;
                } else {
                    println!(" nope");
                    falling = false;
                    if cury > max_y && p1 == 0 {
                        p1 = num - 1;
                    }
                }
            }
        }
        pp(&map, my, mx);
        println!("sand: {}\n", num);
    }
    println!("p1: {}", p1);
    println!("p2: {}", p2);
}
