import java.util.ArrayList;

class Point {
	public int x;
	public int y;

	public Point(int x, int y) {
		this.x = x;
		this.y = y;
	}

	public String toString() {
		return "(" + x + "/" + y +")";
	}

	public static Point where(Point p, int direc) {
		Point rv = new Point(p.x, p.y);
		if (direc == 1) {
			rv.y -= 1;
		} else if (direc == 2) {
			rv.y += 1;
		} else if (direc == 3) {
			rv.x -= 1;
		} else if (direc == 4) {
			rv.x += 1;
		} else {
			System.out.println("ERROR WHERE : "+direc+" "+p+" -> "+rv);
		}
		return rv;
	}

	public static Point wheres(Point p, String direc) {
		Point rv = new Point(p.x, p.y);
		char c = direc.charAt(0);
		if (c == 'n') {
			rv.y = rv.y - 1;
		} else if (c == 's') {
			rv.y = rv.y + 1;
		} else if (c == 'w') {
			rv.x = rv.x - 1;
		} else if (c == 'e') {
			rv.x = rv.x + 1;
		} else {
			System.out.println("ERROR WHERES: "+direc+" "+p+" -> "+rv);
		}
		return rv;
	}

	public ArrayList<Point> neighbors() {
		ArrayList<Point> rv = new ArrayList<Point>();
		Point w1 = where(this, 1);
		Point w2 = where(this, 2);
		Point w3 = where(this, 3);
		Point w4 = where(this, 4);
		rv.add(w1);
		rv.add(w2);
		rv.add(w3);
		rv.add(w4);

		return rv;
	}

	public String cmd(Point cur) {
		if (x == cur.x + 1) return "east";
		if (x == cur.x - 1) return "west";
		if (y == cur.y + 1) return "south";
		if (y == cur.y - 1) return "north";
		return "";
	}
}
