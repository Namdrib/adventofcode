package util;

import java.io.*;
import java.util.*;

/**
 * Collection of public helper functions for Java solutions
 * 
 * @author Namdrib
 *
 */
public class Util {
  // read a file's contents line-by-line into a List<String>
  public static List<String> readFileIntoListString(String filename) {
    List<String> out = new ArrayList<>();
    try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
      for (String line; (line = br.readLine()) != null;) {
        out.add(line);
      }
    } catch (FileNotFoundException e) {
      e.printStackTrace();
    } catch (IOException e) {
      e.printStackTrace();
    }
    return out;
  }

  // read a file's contents line-by-line into a List<Integer>
  public static List<Integer> readFileIntoListInteger(String filename) {
    List<Integer> out = new ArrayList<>();
    try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
      for (String line; (line = br.readLine()) != null;) {
        out.add(Integer.parseInt(line));
      }
    } catch (FileNotFoundException e) {
      e.printStackTrace();
    } catch (IOException e) {
      e.printStackTrace();
    }
    return out;
  }

  public static List<List<Integer>> readInputInto2DListInteger() {
    List<List<Integer>> out = new ArrayList<List<Integer>>();
    try (Scanner scanner = new Scanner(System.in)) {
      for (String line; (line = scanner.nextLine()) != null;) {
        String[] elements = line.split("\\s+");

        ArrayList<Integer> temp = new ArrayList<Integer>();
        for (String s : elements) {
          temp.add(Integer.parseInt(s));
        }
        out.add(temp);
      }
    }
    return out;
  }
}
