import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.time.Instant;

class Benchmark {

	private static List<String> readLines(String fname) throws java.io.FileNotFoundException {
		List<String> data = new ArrayList<String>();

		Scanner sc = new Scanner(new File(fname));

		while (sc.hasNextLine()) {
			String x = sc.nextLine();
			data.add(x);
		}
		System.out.println("Lines: " + data.size());

		return data;
	}

	public static void main(String[] args) throws java.io.FileNotFoundException, InterruptedException {
		if (args.length < 1) {
			System.out.println("Usage: NAME /path/to/input [list,of,inputs]");
			return;
		}

		ArrayList<Long> ops = new ArrayList<Long>();
		ArrayList<Long> inputs = new ArrayList<Long>();

		List<String> data = readLines(args[0]);
		for (String ls : data) {
			for (String lsi : ls.split(",")) {
				ops.add(Long.parseLong(lsi));
			}
		}
		System.out.println("Ops: " + ops.size());

		if (args.length > 1) {
			for (String lsi : args[1].split(",")) {
				inputs.add(0, Long.parseLong(lsi));
			}
			System.out.println("In : " + inputs.size());
		}

		String rv = go(ops, inputs);
		System.out.println(rv);
	}

	private static void show(List<Long> v) {
		show(v, 50);
	}

	private static void show(List<Long> v, int max) {
		StringBuffer s = new StringBuffer();
		max = Math.min(max, v.size()-1);
		for (int i=0;i<max;++i) {
			s.append(v.get(i));
			s.append(" ");
			if (i % 40 == 0) s.append("\n");
		}
		s.append(v.get(max));
		System.out.println(s);
	}

	private static String showAscii(List<Long> v) {
		StringBuffer s = new StringBuffer();
		for (int i=0;i<v.size();++i) {
			s.append(toAscii(v.get(i)));
		}
		System.out.println(s);
		return s.toString();
	}

	private static char toAscii(long v) {
		char c = (char) v;
		return c;
	}

	private static ArrayList<Long> fromAscii(String line) {
		ArrayList<String> sl = new ArrayList<String>(1);
		sl.add(line);
		return fromAscii(sl);
	}

	private static ArrayList<Long> fromAscii(ArrayList<String> lines) {
		ArrayList<Long> rv = new ArrayList<Long>();

		for (int i=lines.size()-1; i>=0; --i) {
			rv.add(10L);
			String line = lines.get(i);
			for (int j=line.length()-1; j>=0; --j) {
				char c = line.charAt(j);
				rv.add((long)c);
			}
		}

		return rv;
	}

	private static void tp(String s) {
		System.out.println(Instant.now().toString() + " " +s);
	}

	private static String go(ArrayList<Long> ops, ArrayList<Long> inputs) throws InterruptedException {

		VM vm = new VM(ops, inputs, false);

		boolean finished = false;

		int idx = 0;
		while (!finished /*&& todo.size() > 0 */ && idx < 20000) {
			vm.run();
			ArrayList<Long> out = vm.getOutputs();
			System.out.println("====================================================" + out.size());
			show(out);
			finished = true;
		}
		return "";
	}
}
