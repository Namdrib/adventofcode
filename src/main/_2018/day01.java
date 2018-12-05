package _2018;

import static org.junit.Assert.assertEquals;
import java.util.*;
import template.day;
import util.Global;
import util.Util;

// https://adventofcode.com/2018/day/1

public class day01 extends day {

  @Override
  public String partOne(List<String> input) {
    return String.valueOf(Util.listStringToInt(input).stream().reduce(0, (a, b) -> a + b));
  }

  @Override
  public String partTwo(List<String> input) {
    Set<Integer> frequencies = new HashSet<>();

    List<Integer> integers = Util.listStringToInt(input);

    int out = 0;
    frequencies.add(out);

    while (true) {
      for (int i : integers) {
        out += i;
        if (frequencies.contains(out)) {
          return String.valueOf(out);
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
      assertEquals("3", a.partOne(Arrays.asList("1", "1", "1")));
      assertEquals("0", a.partOne(Arrays.asList("1", "1", "-2")));
      assertEquals("-6", a.partOne(Arrays.asList("-1", "-2", "-3")));

      // Part "2"
      assertEquals("2", a.partTwo(Arrays.asList("1", "-2", "3", "1", "1", "-2")));
      assertEquals("0", a.partTwo(Arrays.asList("1", "-1")));
      assertEquals("10", a.partTwo(Arrays.asList("3", "3", "4", "-2", "-4")));
      assertEquals("5", a.partTwo(Arrays.asList("-6", "3", "8", "5", "-6")));
      assertEquals("14", a.partTwo(Arrays.asList("7", "7", "-2", "-7", "-4")));

      System.out.println("Tests successful!");
      return;
    }

    // Take input, turn into usable form
    String filename = Global.testPath + "_2018/day01_01" + Global.testExt;

    List<String> input = Util.readFileIntoListString(filename);

    // Do something with the input and a
    System.out.println("Part 1: " + a.partOne(input));
    System.out.println("Part 2: " + a.partTwo(input));
  }
}
