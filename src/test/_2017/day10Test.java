package _2017;

import static org.junit.Assert.*;
import java.util.Arrays;
import org.junit.Before;
import org.junit.Test;

public class day10Test {

  private day10 a;

  @Before
  public void setUp() throws Exception {
    a = new day10();
    a.init(4);
  }

  @Test
  public void testKnotRotate() {
    // fail("Not yet implemented");
  }

  @Test
  public void testInit() {
    a.init(-1);
    assertEquals(Arrays.asList(), a.list);
    
    a.init(0);
    assertEquals(Arrays.asList(0), a.list);
    
    a.init(1);
    assertEquals(Arrays.asList(0, 1), a.list);
    
    a.init(5);
    assertEquals(Arrays.asList(0, 1, 2, 3, 4, 5), a.list);
  }

  @Test
  public void testPartOne() {
    assertEquals(Arrays.asList(3, 4, 2, 1, 0), a.partOne(Arrays.asList(3, 4, 1, 5)));
  }

  @Test
  public void testPartTwo() {
    assertEquals("a2582a3a0e66e6e86e3812dcb672a272", a.partTwo(""));
    assertEquals("33efeb34ea91902bb2f59c9920caa6cd", a.partTwo("AoC 2017"));
    assertEquals("3efbe78a8d82f29979031a4aa0b16a9d", a.partTwo("1,2,3"));
    assertEquals("63960835bcdc130f0b66d7ff4f6a5a8e", a.partTwo("1,2,4"));
  }

  @Test
  public void testDenseHash() {
    assertEquals(Arrays.asList(64),
        a.denseHash(Arrays.asList(65, 27, 9, 1, 4, 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22)));
  }

  @Test
  public void testToHexadecimal() {
    assertEquals("4007ff", a.toHexadecimal(Arrays.asList(64, 7, 255)));
  }

}
