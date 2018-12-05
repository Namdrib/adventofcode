package _2017;

import static org.junit.Assert.assertEquals;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Scanner;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

// http://adventofcode.com/2017/day/10

public class day10 {
  // both parts
  List<Integer> list;
  int current; // the current starting position
  int skipSize; // how much to increment current

  // gets added to part 2 after reading
  final static List<Integer> end = Arrays.asList(17, 31, 73, 47, 23);

  public day10() {
    ;
  }

  // Rotate `list` starting from current to current + length (wrap around if necessary)
  // After rotating, move current forward by (length + skipSize), then increment skipSize
  public void knotRotate(int length) {
    if (length > list.size()) {
      return;
    }

    int currentPlusLength = current + length;
    boolean overflow = (currentPlusLength > list.size());
    int overflowAmount = length - (list.size() - current);
    int boundary = overflow ? list.size() : currentPlusLength;

    // System.out.println("[P1] rotating from " + current + " by " + length + " overflow? " +
    // overflow);
    // System.out.println("[P1] Boundary: " + boundary);

    // Find the area of interest to be reverse - reverse it
    List<Integer> selection = new ArrayList<>(list.subList(current, boundary));
    if (overflow) {
      List<Integer> beginning = new ArrayList<>(list.subList(0, overflowAmount));
      selection.addAll(beginning);
    }
    // System.out.println("[P1] \tSelection: " + selection);
    Collections.reverse(selection);

    // Apply the reversed selection to the appropriate parts
    int i;
    for (i = current; i < boundary; i++) {
      list.set(i, selection.get(i - current));
    }
    i -= current;

    // Do overflowed part if necessary
    if (overflow) {
      // System.out.println("[P1] Overflow part 2");
      for (int j = 0; j < overflowAmount; j++) {
        list.set(j, selection.get(j + i));
      }
    }

    // Admin stuff
    current += (length + skipSize);
    current %= list.size();
    skipSize++;

    // System.out.println("[P1] New stuff:");
    // System.out.println("[P1] \tList: " + list);
    // System.out.println("[P1] \tItems: (c, s) " + current + " " + skipSize);
  }

  // Create the list of numbers from 0..maxValue.
  public void init(int maxValue) {
    // Make the list
    list = new ArrayList<>(IntStream.rangeClosed(0, maxValue).boxed().collect(Collectors.toList()));

    // Set vars
    current = 0;
    skipSize = 0;
  }

  // Perform each of the rotations
  public List<Integer> partOne(List<Integer> lengths) {
    for (int i : lengths) {
      knotRotate(i);
    }

    return list;
  }

  public String partTwo(String input) {
    init(255);
    // Read the input as int reps of each char (0-255)
    List<Integer> lengthSeq = new ArrayList<>();
    for (int i = 0; i < input.length(); i++) {
      lengthSeq.add((int) input.charAt(i));
    }
    lengthSeq.addAll(end);


    List<Integer> sparseHash = null;
    for (int i = 0; i < 64; i++) {
      sparseHash = partOne(lengthSeq);
    }

    List<Integer> denseHash = denseHash(sparseHash);
    return toHexadecimal(denseHash);
  }

  // Return the dense hash where:
  // Perform bitwise XOR (^) to combine each consecutive block of 16 numbers
  // since the input should have 256 numbers, the result should have 16 numbers
  // first element of dense hash
  public List<Integer> denseHash(List<Integer> sparseHash) {
    List<Integer> out = new ArrayList<>();

    for (int i = 0; i < sparseHash.size();) {
      int element = 0;
      for (int j = 0; j < 16; j++) {
        element ^= sparseHash.get(i);
        i++;
      }
      out.add(element);
    }

    return out;
  }

  // Given a denseHash as from denseHash(), represent it as a hexadec string
  // e.g. {67, 7, 255} => "4007ff"
  public String toHexadecimal(List<Integer> denseHash) {
    String out = new String();
    for (int i : denseHash) {
      String hexPair = Integer.toHexString(i);
      while (hexPair.length() < 2) {
        hexPair = "0" + hexPair;
      }
      out += hexPair;
    }
    return out;
  }

  public static void main(String[] args) {
    day10 a = new day10();
    if (args.length > 0) {
      a.init(4);
      assertEquals(Arrays.asList(3, 4, 2, 1, 0), a.partOne(Arrays.asList(3, 4, 1, 5)));

      // Intermediate functions
      assertEquals(Arrays.asList(64),
          a.denseHash(Arrays.asList(65, 27, 9, 1, 4, 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22)));

      assertEquals("4007ff", a.toHexadecimal(Arrays.asList(64, 7, 255)));

      // Part two
      assertEquals("a2582a3a0e66e6e86e3812dcb672a272", a.partTwo(""));
      assertEquals("33efeb34ea91902bb2f59c9920caa6cd", a.partTwo("AoC 2017"));
      assertEquals("3efbe78a8d82f29979031a4aa0b16a9d", a.partTwo("1,2,3"));
      assertEquals("63960835bcdc130f0b66d7ff4f6a5a8e", a.partTwo("1,2,4"));

      System.out.println("Tests successful!");
      return;
    }

    // Take input, turn into usable form
    String input = null;
    try (Scanner scanner = new Scanner(System.in)) {
      if (scanner.hasNextLine()) {
        input = scanner.nextLine();
      }
    }

    // Turn input into a list for partOne
    List<Integer> inputList = new ArrayList<>();
    String[] elements = input.split(",");
    for (String element : elements) {
      inputList.add(Integer.parseInt(element.trim()));
    }

    a.init(255);
    List<Integer> afterRotations = a.partOne(inputList);
    System.out.println("Part 1: " + afterRotations.get(0) * afterRotations.get(1));
    System.out.println("Part 2: " + a.partTwo(input));
  }
}
