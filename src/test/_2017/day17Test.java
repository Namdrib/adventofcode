package _2017;

import static org.junit.Assert.*;
import org.junit.Before;
import org.junit.Test;

public class day17Test {
  
  private day17 a;

  @Before
  public void setUp() throws Exception {
    a = new day17();
  }

  @Test
  public void testSolve() {
    assertEquals(638, a.solve(2017, 2017, 3, false));
  }

}
