package _2017;

import static org.junit.Assert.*;
import org.junit.Before;
import org.junit.Test;
import util.Global;

public class day03Test {

  private day03 a;
  private String pathToSeq = Global.testPath + "_2017/a141481.txt";

  @Before
  public void setUp() throws Exception {
    a = new day03();
  }

  @Test
  public void testStepsFromGrid() {
    assertEquals(0, a.stepsFromGrid(1));
    assertEquals(3, a.stepsFromGrid(12));
    assertEquals(2, a.stepsFromGrid(23));
    assertEquals(31, a.stepsFromGrid(1024));
  }

  @Test
  public void testFirstLargerThan() {
    assertEquals(4, a.firstLargerThan(2, pathToSeq));
    assertEquals(4, a.firstLargerThan(3, pathToSeq));
    assertEquals(5, a.firstLargerThan(4, pathToSeq));
    assertEquals(10, a.firstLargerThan(5, pathToSeq));
    assertEquals(10, a.firstLargerThan(6, pathToSeq));
    assertEquals(10, a.firstLargerThan(7, pathToSeq));
    assertEquals(10, a.firstLargerThan(8, pathToSeq));
    assertEquals(10, a.firstLargerThan(9, pathToSeq));
    assertEquals(11, a.firstLargerThan(10, pathToSeq));
    assertEquals(23, a.firstLargerThan(11, pathToSeq));
  }

}
