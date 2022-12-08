use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
	let args: Vec<String> = env::args().collect();
    let filename = args[1].clone();
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(&file);

    let mut p1 = 0;
    let mut p2 = 0;
    let mut map : Vec<Vec<u32>> = Vec::new();
    for (_index, line) in reader.lines().enumerate() {
        let line = line.unwrap();
        let mut row : Vec<u32> = Vec::new();

        //let trees : Vec<char> = line.chars().collect();
        for i in 0..line.len() {
            let t : u32 =  line[i..i+1].parse().unwrap();
            row.push(t);
        }
        //println!("{:?}", row);
        map.push(row);
	}
    println!("");

    for r in 1..map.len()-1 {
        for c in 1..map[0].len()-1 {
            let cur = map[r][c];
            //print!("{}", cur);
            let mut left = map[r].clone();
            let left1 : Vec<u32> = left.splice(0..c, Vec::new()).collect();
            let left2 = left1.clone().into_iter().filter(|&x|x < cur).collect::<Vec<_>>();
            //println!("{:?} :: {:?}", left1, left2);
            if left2.len() == left1.len() {
                p1 += 1;
                //println!("{:?} @ r {:?} c {:?} vis left", cur, r, c);
                continue
            }
            let mut right = map[r].clone();
            let right1 : Vec<u32> = right.splice(c+1..map[0].len(), Vec::new()).collect();
            let right2 = right1.clone().into_iter().filter(|&x|x < cur).collect::<Vec<_>>();
            //println!("{:?} :: {:?}", right1, right2);
            if right1.len() == right2.len() {
                p1 += 1;
                //println!("{:?} @ r {:?} c {:?} vis right", cur, r, c);
                continue
            }
            let mut top1 : Vec<u32> = Vec::new();
            for t in 0..r {
                top1.push(map[t][c]);
            }
            let top2 = top1.clone().into_iter().filter(|&x|x < cur).collect::<Vec<_>>();
            //println!("{:?} :: {:?}", top1, top2);
            if top1.len() == top2.len() {
                p1 += 1;
                //println!("{:?} @ r {:?} c {:?} vis top", cur, r, c);
                continue
            }

            let mut bot1 : Vec<u32> = Vec::new();
            for b in r+1..map[0].len() {
                bot1.push(map[b][c])
            }
            let bot2 = bot1.clone().into_iter().filter(|&x|x < cur).collect::<Vec<_>>();
            //println!("{:?} :: {:?}", bot1, bot2);
            if bot1.len() == bot2.len() {
                p1 += 1;
                //println!("{:?} @ r {:?} c {:?} vis right", cur, r, c);
                continue
            }
            //println!("");
        }
        //println!("===");
    }

    for r in 1..map.len()-1 {
        for c in 1..map[0].len()-1 {
            let mut vismap : Vec<u32> = Vec::new();
            let cur = map[r][c];
            let mut vis = 0;

            for c2 in (0..c).rev() {
                if map[r][c2] < cur {
                    vis += 1;
                } else {
                    vis +=1;
                    break;
                }
            }
            vismap.push(vis);
            vis = 0;
            for c2 in c+1..map[0].len() {
                if map[r][c2] < cur {
                    vis += 1;
                } else {
                    vis +=1;
                    break;
                }
            }
            vismap.push(vis);
            vis = 0;
            for r2 in (0..r).rev() {
                if map[r2][c] < cur {
                    vis += 1;
                } else {
                    vis +=1;
                    break;
                }
            }
            vismap.push(vis);
            vis = 0;
            for r2 in r+1..map[0].len() {
                if map[r2][c] < cur {
                    vis += 1;
                } else {
                    vis +=1;
                    break;
                }
            }
            vismap.push(vis);

            //println!("+ {} @ ({},{}) {:?}", cur, r, c, vismap);
            let mul = vismap.iter().product();
            if mul > p2 {
                p2 = mul;
            }    
        }
    }

    p1 += 2 * map[0].len() + 2 * (map[0].len()-2);
    println!("p1: {}", p1);
    println!("p2: {}", p2);
}
