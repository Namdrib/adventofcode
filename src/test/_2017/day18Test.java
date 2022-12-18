package _2017;

import static org.junit.Assert.*;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import util.Global;
import util.Util;

public class day18Test {

  private day18 a;
  List<String> instructions;

  @Before
  public void setUp() throws Exception {
    a = new day18();
    String filename = Global.testPath + "_2017/day18_01" + Global.testExt;
    instructions = Util.readFileIntoListString(filename);
  }

  @Test
  public void testPartOne() {
    assertEquals(4, a.partOne(instructions));
  }

  @Test
  public void testPartTwo() {
    assertEquals(0, a.partTwo());
  }

}
