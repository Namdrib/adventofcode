package aoc._2018;

import static org.junit.Assert.assertEquals;
import java.util.*;
import aoc.template.day;
import aoc.util.*;

// https://adventofcode.com/2018/day/2

public class day02 extends day {

  /**
   * Return true if `s` contains `c` exactly `n` times
   * 
   * @param s the input string
   * @param c the character to search for
   * @param n the desired frequency of c in s
   * @return true iff `s` contains `c` exactly `n` times, false otherwise
   */
  public boolean hasN(String s, char c, int n) {
    int freq = 0;
    for (int i = 0; i < s.length(); i++) {
      if (s.charAt(i) == c) {
        freq++;

        // early exit
        if (freq > n) {
          return false;
        }
      }
    }
    return freq == n;
  }

  @Override
  public String partOne(List<String> input) {
    int numTwice = 0, numThrice = 0;

    for (String s : input) {
      boolean gotTwo = false;
      boolean gotThree = false;
      for (char c = 'a'; c <= 'z'; c++) {
        if (!gotTwo && hasN(s, c, 2)) {
          numTwice++;
          gotTwo = true;
        }
        if (!gotThree && hasN(s, c, 3)) {
          numThrice++;
          gotThree = true;
        }
      }
    }

    return String.valueOf(numTwice * numThrice);
  }

  /**
   * 
   * @param a first query string
   * @param b second query string
   * @return the number of indices at which a and b have differing letters
   */
  int numDiffLetters(String a, String b) {
    int out = 0;

    for (int i = 0; i < Math.min(a.length(), b.length()); i++) {
      if (a.charAt(i) != b.charAt(i)) {
        out++;
      }
    }
    return out;
  }

  @Override
  public String partTwo(List<String> input) {
    for (String a : input) {
      for (String b : input) {
        if (a == b) {
          continue;
        }

        if (numDiffLetters(a, b) == 1) {
          String out = "";
          for (int i = 0; i < Math.min(a.length(), b.length()); i++) {
            if (a.charAt(i) == b.charAt(i)) {
              out += a.charAt(i);
            }
          }
          return out;
        }
      }
    }

    return "";
  }

  public static void main(String[] args) {
    day a = new day02();
    if (args.length > 0) {
      // perform tests

      // Part 1
      assertEquals("12", a.partOne(
          Arrays.asList("abcdef", "bababc", "abbcde", "abcccd", "aabcdd", "abcdee", "ababab")));

      // Part 2
      assertEquals("fgij",
          a.partTwo(Arrays.asList("abcde", "fghij", "klmno", "pqrst", "fguij", "axcye", "wvxyz")));

      System.out.println("Tests successful!");
      return;
    }

    // Take input, turn into usable form
    String filename = Global.testPath + "_2018/day02_01" + Global.testExt;
    List<String> input = Util.readFileIntoListString(filename);

    // Do something with the input and a
    System.out.println("Part 1: " + a.partOne(input));
    System.out.println("Part 2: " + a.partTwo(input));
  }
}
