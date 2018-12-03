package _2018;

import static org.junit.Assert.assertEquals;
import java.util.*;
import java.util.Map.Entry;
import util.IntegerPair;
import util.Util;

// https://adventofcode.com/2018/day/3

public class day03 {

  public class Claim {
    public int id, x, y, w, h;

    public Claim() {
      ;
    }

    public Claim(int id, int x, int y, int w, int h) {
      this.id = id;
      this.x = x;
      this.y = y;
      this.w = w;
      this.h = h;
    }

    public boolean intersects(Claim rhs) {
      return !(x + w < rhs.x || rhs.x + rhs.w < x || y + h < rhs.y || rhs.y + rhs.h < y);
    }

    @Override
    public String toString() {
      StringBuilder sb = new StringBuilder();
      sb.append("ID: " + id + ", pos: " + x + "," + y + ", size: " + w + "," + h);
      return sb.toString() + "\n";
    }
  }

  public int solve(List<String> input, boolean partTwo) {
    int out = 0;

    return out;
  }

  public int partOne(List<Claim> input) {
    int out = 0;

    Map<IntegerPair, Integer> numOverlaps = new HashMap<>();
    for (Claim claim1 : input) {
      for (int i = claim1.y; i < claim1.y + claim1.h; i++) {
        for (int j = claim1.x; j < claim1.x + claim1.w; j++) {
          // this fails. maybe something about comparing equality? not sure...
          // switched to c++ at this point to deal with map<pair<int, int>> more easily
          IntegerPair ip = new IntegerPair(j, i);
          numOverlaps.put(ip, numOverlaps.getOrDefault(ip, 0) + 1);
        }
      }
    }

    for (Entry<IntegerPair, Integer> entry : numOverlaps.entrySet()) {
      if (entry.getValue() >= 2) {
        out++;
      }
    }

    return out;
  }

  public int partTwo(List<Claim> input) {
    int out = 0;

    return out;
  }

  public static void main(String[] args) {
    day03 a = new day03();
    if (args.length > 0) {
      // perform tests

      assertEquals(0, a.partOne(Arrays.asList()));



      assertEquals(0, a.partTwo(Arrays.asList()));

      System.out.println("Tests successful!");
      return;
    }

    // Take input, turn into usable form
    String filename = "_2018/tests/day03_01.in";
    List<String> input = Util.readFileIntoListString(filename);

    List<Claim> claims = new ArrayList<>();
    for (String item : input) {
      String[] elems = item.split(" ");

      int claimID = Integer.parseInt(elems[0].substring(1));

      String[] pos = elems[2].split(",");
      pos[1] = pos[1].substring(0, pos[1].length() - 1);
      int xPos = Integer.parseInt(pos[0]);
      int yPos = Integer.parseInt(pos[1]);

      String[] size = elems[3].split("x");
      int xSize = Integer.parseInt(size[0]);
      int ySize = Integer.parseInt(size[1]);

      claims.add(a.new Claim(claimID, xPos, yPos, xSize, ySize));
    }

    System.out.println(claims);

    System.out.println("Part 1: " + a.partOne(claims));
    System.out.println("Part 2: " + a.partTwo(claims));
  }
}
