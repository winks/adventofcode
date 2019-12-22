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

	private static String getTile(int type) {
		switch(type) {
		case 4 : return "#";
		case 6 : return ".";
		case 8 : return "o";
		case 9 : return "D";
		default: return " ";
		}
	}

	private static void showImage(int[][] image) {
		int bmin = 0;
		int bmax = 0;

		int minw = 0;
		int maxw = 100;
		int minh = 0;
		int maxh = 100;

		for (int j = 0; j < 100; ++j) {
			for (int i = 0; i < 100; ++i) {
				if (image[i][j] != 0) {
					minw = Math.max(minw+2, i);
					maxw = Math.min(maxw-2, i);

					minh = Math.max(minh+2, j);
					maxh = Math.min(maxh-1, j);
				}
			}
		}
System.out.println("> im " + minw + " " + maxw + " " + minh + " " + maxh);

		StringBuffer s = new StringBuffer();
		for (int j = maxh; j < minh; ++j) {
			s.append("|");
			s.append( (j<10) ? " " : "" );
			s.append(j);
			s.append("| ");
			for (int i = maxw; i < minw; ++i) {
				s.append(getTile(image[i][j]));
			}
			s.append("\n");
		}
		s.append("|   ");
		for (int i = maxw; i < minw; ++i) {
			if (i % 2 ==  0) {
				if (i < 10) s.append(i);
				else s.append(i % 10);
			} else s.append(" ");
		}
		s.append("\n");
		s.append("\n");
		System.out.println(s.toString());
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
		int[][] image = new int[100][100];

		ArrayList<Long> in = new ArrayList<Long>();
		in.add(1L);
		show(in);

		int j = 0;
		int x = 50;
		int y = 50;
		int direc = 1;
		Point cur = new Point(x, y);
		Point last = new Point(x, y);
		ArrayList<Point> neighbors = new ArrayList<Point>(4);

		do {
			VM vm = new VM(ops, in);
			vm.run();
			ops = vm.getOps();

			long lout = -1;
			List<Long> outputs = vm.getOutputs();
			if (outputs.size() > 0) {
				lout = outputs.get(0);
			}
			if (lout == 2) { // found
				System.out.println("FOUND OXYGEN: " + cur);
				image[cur.x][cur.y] = 8;
				break;
			} else if (lout == 1) { // ok
				System.out.println("WAY: " + last + " > " + cur);
				cur = Point.where(cur, direc);
				image[last.x][last.y] = 6;
				image[cur.x][cur.y] = 9;
				in.add(Long.valueOf(direc));
				
			} else if (lout == 0) { // wall
				System.out.println("WALL: " + cur);
				Point w = Point.where(cur, direc);
				image[w.x][w.y] = 4;
			} else {
				System.out.println("ERROR OUT: " + lout);
			}
			showImage(image);
			++j;
			last = cur;
		} while (j < 13);
	}

	private static void part2(ArrayList<Long> ops) {
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
