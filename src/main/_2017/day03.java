package _2017;

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
    String pathToSeq = "src/test/_2017/a141481.txt";

    // Take input, turn into usable form
    int input = 1;
    try (Scanner scanner = new Scanner(System.in)) {
      input = scanner.nextInt();
    }

    System.out.println("Part 1: " + a.stepsFromGrid(input));
    System.out.println("Part 2: " + a.firstLargerThan(input, pathToSeq));
  }
}
