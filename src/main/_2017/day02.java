package _2017;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

// http://adventofcode.com/2017/day/2

public class day02 {

  public day02() {
    ;
  }

  public int checksum_one(List<List<Integer>> spreadsheet) {
    int sum = 0;

    for (List<Integer> row : spreadsheet) {
      int largest = Integer.MIN_VALUE;
      int smallest = Integer.MAX_VALUE;
      for (int element : row) {
        smallest = Math.min(smallest, element);
        largest = Math.max(largest, element);
      }
      sum += largest - smallest;
    }

    return sum;
  }

  public int checksum_two(List<List<Integer>> spreadsheet) {
    int sum = 0;

    for (List<Integer> row : spreadsheet) {
      int a = 0, b = 0;

      // each value in row
      for (int i = 0; i < row.size(); i++) {
        a = row.get(i);

        // each value in front of a
        for (int j = i + 1; j < row.size(); j++) {
          b = row.get(j);
          int top = Math.max(a, b);
          int bottom = Math.min(a, b);
          sum += (top % bottom == 0) ? top / bottom : 0; // add if multiples
        }
      }
    }

    return sum;
  }

  public static void main(String[] args) {
    day02 a = new day02();

    List<List<Integer>> input = new ArrayList<List<Integer>>();

    // Take input, turn into usable form
    try (Scanner scanner = new Scanner(System.in)) {
      while (scanner.hasNextLine()) {
        String line = scanner.nextLine();
        String[] elements = line.split("\\s+");

        ArrayList<Integer> temp = new ArrayList<Integer>();
        for (String s : elements) {
          temp.add(Integer.parseInt(s));
        }
        input.add(temp);
      }
    }

    System.out.println("Part 1: " + a.checksum_one(input));
    System.out.println("Part 2: " + a.checksum_two(input));
  }
}
