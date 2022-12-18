package _2017;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Scanner;

// https://adventofcode.com/2017/day/14

public class day14 {
  public day14() {
    ;
  }

  public List<String> generateHashes(String input) {
    List<String> out = new ArrayList<>();
    day10 d10 = new day10();
    for (int i = 0; i < 128; i++) {
      String row = input + "-" + String.valueOf(i);
      out.add(d10.partTwo(row));
    }
    return out;
  }

  // For part two, a -1 is an un-assigned grid
  // 0 means it is off
  // n > 0 means it is in category n
  public List<List<Integer>> generateGrid(List<String> hashes) {
    List<List<Integer>> out = new ArrayList<List<Integer>>();
    for (String s : hashes) {
      List<Integer> temp = new ArrayList<>();
      for (int i = 0; i < s.length(); i++) {
        // Convert hex digit into binary string
        int hexDigit = Character.digit(s.charAt(i), 16);
        for (int mask = 8; mask > 0; mask >>= 1) {
          int value = hexDigit & mask;
          temp.add(value > 0 ? -1 : 0);
          if (mask == 0)
            break;
        }
      }
      out.add(temp);
    }
    return out;
  }

  // Recursively label all the -1s connected to grid[y][x] as groupNumber
  // Only operate with 4-connectedness
  public void dfsFill(List<List<Integer>> grid, int x, int y, int groupNumber) {
    if (grid.get(y).get(x) >= 0) {
      return;
    }
    grid.get(y).set(x, groupNumber); // set the label

    final int[] deltaX = {0, 0, -1, 1};
    final int[] deltaY = {-1, 1, 0, 0};

    // each neighbouring tile
    for (int i = 0; i < deltaX.length; i++) {
      int tempX = x + deltaX[i];
      int tempY = y + deltaY[i];
      // stop if new x,y is out of bounds
      if (tempY < 0 || tempY >= grid.size() || tempX < 0 || tempX >= grid.get(y).size()) {
        continue;
      }

      // Skips those not in an island or already in a group
      int current = grid.get(tempY).get(tempX);
      if (current != -1) {
        continue;
      }

      // Recurse
      dfsFill(grid, tempX, tempY, groupNumber);
    }
  }

  // Count how many bits in input are on (not zero)
  public int partOne(List<List<Integer>> grid) {
    return (int) grid.stream().flatMap(Collection::stream).filter(x -> x != 0).count();
  }

  // Count how many distinct groups there are
  // modifies the grid by assigning each cell its own label
  public int partTwo(List<List<Integer>> grid) {
    int groupNumber = 0;
    for (int i = 0; i < grid.size(); i++) {
      for (int j = 0; j < grid.get(0).size(); j++) {
        if (grid.get(i).get(j).equals(-1)) {
          groupNumber++;
          dfsFill(grid, j, i, groupNumber);
        }
      }
    }
    return groupNumber;
  }

  public static void main(String[] args) {
    day14 a = new day14();

    // Take input, turn into usable form
    String input = null;
    try (Scanner scanner = new Scanner(System.in)) {
      if (scanner.hasNextLine()) {
        input = scanner.next();
      }
    }

    List<String> hashes = a.generateHashes(input);
    List<List<Integer>> grid = a.generateGrid(hashes);
    System.out.println("Part 1: " + a.partOne(grid));
    System.out.println("Part 2: " + a.partTwo(grid));
  }
}
