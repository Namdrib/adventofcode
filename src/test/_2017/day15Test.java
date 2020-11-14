package _2017;

import static org.junit.Assert.*;
import org.junit.Before;
import org.junit.Test;

public class day15Test {

  private day15 a;

  @Before
  public void setUp() throws Exception {
    a = new day15();
  }

  @Test
  public void testSamePairs() {
    assertEquals(1, a.samePairs(65, 8921, 5, false));
    assertEquals(588, a.samePairs(65, 8921, 40000000, false));

    assertEquals(0, a.samePairs(65, 8921, 5, true));
    assertEquals(0, a.samePairs(65, 8921, 1055, true));
    assertEquals(1, a.samePairs(65, 8921, 1056, true));
    assertEquals(309, a.samePairs(65, 8921, 5000000, true));
  }

}
