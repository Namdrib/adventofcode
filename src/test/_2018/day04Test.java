package _2018;

import static org.junit.Assert.assertEquals;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import util.Global;
import util.Util;

public class day04Test {

  private day04 a;
  String filename = Global.testPath + "_2018/day04_00" + Global.testExt;
  List<String> input;

  @Before
  public void setUp() throws Exception {
    a = new day04();
    List<String> input = Util.readFileIntoListString(filename);
    a.presolve(input);
  }

  @Test
  public void testPartOne() {
    assertEquals("240", a.partOne(input));
  }

  @Test
  public void testPartTwo() {
    assertEquals("4455", a.partTwo(input));
  }

}
