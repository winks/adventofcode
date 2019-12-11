import fs from 'fs';
import argv from 'process';

const OP_ADD = 1;
const OP_MUL = 2;
const OP_HLT = 99;

function getArgsIn(op: number) {
    switch(op) {
        case OP_ADD: return 2;
        case OP_MUL: return 2;
        case OP_HLT: return 0;
        default: return 0;
    }
}

function getArgsOut(op: number) {
    switch(op) {
        case OP_ADD: return 1;
        case OP_MUL: return 1;
        case OP_HLT: return 0;
        default: return 0;
    }
}

//let instruction: [number, Array<number>];

function calc(dtx: {position: number, status: number, ops: number[]}) {
    var op = dtx.ops[dtx.position];
    var argsIn = getArgsIn(op);
    var argsOut = getArgsOut(op);
    
    var paramsIn: number[] = [];
    for (var i=0; i<argsIn;++i) {
        var pos = dtx.ops[dtx.position+1+i];
        paramsIn.push(dtx.ops[pos]);
    }
    var paramOut: number = 0;
    if (argsOut > 0) {
        paramOut = dtx.ops[dtx.position+1+argsIn]
    }
    
    if (op == OP_HLT) {
        console.log("#OP_HLT @" + dtx.position);
        dtx.status = 10;
        return dtx;
    } else if (op == OP_ADD) {
        dtx.ops[paramOut] = paramsIn[0] + paramsIn[1];
        console.log("#OP_ADD @" + dtx.position + " " + paramsIn + " " + paramOut+" = "+dtx.ops[paramOut]);
    } else if (dtx.ops[dtx.position] == OP_MUL) {
        console.log("#OP_MUL @" + dtx.position + " " + paramsIn + " " + paramOut);
        dtx.ops[paramOut] = paramsIn[0] * paramsIn[1];
    } else {
        dtx.status = 10;
    }

    dtx.position = dtx.position + 1 + argsIn + argsOut;
    return dtx;
}

function main() {
    var inp = "";
    //process.argv.forEach((val, index) => {
    //    console.log(`${index}: ${val}`)
    //})
    var fname: string = ""
    if (process.argv.length < 3) {
        return 1;
    }
    fname = process.argv[2];
    if (fname.length < 1) {
        return 1;
    }
    inp = fs.readFileSync(fname,'utf8');
    if (inp.length < 1) {
        return 1;
    }

    var opsStr = inp.split(',');
    var opsNum = opsStr.map(function(o) {
        return parseInt(o, 10);
    });
    console.log(opsNum);

    // 12 + 2 for part1
    if (process.argv.length > 3) opsNum[1] = parseInt(process.argv[3]);
    if (process.argv.length > 4) opsNum[2] = parseInt(process.argv[4]);

    var data = {
        position: 0, 
        status: 0, 
        ops: opsNum
    };
    console.log(data);

    do {
        data = calc(data);
        console.log(data);
    } while (data.position < data.ops.length && data.status == 0)
}

main();