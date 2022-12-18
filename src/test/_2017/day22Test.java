package _2017;

import static org.junit.Assert.*;
import java.util.Map;
import org.junit.Before;
import org.junit.Test;
import _2017.day22.InfectionState;
import util.Global;
import util.IntegerPair;

public class day22Test {

  private day22 a;
  private Map<IntegerPair, InfectionState> infected;

  @Before
  public void setUp() throws Exception {
    a = new day22();
    String filename = Global.testPath + "_2017/day22_01" + Global.testExt;
    infected = a.readInfected(filename);
  }

  @Test
  public void testSolve() {
    assertEquals(5, a.solve(infected, 7, false));
    assertEquals(41, a.solve(infected, 70, false));
    assertEquals(5_587, a.solve(infected, 10_000, false));

    assertEquals(26, a.solve(infected, 100, true));

    // this one takes a long time
    // assertEquals(2_511_944, a.solve(infected, 10_000_000, true));
  }

}
