package _2017;

import static org.junit.Assert.*;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import util.Global;
import util.Util;

public class day19Test {

  private day19 a;
  private List<String> network;

  @Before
  public void setUp() throws Exception {
    a = new day19();
    String filename = Global.testPath + "_2017/day19_01" + Global.testExt;
    network = Util.readFileIntoListString(filename);
    a.solve(network);
  }

  @Test
  public void testPartOne() {
    assertEquals("ABCDEF", a.partOne());
  }

  @Test
  public void testPartTwo() {
    assertEquals(38, a.partTwo());
  }

}
