package _2018;

import static org.junit.Assert.assertEquals;
import java.util.Arrays;
import org.junit.Before;
import org.junit.Test;

public class day01Test {

  private day01 a;

  @Before
  public void setUp() throws Exception {
    a = new day01();
  }

  @Test
  public void testPartOne() {
    assertEquals("3", a.partOne(Arrays.asList("1", "1", "1")));
    assertEquals("0", a.partOne(Arrays.asList("1", "1", "-2")));
    assertEquals("-6", a.partOne(Arrays.asList("-1", "-2", "-3")));
  }

  @Test
  public void testPartTwo() {
    assertEquals("2", a.partTwo(Arrays.asList("1", "-2", "3", "1", "1", "-2")));
    assertEquals("0", a.partTwo(Arrays.asList("1", "-1")));
    assertEquals("10", a.partTwo(Arrays.asList("3", "3", "4", "-2", "-4")));
    assertEquals("5", a.partTwo(Arrays.asList("-6", "3", "8", "5", "-6")));
    assertEquals("14", a.partTwo(Arrays.asList("7", "7", "-2", "-7", "-4")));
  }

}
