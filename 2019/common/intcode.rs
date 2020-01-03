#[derive(Debug, Clone)]
pub struct VM {
    status: i64,
    position: usize,
    code: Vec<i64>,
    inputs: Vec<i64>,
    outputs: Vec<i64>,
    debug: bool
}

impl VM {
    pub fn new(code: Vec<i64>, inputs: Vec<i64>) -> VM {
        VM {
            status: 0,
            position: 0,
            code: code,
            inputs: inputs,
            outputs: Vec::new(),
            debug: false
        }
    }

    pub fn newd(code: Vec<i64>, inputs: Vec<i64>) -> VM {
        VM {
            status: 0,
            position: 0,
            code: code,
            inputs: inputs,
            outputs: Vec::new(),
            debug: true
        }
    }

    pub fn gbm(&mut self, pos: usize, mode: i64) -> i64 {
        match mode {
            1 => self.code[pos],
            _ => { let val = self.code[pos] as usize; self.code[val] }
        }
    }

    pub fn gbmo(&mut self, pos: usize, mode: i64) -> i64 {
        match mode {
            _ => self.code[pos]
        }
    }

    pub fn run(&mut self) {
        let mut finished = false;
        while !finished {
            let mut step_size = 4;
            let mut opcode = self.code[self.position];
            let par1 = (opcode / 100)   % 10;
            let par2 = (opcode / 1000)  % 10;
            let par3 = (opcode / 10000) % 10;
            opcode = opcode % 100;
            let params : Vec<i64> = vec![par1, par2, par3];
            if self.debug { println!("pos: {} opcode: {}", self.position, opcode); }
            if opcode == 1 { // ADD
                let a = self.gbm(self.position+1, params[0]);
                let b = self.gbm(self.position+2, params[1]);
                let pos_out = self.code[self.position+3];
                self.code[pos_out as usize] = a + b;
            } else if opcode == 2 { // MUL
                let a = self.gbm(self.position+1, params[0]);
                let b = self.gbm(self.position+2, params[1]);
                let pos_out = self.code[self.position+3];
                self.code[pos_out as usize] = a * b;
            } else if opcode == 3 { // INP
                let a = self.gbmo(self.position+1, params[0]);
                match self.inputs.pop() {
                    Some(x) => self.code[a as usize] = x,
                    None => {
                        finished = true;
                        println!("NO INPUT");
                    },
                }
                step_size = 2;
            } else if opcode == 4 { // OUT
                let a = self.gbm(self.position+1, params[0]);
                self.outputs.push(a);
                println!("OUTPUT: {}", a);
                step_size = 2;
            } else if opcode == 5 { // JMT
                let a = self.gbm(self.position+1, params[0]);
                if a != 0 {
                    let b = self.gbm(self.position+2, params[1]);
                    self.position = b as usize;
                    step_size = 0;
                } else {
                    step_size = 3;
                }
            } else if opcode == 6 { // JMF
                let a = self.gbm(self.position+1, params[0]);
                if a == 0 {
                    let b = self.gbm(self.position+2, params[1]);
                    self.position = b as usize;
                    step_size = 0;
                } else {
                    step_size = 3;
                }
            } else if opcode == 7 { // LT
                let a = self.gbm(self.position+1, params[0]);
                let b = self.gbm(self.position+2, params[1]);
                let pos_out = self.code[self.position+3];
                if a < b {
                    self.code[pos_out as usize] = 1;
                } else {
                    self.code[pos_out as usize] = 0;
                }
            } else if opcode == 8 { //EQ
                let a = self.gbm(self.position+1, params[0]);
                let b = self.gbm(self.position+2, params[1]);
                let pos_out = self.code[self.position+3];
                if a == b {
                    self.code[pos_out as usize] = 1;
                } else {
                    self.code[pos_out as usize] = 0;
                }
            } else if opcode == 99 {
                finished = true;
            } else {
                finished = true;
                println!("Unknown code {} at position {}", self.code[self.position], self.position);
            }
            self.position += step_size;
        }
    }

    pub fn code(&mut self) -> Vec<i64> {
        return self.code.clone();
    }

    pub fn outputs(&mut self) -> Vec<i64> {
        return self.outputs.clone();
    }

    pub fn pp(&mut self) {
        println!("--------------------------");
        println!("status  : {:?}", self.status);
        println!("position: {:?}", self.position);
        println!("code[]: : {:?}", self.code.len());
        println!("code:   : {:?}", self.code);
    }
}
