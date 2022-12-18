package _2017;

import static org.junit.Assert.*;
import org.junit.Before;
import org.junit.Test;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class day02Test {

  private day02 a;
  private List<List<Integer>> input;

  @Before
  public void setUp() throws Exception {
    a = new day02();
  }

  @Test
  public void testChecksum_one() {
    input = new ArrayList<List<Integer>>(Arrays.asList(Arrays.asList(5, 1, 9, 5),
        Arrays.asList(7, 5, 3), Arrays.asList(2, 4, 6, 8)));
    assertEquals(18, a.checksum_one(input));
  }

  @Test
  public void testChecksum_two() {
    input = new ArrayList<List<Integer>>(Arrays.asList(Arrays.asList(5, 9, 2, 8),
        Arrays.asList(9, 4, 7, 3), Arrays.asList(3, 8, 6, 5)));
    assertEquals(9, a.checksum_two(input));
  }

}
