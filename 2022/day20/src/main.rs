use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};

#[derive(Hash, Clone, PartialEq, Debug)]
struct T {
    v: i64,
    p: usize,
}

fn main() {
	let args: Vec<String> = env::args().collect();
    let filename = args[1].clone();
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(&file);

    let p2f : i64 = 811589153;
    let mut num : Vec<T> = Vec::new();
    let mut nump2 : Vec<T> = Vec::new();
    for (index, line) in reader.lines().enumerate() {
        let line = line.unwrap();
        let n : i64 = line.parse().unwrap();
        num.push(T{v: n, p: index});
        nump2.push(T{v: n * p2f, p: index});
	}
    let vlen = num.len();

    // p1
    let numx = num.clone();
    for n2 in numx {
        let pos = num.iter().position(|r| r == &n2).unwrap();
        let np : i64 = (pos as i64 + n2.v).rem_euclid(vlen as i64 - 1);
        //println!("n= {} @ {} > {}", n2.v, pos, np);
        num.remove(pos);
        num.insert(np as usize, n2);
    }
    let pos0 = num.iter().position(|r| r.v == 0).unwrap();
    let a = (pos0+1000).rem_euclid(vlen);
    let b = (pos0+2000).rem_euclid(vlen);
    let c = (pos0+3000).rem_euclid(vlen);

    // p2
    let nump2s = nump2.clone();
    for _i in 1..11 {
        for n2 in &nump2s {
            let pos = nump2.iter().position(|r| r == n2).unwrap();
            let np : i64 = (pos as i64 + n2.v).rem_euclid(vlen as i64 - 1);
            //println!("n= {} @ {} > {}", n2.v, pos, np);
            let x = nump2.remove(pos);
            //println!("mid : {:?}", num);
            nump2.insert(np as usize, x);
        }
    }
    let pos02 = nump2.iter().position(|r| r.v == 0).unwrap();
    let a2 = (pos02+1000).rem_euclid(vlen);
    let b2 = (pos02+2000).rem_euclid(vlen);
    let c2 = (pos02+3000).rem_euclid(vlen);

    println!("p1: {}", num[a].v + num[b].v + num[c].v);
    println!("p2: {}", nump2[a2].v + nump2[b2].v + nump2[c2].v);
}
