package _2016;

import static org.junit.Assert.assertEquals;
import java.util.Scanner;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

// https://adventofcode.com/2016/day/05

public class day05 {
  public day05() {
    ;
  }

  /**
   * Return the password obtained from various hashes of input
   * 
   * The hashes are given by <code>input + n</code> where n is a number signifying which has is
   * being tried. n starts from 0 and goes up. It is not padded. e.g. hashing "test8", "test9",
   * "test10"
   * 
   * <b>Part One</b>
   * 
   * Until the password is filled up, the hash indicates the next character in the password if the
   * hex of the hash starts with 5 0s. The 6th character gives the next character in the password
   * 
   * <b>Part Two</b>
   * 
   * Now, the 6th character gives the <i>index</i> of the password, and the seventh character gives
   * the character to put at the index
   * 
   * @param input the string to be hashed
   * @param passwordLength length of password to solve
   * @param partTwo whether we are solving for part two
   * @return
   */
  public String solve(String input, int passwordLength, boolean partTwo) {
    String out = partTwo ? new String(new char[passwordLength]).replace('\0', '_') : "";

    MessageDigest md = null;
    try {
      md = MessageDigest.getInstance("MD5");
    } catch (NoSuchAlgorithmException e) {
      e.printStackTrace();
    }

    for (int i = 0; partTwo ? out.contains("_") : out.length() < passwordLength; i++) {
      String strToHash = input + String.valueOf(i);
      byte[] digestBytes = md.digest(strToHash.getBytes());

      // bytes[0] and bytes[1] check the first four characters
      // bytes[2] & 0xF0 and bytes[2] & 0x0F checks the fifth and sixth, respectively
      // bytes[3] & 0xF0 checks the seventh character
      if (digestBytes[0] == 0 && digestBytes[1] == 0 && (digestBytes[2] & 0xF0) == 0) {
        int a = Byte.toUnsignedInt((byte) (digestBytes[2] & 0x0F));
        if (partTwo) {
          // a points to a bad position
          if (a >= passwordLength || out.charAt(a) != '_') {
            continue;
          }
          int b = Byte.toUnsignedInt((byte) ((digestBytes[3] & 0xF0) >> 4));

          // Replace out[a] with b
          StringBuilder sb = new StringBuilder(out);
          sb.setCharAt(a, Character.forDigit(b, 16));
          out = sb.toString();
        } else {
          out += Character.forDigit(a, 16);
        }
        // Makes it look like it is populating the string
        System.out.print(out + "\r");
      }
    }
    System.out.println();

    return out;
  }

  public static void main(String[] args) {
    day05 a = new day05();
    if (args.length > 0) {
      // perform tests
      assertEquals("18f47a30", a.solve("abc", 8, false));
      assertEquals("05ace8e3", a.solve("abc", 8, true));

      System.out.println("Tests successful!");
      return;
    }

    // Take input, turn into usable form
    String input = null;
    try (Scanner scanner = new Scanner(System.in)) {
      if (scanner.hasNextLine()) {
        input = scanner.next();
      }
    }

    // Do something with the input and a
    System.out.println("Part 1: " + a.solve(input, 8, false));
    System.out.println("Part 2: " + a.solve(input, 8, true));
  }
}
