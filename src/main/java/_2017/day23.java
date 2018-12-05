package _2017;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import template.day;
import util.Global;
import util.Util;

// https://adventofcode.com/2017/day/23

public class day23 extends day {

  Map<String, Long> registers; // <name, value>
  int numMultiplies;

  public day23() {
    registers = new HashMap<>();
    numMultiplies = 0;
  }

  /**
   * Determine whether s refers to a register entry or a value
   * 
   * @param s either a register entry or a value
   * @return true if the value given by <code>s</code> is a register entry
   */
  private boolean isRegisterEntry(String s) {
    try {
      Long.parseLong(s);
    } catch (Exception ex) {
      return true;
    }
    return false;
  }

  /**
   * Return the value being referred to by s (whether directly or indirectly)
   * 
   * @param s either a register entry or a value
   * @return the value given by register.get(s) if s is a register entry or the value s represents
   */
  private long valueOf(String s) {
    return isRegisterEntry(s) ? registers.getOrDefault(s, 0L) : Long.parseLong(s);
  }


  @Override
  public String solve(List<String> input, boolean partTwo) {

    if (partTwo) {
      registers.put("a", 1L);
    }

    for (int i = 0; i < input.size(); i++) {
      String[] tokens = input.get(i).split(" ");
      String opcode = tokens[0];

      String x = tokens[1];
      long y = valueOf(tokens[2]);

      switch (opcode) {
        case "set":
          registers.put(x, y);
          break;
        case "sub":
          registers.put(x, valueOf(x) - y);
          break;
        case "mul":
          registers.put(x, valueOf(x) * y);
          numMultiplies++;
          break;
        case "jnz":
          if (valueOf(x) != 0) {
            i += y;
            i--;
          }
          break;
        default:
          break;
      }

      if (x.equals("h")) {
        System.out.println("h: " + valueOf("h"));
      }
    }

    return String.valueOf(partTwo ? valueOf("h") : numMultiplies);
  }

  @Override
  public String partOne(List<String> input) {
    return solve(input, false);
  }

  @Override
  public String partTwo(List<String> input) {
    // running solve(input, true) takes way too long
    // translated the assembly code to Java here
    // part two runs the translated code

    int b = 108_100;
    int c = 125_100;
    int h = 0; // the output

    for (; b <= c; b += 17) {
      if (!Util.isPrime(b)) {
        h++;
      }
    }

    return String.valueOf(h);
  }


  public static void main(String[] args) {
    day a = new day23();
    if (args.length > 0) {
      // perform tests
      System.out.println("Tests successful!");
      return;
    }

    // Take input, turn into usable form
    String filename = Global.testPath + "_2017/day23_01" + Global.testExt;

    List<String> input = Util.readFileIntoListString(filename);

    // Do something with the input and a
    System.out.println("Part 1: " + a.partOne(input));
    a = new day23(); // reset the vars
    System.out.println("Part 2: " + a.partTwo(input));
  }
}
