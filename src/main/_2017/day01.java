package _2017;

import java.util.Scanner;

// http://adventofcode.com/2017/day/1

public class day01 {
  public day01() {
    ;
  }

  public int solution(String input, boolean partTwo) {
    int sum = 0;

    for (int i = 0; i < input.length(); i++) {
      // Store the two digits to check
      char first = input.charAt(i);
      int nextPos = (i + ((partTwo) ? input.length() / 2 : 1)) % input.length();
      char second = input.charAt(nextPos);

      if (first == second) {
        sum += (first - '0');
      }
    }

    return sum;
  }

  public static void main(String[] args) {
    day01 a = new day01();

    String input = new String();
    try (Scanner scanner = new Scanner(System.in)) {
      System.out.print("Enter input: ");
      input = scanner.nextLine();
    }

    input = input.trim();
    System.out.println("Part 1: " + a.solution(input, false));
    System.out.println("Part 2: " + a.solution(input, true));
  }
}
