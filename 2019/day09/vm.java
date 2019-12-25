import java.util.List;
import java.util.ArrayList;

class VM {
	private ArrayList<Long> ops;
	private ArrayList<Long> inputs;
	private ArrayList<Long> outputs;
	private boolean ran = false;
	private boolean debug = false;
	private long pos = 0;
	private long relPos = 0;

	public VM(ArrayList<Long> ops, ArrayList<Long> inputs) {
		this(ops, inputs, false);
	}

	public VM(ArrayList<Long> ops, ArrayList<Long> inputs, boolean debug) {
		ArrayList<Long> tmpOps = (ArrayList<Long>) ops.clone();
		ArrayList<Long> tmpIn = (ArrayList<Long>) inputs.clone();
		this.ops = tmpOps;
		this.inputs = inputs;
		this.debug = debug;
		this.outputs = new ArrayList<>();
		if (this.debug) {
			System.out.println("########## Booting up ##########");
			System.out.println("OPS    : " + this.ops.size());
			System.out.println("INPUTS : " + this.inputs.size());
			System.out.println("OUTPUTS: " + this.outputs.size());
		}
	}

	private void maybeResize(long val) {
		if (ops.size() <= val) {
			for (int i=ops.size(); i<=val+1; ++i) {
				ops.add(0L);
			}
		}
	}

	public void setPos(long n) {
		this.pos = n;
	}
	public void setRelPos(long n) {
		this.relPos = n;
		maybeResize(this.relPos);
	}
	public void setCodeAt(long p, long val) {
		ops.set((int)p, val);
	}
	public void setOutputs(ArrayList<Long> o) {
		outputs = o;
	}
	public void setInputs(ArrayList<Long> o) {
		inputs = o;
	}
	public void addInput(long o) {
		inputs.add(o);
	}
	public void addInput2(long o) {
		inputs.add(0, o);
	}

	public ArrayList<Long> getOutputs() {
		return outputs;
	}
	public ArrayList<Long> getInputs() {
		return inputs;
	}
	public ArrayList<Long> getOps() {
		return ops;
	}
	public boolean isStopped() {
		return ops.get((int)pos) == 99;
	}

	private long getIn(long opcode) {
		if (opcode == 1 || opcode == 2 || opcode == 5 || opcode == 6 || opcode == 7 || opcode == 8) {
			return 2;
		} else if (opcode == 4 || opcode == 9) {
			return 1;
		}
		return 0;
	}

	private long getOut(long opcode) {
		if (opcode == 1 || opcode == 2 || opcode == 3 || opcode == 7 || opcode == 8) {
			return 1;
		}
		return 0;
	}

	public void run() {
		ran = false;
		while (!isStopped()) {
			if (this.debug) System.out.println("AT POS "+pos);
			ran = true;
			long opcode = ops.get((int)pos) % 100;
			long numIn  = getIn(opcode);
			long numOut = getOut(opcode);

			ArrayList<Long> args = new ArrayList<Long>();
			long mode = (long) Math.floor(ops.get((int)pos) / 100.0);

			long posOut = 0;
			for (int i=0;i<numIn;++i) {
				long val = ops.get((int)(pos+i+1));
				if (mode % 10 == 0) {
					maybeResize(val);
					args.add(ops.get((int)val));
				} else if (mode % 10 == 1) {
					args.add(val);
				} else if (mode % 10 == 2) {
					args.add(ops.get((int)(relPos + val)));
				}
				mode = (long) Math.floor(mode / 10.0);
			}
			for (int i=0;i<numOut;++i) {
				if (mode % 10 == 0) {
					posOut = ops.get((int)(pos + numIn + 1));
				} else if (mode % 10 == 2) {
					posOut = relPos + ops.get((int)(pos + numIn + 1));
				}
				mode = (long) Math.floor(mode / 10.0);
			}
			if (this.debug) System.out.println("PRE: pos:" + pos + " []a= " + args.size() + " nI: " + numIn + " nO: " + numOut);

			if (opcode == 1) {
				maybeResize(posOut);
				ops.set((int)posOut, args.get(0) + args.get(1));
			} else if (opcode == 2) {
				maybeResize(posOut);
				ops.set((int)posOut, args.get(0) * args.get(1));
			} else if (opcode == 3) {
				if (inputs.size() > 0) {
					if (this.debug) System.out.println("READ IN: " + inputs.get(inputs.size()-1) + ", "+ (inputs.size()-1) + " left");
					ops.set((int)posOut, inputs.remove(inputs.size()-1));
				} else {
					if (this.debug) System.out.println("NO INPUT");
					return;
				}
			} else if (opcode == 4) {
				outputs.add(args.get(0));
				if (this.debug) System.out.println("OUTPUT: " + args.get(0));
			} else if (opcode == 5) {
				if (args.get(0) != 0) {
					pos = args.get((int)1);
					continue;
				}
			} else if (opcode == 6) {
				if (args.get(0) == 0) {
					pos = args.get((int)1);
					continue;
				}
			} else if (opcode == 7) {
				maybeResize(posOut);
				if (args.get(0) < args.get(1)) {
					ops.set((int)posOut, 1L);
				} else {
					ops.set((int)posOut, 0L);
				}
			} else if (opcode == 8) {
				maybeResize(posOut);
				if (args.get(0).equals(args.get(1))) {
					ops.set((int)posOut, 1L);
				} else {
					ops.set((int)posOut, 0L);
				}
			} else if (opcode == 9) {
				relPos += args.get(0);
			}
			pos += (numIn + numOut + 1);
		}
	}

	public String toString() {
		StringBuffer s = new StringBuffer();
		s.append("> VM: \n> pos: ");
		s.append(pos);
		s.append("\n> pos: ");
		s.append(relPos);
		s.append("> VM: \n> OPS[");
		s.append(ops.size());
		s.append("]:\t");
		for (int i = 0; i < ops.size()-1; ++i) {
			s.append(ops.get(i));
			s.append(',');
		}
		s.append(ops.get(ops.size()-1));

		s.append("\n> INPUTS[");
		s.append(inputs.size());
		s.append("]:\t");
		for (int i = 0; i < inputs.size()-1; ++i) {
			s.append(inputs.get(i));
			s.append(',');
		}
		if (inputs.size() > 0) s.append(inputs.get(inputs.size()-1));

		s.append("\n> OUTPUTS[");
		s.append(outputs.size());
		s.append("]:\t");
		for (int i = 0; i < outputs.size()-1; ++i) {
			s.append(outputs.get(i));
			s.append(',');
		}
		if (outputs.size() > 0) s.append(outputs.get(outputs.size()-1));

		return s.toString();
	}
}
