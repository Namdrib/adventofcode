package _2018;

import static org.junit.Assert.assertEquals;
import java.util.*;
import util.Util;

// https://adventofcode.com/2018/day/2

public class day02 {

  /**
   * Return true if `s` contains `target` number of `c`
   * @param s the input string
   * @param c the character to search for
   * @param target the desired frequency of c in s
   * @return true iff `s` contains `target` number of `c`, false otherwise
   */
  public boolean hasN(String s, char c, int target) {
    
    int freq = 0;
    for (int i = 0; i < s.length(); i++) {
      if (s.charAt(i) == c) {
        freq++;
        
        // early exit
        if (freq > target) {
          return false;
        }
      }
    }
    return freq == target;
  }

  public int partOne(List<String> list) {
    int numTwice = 0;
    int numThrice = 0;

    for (String s : list) {
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

    return numTwice * numThrice;
  }

  int numDiffLetters(String a, String b) {
    int out = 0;

    for (int i = 0; i < Math.min(a.length(), b.length()); i++) {
      if (a.charAt(i) != b.charAt(i)) {
        out++;
      }
    }
    return out;
  }


  public String partTwo(List<String> list) {
    for (int i = 0; i < list.size(); i++) {
      for (int j = i + 1; j < list.size(); j++) {
        int numDiff = numDiffLetters(list.get(i), list.get(j));
        if (numDiff == 1) {
          String out = "";
          for (int k = 0; k < Math.min(list.get(i).length(), list.get(j).length()); k++) {
            if (list.get(i).charAt(k) == list.get(j).charAt(k)) {
              out += list.get(i).charAt(k);
            }
          }
          return out;
        }
      }
    }

    return "";
  }

  public static void main(String[] args) {
    day02 a = new day02();
    if (args.length > 0) {
      // perform tests

      // Part 1
      assertEquals(12, a.partOne(
          Arrays.asList("abcdef", "bababc", "abbcde", "abcccd", "aabcdd", "abcdee", "ababab")));

      // Part 2
      assertEquals("fgij",
          a.partTwo(Arrays.asList("abcde", "fghij", "klmno", "pqrst", "fguij", "axcye", "wvxyz")));

      System.out.println("Tests successful!");
      return;
    }

    // Take input, turn into usable form
    String filename = "_2018/tests/day02_01.in";
    List<String> input = Util.readFileIntoListString(filename);

    // Do something with the input and a
    System.out.println("Part 1: " + a.partOne(input));
    System.out.println("Part 2: " + a.partTwo(input));
  }
}
