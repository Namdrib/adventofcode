package _2017;

import static org.junit.Assert.assertEquals;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Scanner;

// http://adventofcode.com/2017/day/3

public class day03 {

  public day03() {
    ;
  }

  private <T> void print2DList(List<List<T>> input) {
    for (List<T> list : input) {
      for (T elem : list) {
        System.out.print(String.format("%7d", elem));
      }
      System.out.println();
    }
    System.out.println();
  }

  private int gridDimFor(int input) {
    int n = 1;
    while (n * n < input) {
      n += 2;
    }
    return n;
  }

  // Generate an anti-clockwise spiral grid with 1 in the centre
  // such that it includes input
  // e.g. including 9:
  // 5 4 3
  // 6 1 2
  // 7 8 9
  // Will have a complete square (e.g. must be n*n) such that it includes input
  // That means including 2, 3, ..., 9 will generate a 3*3
  // Observation: n^2 (where n is odd) is always on a bottom-right diagonal
  // So generate enough to hold the n^2 such that n^2 >= input
  public List<List<Integer>> generateGridWith(int input) {
    // Ensure n is large enough to encompass input
    int n = gridDimFor(input);

    // Initialise (kind of empty) n*n list
    List<Integer> temp = new ArrayList<>(Collections.nCopies(n, 0));
    List<List<Integer>> out = new ArrayList<>();
    for (int i = 0; i < n; i++) {
      out.add(new ArrayList<>(temp));
    }

    // Now populate with numbers
    int x = (int) Math.floor(n / 2);
    int y = (int) Math.floor(n / 2);

    // Each "layer" of the grid
    // counter is the value to insert
    for (int i = 0, counter = 1; i <= n; i++) {
      // x-axis lines
      for (int j = 0; j < i; j++) {
        out.get(y).set(x, counter);
        counter++;
        x += ((i & 1) == 0) ? -1 : 1;
      }

      if (i == n)
        break;

      // y-axis lines
      for (int j = 0; j < i; j++) {
        out.get(y).set(x, counter);
        counter++;
        y += ((i & 1) == 0) ? 1 : -1;
      }

    }

    System.err.println("Final: ");
    print2DList(out);

    return out;
  }

  // Part 1
  // On such a spiral grid, how many steps away (using manhattan distance)
  // the input number is from the centre (1)
  public int stepsFromGrid(int input) {
    List<List<Integer>> grid = generateGridWith(input);

    // Find `input` in the grid.
    int y = 0, x = 0;
    for (y = 0; y < grid.size(); y++) {
      x = grid.get(y).indexOf(input);
      if (x > -1) {
        break;
      }
    }

    int dy = Math.abs((grid.size() / 2) - y);
    int dx = Math.abs((grid.get(dy).size() / 2) - x);
    return dx + dy;
  }

  // Part 2
  // The description is decribed by https://oeis.org/A141481
  public int firstLargerThan(int input, String OEIS_A14181) {
    int n = gridDimFor(input);

    // Read file in the string
    try (BufferedReader br = new BufferedReader(new FileReader(OEIS_A14181))) {
      String s;
      while ((s = br.readLine()) != null) {
        if (!s.startsWith("#") && s.contains(" ")) {
          String[] parts = s.split(" ");
          int whichEntry = Integer.parseInt(parts[0]);

          if (whichEntry > n * n) {
            break;
          }
          int entry = Integer.parseInt(parts[1]);
          if (entry > input) {
            return entry;
          }
        }
      }
    } catch (IOException ex) {
      ex.printStackTrace();
    }

    return -1;
  }

  public static void main(String[] args) {
    day03 a = new day03();
    String pathToSeq = "2017/tests/a141481.txt";

    if (args.length > 0) {
      // Part 1
      assertEquals(0, a.stepsFromGrid(1));
      assertEquals(3, a.stepsFromGrid(12));
      assertEquals(2, a.stepsFromGrid(23));
      assertEquals(31, a.stepsFromGrid(1024));

      // Part 2
      assertEquals(4, a.firstLargerThan(2, pathToSeq));
      assertEquals(4, a.firstLargerThan(3, pathToSeq));
      assertEquals(5, a.firstLargerThan(4, pathToSeq));
      assertEquals(10, a.firstLargerThan(5, pathToSeq));
      assertEquals(10, a.firstLargerThan(6, pathToSeq));
      assertEquals(10, a.firstLargerThan(7, pathToSeq));
      assertEquals(10, a.firstLargerThan(8, pathToSeq));
      assertEquals(10, a.firstLargerThan(9, pathToSeq));
      assertEquals(11, a.firstLargerThan(10, pathToSeq));
      assertEquals(23, a.firstLargerThan(11, pathToSeq));

      System.out.println("Tests successful!");
      return;
    }

    // Take input, turn into usable form
    int input = 1;
    try (Scanner scanner = new Scanner(System.in)) {
      input = scanner.nextInt();
    }

    System.out.println("Part 1: " + a.stepsFromGrid(input));
    System.out.println("Part 2: " + a.firstLargerThan(input, pathToSeq));
  }
}
