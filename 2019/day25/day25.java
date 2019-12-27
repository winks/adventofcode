import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.time.Instant;

class Day25 {
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

		String p1 = go(ops);
		System.out.println(p1);
	}

	private static void showImage(int[][] image) {
		int bmin = 0;
		int bmax = 0;

		int minw = 30;
		int maxw = 80;
		int minh = 30;
		int maxh = 80;

		for (int j = 0; j < 100; ++j) {
			for (int i = 0; i < 100; ++i) {
				if (image[i][j] != 0) {
					minw = Math.max(minw, i);
					maxw = Math.min(maxw, i);

					minh = Math.max(minh, j);
					maxh = Math.min(maxh, j);
				}
			}
		}
		//System.out.println("> im " + minw + " " + maxw + " " + minh + " " + maxh);
		minw = minw + 1;
		maxw = maxw - 1;
		minh = minh + 1;
		maxh = maxh - 1;

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
		s.append("|    ");
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
		if (max > 0) s.append(v.get(max));
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

	private static ArrayList<String> getDoors(String s) {
		ArrayList<String> sl = new ArrayList<String>();
		String ck = "Doors here lead:";
		if (!s.contains(ck)) return sl;
		int p1 = s.indexOf(ck)+ck.length()+1;
		int p2 = 0;
		int p9 = s.indexOf("Command?");
		if (p9 < 0) return sl;
		String rest = s.substring(p1, p9);
		//System.out.println(">>>"+rest+"<<<");
		boolean finished = false;
		while (!finished) {
			p2 = rest.indexOf('\n');
			if (p2 < 0) return sl;
			String line = rest.substring(0,p2);
			if (line.startsWith("- ")) line = line.substring(2);
			else break;
			sl.add(line);
			rest = rest.substring(p2+1);
		}
		for (int j=0; j<sl.size(); ++j) {
			System.out.println("DOOR>" + sl.get(j) + "<");
		}
		return sl;
	}

	private static ArrayList<String> getItems(String s) {
		ArrayList<String> sl = new ArrayList<String>();
		String ck = "Items here:";
		if (!s.contains(ck)) return sl;
		int p1 = s.indexOf(ck)+ck.length()+1;
		int p2 = 0;
		String rest = s.substring(p1);
		System.out.println(">>>"+rest+"<<<");
		boolean finished = false;
		while (!finished) {
			p2 = rest.indexOf('\n');
			if (p2 < 0) return sl;
			String line = rest.substring(1,p2);
			if (line.endsWith(".")) line = line.substring(0, line.length()-1);
			sl.add(line);
			break;
		}
		for (int j=0; j<sl.size(); ++j) {
			System.out.println("ITEM>" + sl.get(j) + "<");
		}
		return sl;
	}

	private static String getTile(int type) {
		switch(type) {
		case 3 : return ":";
		case 4 : return "#";
		case 6 : return ".";
		case 7 : return "x";
		case 9 : return "D";
		case 0 : return " ";
		default: return ""+type;
		}
	}

	private static String go(ArrayList<Long> ops) throws InterruptedException {
		int[][] image = new int[100][100];
		int x = 50;
		int y = 50;
		Point cur = new Point(x, y);
		Point last = new Point(x, y);
		Point next = new Point(x, y);
		ArrayList<Long> check = new ArrayList<Long>();
		ArrayList<String> inv = new ArrayList<String>();
		ArrayList<String> doors = new ArrayList<String>();
		ArrayList<String> newItems = new ArrayList<String>();
		ArrayList<Point> todo = new ArrayList<Point>();
		ArrayList<Point> neighbors = new ArrayList<Point>();
		ArrayList<Point> doorNeighbors = new ArrayList<Point>();

		String line = "";
		//ArrayList<Long> ins = fromAscii(line);
		ArrayList<Long> ins = new ArrayList<Long>();
		VM vm = new VM(ops, ins, true);
		long temp = -40;

		boolean finished = false;
		boolean moved = true;

		// 6 = visited
		// 7 = deadend
		// 4 = wall
		// 3 = door

		int idx = 0;
		while (!finished /*&& todo.size() > 0 */ && idx < 20000) {
			vm.run();
			ArrayList<Long> out = vm.getOutputs();
			System.out.println("====================================================");
			String recv = showAscii(out);
			if (recv.indexOf("You can't go that way") >= 0 || recv.indexOf("Unrecognized command") >= 0 ) {
				moved = false;
				last = cur;
			} else if (next.x != last.x || next.y != last.y || idx == 0) {
				moved = true;
					if (doors.size() < 2) {
						image[cur.x][cur.y] = 7;
					} else {
						image[cur.x][cur.y] = 6;
					}
				image[cur.x][cur.y] = 6;
				last = cur;
				//image[last.x][last.y] = 2;
				cur = next;
			} else {
				if (next.x != cur.x || next.y != cur.y) {
					moved = true;
					image[cur.x][cur.y] = 6;
					last = cur;
					cur = next;
				} else {
				moved = false;
				cur = last;
				}
			}
			System.out.println("------------------------------------------");
			image[cur.x][cur.y] = 9;
			neighbors = cur.neighbors();
			if (moved) {
				doors = getDoors(recv);
				newItems = getItems(recv);
				doorNeighbors.clear();
				for (String s : doors) {
					Point p = Point.wheres(cur, s);
					doorNeighbors.add(p);
				}
			}
			System.out.println("------------------------------------------");
			System.out.println("X MOVED: "+(moved?"YES":"no"));
			System.out.println("X STEP : "+idx);
			System.out.println("X LAST : "+last);
			System.out.println("X CUR  : "+cur);
			System.out.print("X DOORS: ");
			for (Point pt : doorNeighbors) {
				System.out.print(pt);
			}
			System.out.println("");
			for (Point p : neighbors) {
				boolean isDoor = false;
				for (Point d : doorNeighbors) {
					if (p.x == d.x && p.y == d.y) {
						if(image[p.x][p.y] == 0) image[p.x][p.y] = 3;
						isDoor = true;
						break;
					}
				}
				if (!isDoor && image[p.x][p.y] == 0) {
					image[p.x][p.y] = 4;
				} else {
					if (moved) {
						if (!(p.x == last.x && p.y == last.y)) {
							if (image[p.x][p.y] != 7) todo.add(p);
						}
						if (doors.size() < 2) todo.add(last);
					}
				}
			}
			vm.setOutputs(new ArrayList<Long>());
			showImage(image);

			String nextCmd;

			Scanner scm = new Scanner(System.in);
			String manual = scm.nextLine();
			if (manual.length() > 0) {
				nextCmd = manual;
			//System.out.println(">"+nextCmd+"<"+nextCmd.getClass().getName()+nextCmd.startsWith("n")+(nextCmd=="n"));

				if (	nextCmd.startsWith("n") || nextCmd.startsWith("s") ||
						nextCmd.startsWith("w") || nextCmd.startsWith("e")) {
					if (nextCmd.equals("n")) nextCmd = "north";
					if (nextCmd.equals("e")) nextCmd = "east";
					if (nextCmd.equals("s")) nextCmd = "south";
					if (nextCmd.equals("w")) nextCmd = "west";

					next = Point.wheres(cur, nextCmd);
				}

				ins = fromAscii(nextCmd);
				System.out.println("X NEXT   : "+next);
				System.out.println("X CUR    : "+cur);
				System.out.println("X LAST   : "+last);
				System.out.println("X MANUAL : "+nextCmd);
				System.out.println("====================================================");
				vm.setInputs(ins);
				++idx;
				continue;
			}

			if (newItems.size() > 0) {
				String it = newItems.remove(newItems.size()-1);
				nextCmd = "take "+it;

				ins = fromAscii(nextCmd);
				System.out.println("X SENDING: "+nextCmd);
				System.out.println("====================================================");
				vm.setInputs(ins);
				++idx;
				continue;
			}

			next = todo.remove(todo.size()-1);
			nextCmd = next.cmd(cur);

			ins = fromAscii(nextCmd);
			System.out.println("X NEXT   : "+next);
			System.out.println("X CUR    : "+cur);
			System.out.println("X LAST   : "+last);
			System.out.println("X SENDING: "+nextCmd);
			System.out.println("====================================================");
			vm.setInputs(ins);
			++idx;
		}
		return "";
	}
}
