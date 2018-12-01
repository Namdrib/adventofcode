package _2018;

import static org.junit.Assert.assertEquals;
import java.util.*;
import util.Util;

// https://adventofcode.com/2018/day/1

public class day01 {

  public int partOne(List<Integer> list) {
    int out = 0;
    for (int i : list) {
      out += i;
    }
    return out;
  }

  public int partTwo(List<Integer> list) {
    Set<Integer> frequencies = new HashSet<>();

    int out = 0;
    frequencies.add(out);

    while (true) {
      for (int i : list) {
        out += i;
        if (frequencies.contains(out)) {
          return out;
        }
        frequencies.add(out);
      }
    }
  }

  public static void main(String[] args) {
    day01 a = new day01();
    if (args.length > 0) {
      // perform tests

      // Part 1
      assertEquals(3, a.partOne(Arrays.asList(1, 1, 1)));
      assertEquals(0, a.partOne(Arrays.asList(1, 1, -2)));
      assertEquals(-6, a.partOne(Arrays.asList(-1, -2, -3)));

      // Part 2
      assertEquals(2, a.partTwo(Arrays.asList(1, -2, 3, 1, 1, -2)));
      assertEquals(0, a.partTwo(Arrays.asList(1, -1)));
      assertEquals(10, a.partTwo(Arrays.asList(3, 3, 4, -2, -4)));
      assertEquals(5, a.partTwo(Arrays.asList(-6, 3, 8, 5, -6)));
      assertEquals(14, a.partTwo(Arrays.asList(7, 7, -2, -7, -4)));

      System.out.println("Tests successful!");
      return;
    }

    // Take input, turn into usable form
    String filename = "_2018/tests/day01_01.in";

    List<Integer> input = Util.readFileIntoListInteger(filename);

    // Do something with the input and a
    System.out.println("Part 1: " + a.partOne(input));
    System.out.println("Part 2: " + a.partTwo(input));
  }
}
