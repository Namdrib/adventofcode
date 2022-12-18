package _2017;

import java.util.Scanner;

// https://adventofcode.com/2017/day/15

public class day15 {
  public class Generator {
    final long factor;
    final static long divisor = 2147483647;
    final long multiple;
    final boolean partTwo;
    long start;

    Generator(long factor, long multiple, long start, boolean partTwo) {
      this.factor = factor;
      this.multiple = multiple;
      this.start = start;
      this.partTwo = partTwo;
    }

    public void init(long start) {
      this.start = start;
    }

    private void updateStart() {
      start = (start * factor) % divisor;
    }

    public long getNextNumber() {
      updateStart();

      if (partTwo == true) {
        while (start % multiple != 0) {
          updateStart();
        }
      }

      return start;
    }
  }

  public day15() {
    ;
  }

  int samePairs(long startA, long startB, int count, boolean partTwo) {
    Generator a = new Generator(16807, 4, startA, partTwo);
    Generator b = new Generator(48271, 8, startB, partTwo);
    int numSamePairs = 0;

    while (count-- > 0) {
      long numA = a.getNextNumber();
      long numB = b.getNextNumber();

      long significantA = numA & 0xFFFF;
      long significantB = numB & 0xFFFF;
      if (significantA == significantB) {
        numSamePairs++;
      }
    }

    return numSamePairs;
  }

  public static void main(String[] args) {
    day15 a = new day15();

    long startA, startB;
    try (Scanner scanner = new Scanner(System.in)) {
      String lineA = scanner.nextLine();
      String[] elementsA = lineA.split(" ");
      startA = Long.parseLong(elementsA[elementsA.length - 1]);
      String lineB = scanner.nextLine();
      String[] elementsB = lineB.split(" ");
      startB = Long.parseLong(elementsB[elementsB.length - 1]);
    }

    System.out.println("Part 1: " + a.samePairs(startA, startB, 40000000, false));
    System.out.println("Part 2: " + a.samePairs(startA, startB, 5000000, true));
  }
}
