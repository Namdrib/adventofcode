package _2016;

import static org.junit.Assert.*;
import org.junit.Before;
import org.junit.Test;

public class day05Test {
  
  private day05 a;

  @Before
  public void setUp() throws Exception {
    a = new day05();
  }

  @Test
  public void testSolve() {
    assertEquals("18f47a30", a.solve("abc", 8, false));
    assertEquals("05ace8e3", a.solve("abc", 8, true));
  }

}
