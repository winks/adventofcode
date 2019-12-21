import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

class Day21 {
	public static void main(String[] args) throws java.io.FileNotFoundException {
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

		//tests();
		part1(ops);
		part2(ops);
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

	private static void showAscii(List<Long> v) {
		StringBuffer s = new StringBuffer();
		for (int i=0;i<v.size();++i) {
			s.append(toAscii(v.get(i)));
		}
		System.out.println(s);
	}

	private static char toAscii(long v) {
		char c = (char) v;
		return c;
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

	private static void part1(ArrayList<Long> ops) {
		ArrayList<String> instr = new ArrayList<String>();

		instr.add("OR C J");
		instr.add("AND A J");
		instr.add("NOT J J");
		instr.add("AND D J");
		instr.add("WALK");

		ArrayList<Long> in = fromAscii(instr);
		show(in);
		VM vm = new VM(ops, in);
		vm.run();
	}

	private static void part2(ArrayList<Long> ops) {
		ArrayList<String> instr = new ArrayList<String>();

		instr.add("OR H J");
		instr.add("AND D J");

		instr.add("OR C T");
		instr.add("AND B T");
		instr.add("NOT T T");
		instr.add("AND T J");

		instr.add("NOT A T");
		instr.add("OR T J");

		instr.add("RUN");

		ArrayList<Long> in = fromAscii(instr);
		show(in);
		VM vm = new VM(ops, in);
		vm.run();
	}

	private static void tests() {
		test1();
		test2();
		test3();
		test4();
		test5();
		test6();
	}

	private static void test1() {
		int[] arr = {1,0,0,0,99};
		ArrayList<Long> ops = new ArrayList<Long>();
		ArrayList<Long> in  = new ArrayList<Long>();

		for (int i : arr) {
			ops.add(Long.valueOf(i));
		}

		VM vm = new VM(ops, in);
		vm.run();
		List<Long> rv = vm.getOps();
		System.out.println("==========");
		show(ops);
		show(rv);
	}

	private static void test2() {
		int[] arr = {2,3,0,3,99};
		ArrayList<Long> ops = new ArrayList<Long>();
		ArrayList<Long> in  = new ArrayList<Long>();

		for (int i : arr) {
			ops.add(Long.valueOf(i));
		}

		VM vm = new VM(ops, in);
		vm.run();
		List<Long> rv = vm.getOps();
		System.out.println("==========");
		show(ops);
		show(rv);
	}

	private static void test3() {
		int[] arr = {2,4,4,5,99,0};
		ArrayList<Long> ops = new ArrayList<Long>();
		ArrayList<Long> in  = new ArrayList<Long>();

		for (int i : arr) {
			ops.add(Long.valueOf(i));
		}

		VM vm = new VM(ops, in);
		vm.run();
		List<Long> rv = vm.getOps();
		System.out.println("==========");
		show(ops);
		show(rv);
	}

	private static void test4() {
		int[] arr = {1, 1, 1, 4, 99, 5, 6, 0, 99};
		ArrayList<Long> ops = new ArrayList<Long>();
		ArrayList<Long> in  = new ArrayList<Long>();

		for (int i : arr) {
			ops.add(Long.valueOf(i));
		}

		VM vm = new VM(ops, in);
		vm.run();
		List<Long> rv = vm.getOps();
		System.out.println("==========");
		show(ops);
		show(rv);
	}

	private static void test5() {
		int[] arr = {1002, 4, 3, 4, 33, 99};
		int[] exp = {1002, 4, 3, 4, 99, 99};
		ArrayList<Long> ops = new ArrayList<Long>();
		ArrayList<Long> in  = new ArrayList<Long>();

		for (int i : arr) {
			ops.add(Long.valueOf(i));
		}

		VM vm = new VM(ops, in);
		vm.run();
		List<Long> rv = vm.getOps();
		System.out.println("==========");
		show(ops);
		show(rv);
	}

	private static void test6() {
		int[] arr = {1101, 100, -1, 4, 0, 99};
		int[] exp = {1101, 100, -1, 4, 99, 99};
		ArrayList<Long> ops = new ArrayList<Long>();
		ArrayList<Long> in  = new ArrayList<Long>();

		for (int i : arr) {
			ops.add(Long.valueOf(i));
		}

		VM vm = new VM(ops, in);
		vm.run();
		List<Long> rv = vm.getOps();
		System.out.println("==========");
		show(ops);
		show(rv);
	}
}
