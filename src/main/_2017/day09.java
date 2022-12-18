package _2017;

import java.util.Scanner;

// http://adventofcode.com/2017/day/9

public class day09 {

  public day09() {
    ;
  }

  // Clear the effect of '!' in input
  // Should be used as the first "filter"
  public String clearExclamation(String input) {
    String out = new String();
    for (int i = 0; i < input.length(); i++) {
      if (input.charAt(i) == '!') {
        i++;
      } else {
        out += input.charAt(i);
      }
    }
    return out;
  }

  // Loop through input until first '<'
  // ignore everything until first '>'
  // remove everything in between (inclusive)
  // repeat
  public String clearGarbage(String input) {
    String out = "";
    boolean inGarbage = false;
    for (int i = 0; i < input.length(); i++) {
      char current = input.charAt(i);
      if (inGarbage) {
        if (current == '>') {
          inGarbage = false;
        }
      } else {
        if (current == '<') {
          inGarbage = true;
        } else {
          out += current;
        }
      }
    }

    return out;
  }

  public int score(String input) {
    input = clearExclamation(input);
    input = clearGarbage(input);

    // At this point, should only be left with braces and commas
    // Loop through the string, accumulating potential "points" as a new "{" is encountered
    // When a "}" is matched, add those points to the score and reduce points by 1
    // basically each layer +1 point
    int score = 0;

    int pointsForClosing = 0;
    for (int i = 0; i < input.length(); i++) {
      char current = input.charAt(i);
      if (current == '{') {
        pointsForClosing++;
      } else if (current == '}') {
        score += pointsForClosing;
        pointsForClosing--;
      }
    }

    return score;
  }

  public int charactersInGarbage(String input) {
    input = clearExclamation(input);

    int out = 0;

    boolean counting = false;
    for (int i = 0; i < input.length(); i++) {
      char current = input.charAt(i);
      if (counting) {
        if (current == '>') {
          counting = false;
        } else {
          out++;
        }
      } else {
        if (current == '<') {
          counting = true;
        }
      }
    }

    return out;
  }

  public static void main(String[] args) {
    day09 a = new day09();

    String input = new String();
    try (Scanner scanner = new Scanner(System.in)) {
      if (scanner.hasNextLine()) {
        input = scanner.nextLine();
      }
    }

    System.out.println("Part 1: " + a.score(input));
    System.out.println("Part 2: " + a.charactersInGarbage(input));
  }
}

