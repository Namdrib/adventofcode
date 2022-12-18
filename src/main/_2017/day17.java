package _2017;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

// https://adventofcode.com/2017/day/17

public class day17 {

  public day17() {
    ;
  }

  /**
   * Return the value after `target` after `numInsertions` insertions at `spinsPerInsert` spins per
   * insertion
   * 
   * <b>Part One</b>
   * 
   * Create a simulation, populate a buffer with the insertions and spins. This is required because
   * something might be inserted <i>behind</i> <code>target</code>
   * 
   * <b>Part Two</b>
   * 
   * Simulating the buffer takes way too long, so need to work it out w/o the buffer. Only keep
   * track of the number at position <code>target+1</code>. Therefore also need to track the index
   * at which <code>target</code> was inserted
   * 
   * @param target some number in the buffer
   * @param numInsertions number of times to perform an insertion into the buffer
   * @param spinsPerInsert how many times the buffer advances before an insertion is made
   * @param partTwo whether we are solving for part two
   * @return the value after `target` after `numInsertions` insertions
   */
  public int solve(int target, int numInsertions, int spinsPerInsert, boolean partTwo) {
    List<Integer> buffer = new ArrayList<>();
    buffer.add(0);
    int currentIndex = 0;
    int numToInsert = 1;
    int bufferSize = 1; // (starts with zero in the buffer)

    int targetIndex = 0; // index where target is inserted
    int valueAfterTarget = 0; // return value

    // spin the buffer
    // perform numInsertions on buffer, spinning spinsPerInsert on each insert
    for (int i = 0; i < numInsertions; i++) {
      // perform spins
      currentIndex += spinsPerInsert;
      currentIndex %= bufferSize;

      // insert the number
      currentIndex++;
      if (partTwo) {
        if (currentIndex == (targetIndex + 1) % bufferSize) {
          valueAfterTarget = numToInsert;
        }
      } else {
        buffer.add(currentIndex, numToInsert);
      }
      bufferSize++;
      numToInsert++;
    }

    // return the value after `target`
    if (partTwo) {
      return valueAfterTarget;
    } else {
      targetIndex = buffer.indexOf(target);
      int indexAfter = (targetIndex + 1) % bufferSize;
      return buffer.get(indexAfter);
    }
  }

  public static void main(String[] args) {
    day17 a = new day17();

    int spinsPerInsert;
    try (Scanner scanner = new Scanner(System.in)) {
      spinsPerInsert = scanner.nextInt();
    }

    System.out.println("Part 1: " + a.solve(2017, 2017, spinsPerInsert, false));
    System.out.println("Part 2: " + a.solve(0, 50_000_000, spinsPerInsert, true));
  }
}
