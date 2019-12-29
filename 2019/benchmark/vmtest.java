import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

class VMTest {
    public static void main(String[] args) throws java.io.FileNotFoundException {
		String fname = "";
		ArrayList<Long> ops = new ArrayList<Long>();
        if (args.length > 0) {
			fname = args[0];

	        List<String> data = new ArrayList<String>();
	        Scanner sc = new Scanner(new File(fname)); 

	        while (sc.hasNextLine()) {
	            String x = sc.nextLine();
	            //System.out.println(x);
	            data.add(x);
	        }
	        System.out.println("Lines: " + data.size());

			for (String ls : data) {
				for (String lsi : ls.split(",")) {
					ops.add(Long.parseLong(lsi));
				}
			}
	        System.out.println("Ops: " + ops.size());
        }

		tests();
	}

	private static void show(List<Long> v) {
		StringBuffer s = new StringBuffer();
		for (int i=0;i<v.size()-1;++i) {
			s.append(v.get(i));
			s.append(",");
		}
		if (v.size() > 0) s.append(v.get(v.size()-1));
		System.out.println(s);
	}

	private static void tests() {
		test1();
		test2();
		test3();
		test4();
		test5();
		test6();
		day09test1();
		day09test2();
		day09test3();
		day09test4();
	}

	private static void day09test1() {
		int[] arr = {109, 19, 204, -34, 99};
		ArrayList<Long> ops = new ArrayList<Long>();
		ArrayList<Long> in  = new ArrayList<Long>();

		for (int i : arr) {
			ops.add(Long.valueOf(i));
		}

		VM vm = new VM(ops, in);
		System.out.println(vm);
		vm.setRelPos(2000L);
		vm.setCodeAt(1985L, 666L);
		vm.run();
		List<Long> rv = vm.getOutputs();
		System.out.println("==========");
		show(ops);
		show(rv);
		System.out.println(vm.getOps().get(1985));
	}

	private static void day09test2() {
		int[] arr = {109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99};
		ArrayList<Long> ops = new ArrayList<Long>();
		ArrayList<Long> in  = new ArrayList<Long>();

		for (int i : arr) {
			ops.add(Long.valueOf(i));
		}

		VM vm = new VM(ops, in);
		System.out.println(vm);
		vm.run();
		List<Long> rv = vm.getOutputs();
		System.out.println("==========");
		show(ops);
		show(rv);
		assert rv.get(0) == 109;
		assert rv.size() == ops.size();
	}

	private static void day09test3() {
		int[] arr = {1102,34915192,34915192,7,4,7,99,0};
		ArrayList<Long> ops = new ArrayList<Long>();
		ArrayList<Long> in  = new ArrayList<Long>();

		for (int i : arr) {
			ops.add(Long.valueOf(i));
		}

		VM vm = new VM(ops, in);
		System.out.println(vm);
		vm.run();
		List<Long> rv = vm.getOutputs();
		System.out.println("==========");
		show(ops);
		show(rv);
		System.out.println("    ^    ^    ^6");
		assert rv.get(0) == 1219070632396864L;
	}

	private static void day09test4() {
		long[] arr = {104L,1125899906842624L,99L};
		ArrayList<Long> ops = new ArrayList<Long>();
		ArrayList<Long> in  = new ArrayList<Long>();

		for (long i : arr) {
			ops.add(Long.valueOf(i));
		}

		VM vm = new VM(ops, in);
		System.out.println(vm);
		vm.run();
		List<Long> rv = vm.getOutputs();
		System.out.println("==========");
		show(ops);
		show(rv);
		assert rv.get(0) == arr[1];
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
		assert rv.get(0) == 2;
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
		assert rv.get(3) == 6;
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
		assert rv.get(5) == 9801;
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
		assert rv.get(1) == 30;
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
		assert rv.get(5) == 99;
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
		assert rv.get(5) == 99;
	}
}
