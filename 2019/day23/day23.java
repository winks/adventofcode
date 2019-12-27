import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.time.Instant;

class Day23 {
	public static void main(String[] args) throws java.io.FileNotFoundException, InterruptedException {
		if (args.length < 1) {
			System.out.println("Usage: NAME /path/to/input");
			return;
		}
		String fname = args[0];
		List<String> data = new ArrayList<String>();
		Scanner sc = new Scanner(new File(fname));

		while (sc.hasNextLine()) {
			String x = sc.nextLine();
			data.add(x);
		}
		System.out.println("Lines: " + data.size());

		ArrayList<Long> ops = new ArrayList<Long>();
		for (String ls : data) {
			for (String lsi : ls.split(",")) {
				ops.add(Long.parseLong(lsi));
			}
		}
		System.out.println("Ops: " + ops.size());

		String p1 = go(ops, false);
		String p2 = go(ops, true);
		System.out.println(p1);
		System.out.println(p2);
	}

	private static void show(List<Long> v) {
		show(v, 50);
	}

	private static void show(List<Long> v, int max) {
		StringBuffer s = new StringBuffer();
		max = Math.min(max, v.size()-1);
		for (int i=0;i<max;++i) {
			s.append(v.get(i));
			s.append(",");
		}
		if (max > 0) s.append(v.get(max));
		System.out.println(s);
	}

	private static void tp(String s) {
		System.out.println(Instant.now().toString() + " " +s);
	}

	private static String go(ArrayList<Long> ops, boolean part2) throws InterruptedException {
		int sz = 50;

		VM[] vms = new VM[sz];
		ArrayList<Long> check = new ArrayList<Long>();

		for (int i = 0; i<sz; ++i) {
			vms[i] = new VM(ops, new ArrayList<Long>());
			vms[i].addInput(Long.valueOf(i));
		}

		long natx = 0;
		long naty = 0;
		long lastnaty = -1;
		boolean finished = false;

		int i = 0;
		while (!finished) {
			int numIdle = 0;

				tp("Next is "+i);

				if (vms[i].getInputs().size() == 0) {
					vms[i].addInput(Long.valueOf(-1));
				}
				vms[i].run();
				ArrayList<Long> out = vms[i].getOutputs();
				int idx = 0;
				long addr = -1;
				long x = -1;
				long y = -1;
				if (out.size() > 0) {
					show(out);
					while (out.size() > 0) {
						addr = out.remove(0);
						x = out.remove(0);
						y = out.remove(0);
						if (!part2) {
							return "Part 1: " + y;
						}
						tp("Sending from "+i+" to " + addr + ": ("+x+"/"+y+")");
						if ((int)addr == 255) {
							natx = x;
							naty = y;
						} else {
							vms[(int)addr].addInput2(x);
							vms[(int)addr].addInput2(y);
						}
					}
					vms[i].setOutputs(new ArrayList<Long>());
				}

			for (int ia = 0; ia<sz; ++ia) {
				numIdle += vms[ia].getInputs().size();
			}

			tp("IDLE: "+numIdle+" @ "+natx+"/"+naty);
			if (numIdle == 0 && (natx != 0 || naty != 0)) {
				tp("ALL IDLE, SENDING "+natx+"/"+naty);
				vms[0].addInput(naty);
				vms[0].addInput(natx);
				if (naty == lastnaty) {
					tp("Sending again: " +naty);
					if (part2) {
						return "Part 2: " + naty;
					}
				}
				lastnaty = naty;
			}

			++i;
			if (i > 49) i = 0;
		}
		return "";
	}
}
