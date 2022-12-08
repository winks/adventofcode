use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::collections::HashSet;
use std::iter::FromIterator;

fn main() {
	let args: Vec<String> = env::args().collect();
    let filename = args[1].clone();
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(&file);

    let mut p1 = 0;
    let mut p2 = 0;
    let pkg = 4;
    let msg = 14;
    'outer: for (_index, line) in reader.lines().enumerate() {
        let line = line.unwrap();
        let p : Vec<char> = line.chars().collect();

        for i in (pkg-1)..p.len() {
            let cur : Vec<char> = p.clone().splice(i+1-pkg..i+1, Vec::new()).collect();
            let set : HashSet<char> = HashSet::from_iter(cur);
            if set.len() == pkg {
                p1 = i;
                break;
            }
        }
        for i in msg..p.len()+1 {
            if i+1 > p.len() {
                continue
            }
            let cur : Vec<char> = p.clone().splice(i-msg..i, Vec::new()).collect();
            //println!("{:?}", cur);
            let set : HashSet<char> = HashSet::from_iter(cur);
            //println!("{:?}", set);
            if set.len() == msg {
                p2 = i;
                break 'outer;
            }
        }
	}
    println!("p1: {}", p1+1);
    println!("p2: {}", p2);
}
