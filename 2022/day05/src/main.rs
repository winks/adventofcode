use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::collections::HashMap;

fn main() {
	let args: Vec<String> = env::args().collect();
    let filename = args[1].clone();
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(&file);

    let mut piles = HashMap::<usize, Vec<String>>::new();
    let mut piles2 = HashMap::<usize, Vec<String>>::new();
    let mut max = 0;

    for (_index, line) in reader.lines().enumerate() {
        let line = line.unwrap();
        if line.len() < 1 || &line[0..3] == " 1 " {
        } else if &line[0..1] == "m" {
            println!("! {}", line);
            let parts = line.split(" ").collect::<Vec<&str>>();
            let num : usize = parts[1].parse().unwrap();
            let src : usize = parts[3].parse().unwrap();
            let dst : usize = parts[5].parse().unwrap();

            //p1
            for _i in 0..num {
                //println!("+ {}", i);
                let src_p = piles.get_mut(&(src - 1)).unwrap();
                let cur = src_p.pop().unwrap();
                let dst_p = piles.get_mut(&(dst - 1)).unwrap();
                dst_p.push(cur);
            }
            
            // p2
            let src_p2 = piles2.get_mut(&(src - 1)).unwrap();
            let rest = src_p2.len() - num;
            let mut cur2 = src_p2.split_off(rest);
            //println!("tmp {:?}", cur2);
            let dst_p2 = piles2.get_mut(&(dst - 1)).unwrap();
            for _i in 0..cur2.len() {
                let c2 = cur2.remove(0);
                dst_p2.push(c2);
            }
            
            if src > max {
                max = src
            }
            if dst > max {
                max = dst
            }
            //println!("---x1 {:?}", piles.clone());
            //println!("---x2 {:?}", piles2.clone());
        } else {
            for i in 1..line.len() {
                let cur = &line[i..i+1];
                if cur == " " || cur == "[" || cur == "]" {
                    continue
                }
                let cur1 = cur.to_string();
                let cur2 = cur.to_string();
                
                let col = (i-1) / 4;
                //println!("col {} {}", col, cur);
                if !piles.contains_key(&col) {
                    piles.insert(col, vec![cur1]);
                } else {
                    if let Some(v) = piles.get_mut(&col) {
                        v.insert(0, cur1);
                    }
                }
                if !piles2.contains_key(&col) {
                    piles2.insert(col, vec![cur2]);
                } else {
                    if let Some(v) = piles2.get_mut(&col) {
                        v.insert(0, cur2);
                    }
                }
            }
            println!("--- {:?}", piles.clone())
        }
	}
    print!("p1: ");
    for i in 0..max {
        let p = piles.get_mut(&i).unwrap();
        print!("{}", p.pop().unwrap());
    }
    println!("");
    print!("p2: ");
    for i in 0..max {
        let p = piles2.get_mut(&i).unwrap();
        print!("{}", p.pop().unwrap());
    }
    println!("")
}
