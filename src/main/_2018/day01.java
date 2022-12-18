package _2018;

import java.util.HashSet;
import java.util.List;
import java.util.Set;
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

    // Take input, turn into usable form
    String filename = Global.testPath + "_2018/day01_00" + Global.testExt;

    List<String> input = Util.readFileIntoListString(filename);

    // Do something with the input and a
    System.out.println("Part 1: " + a.partOne(input));
    System.out.println("Part 2: " + a.partTwo(input));
  }
}
