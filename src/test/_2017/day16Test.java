package _2017;

import static org.junit.Assert.*;
import java.util.Arrays;
import org.junit.Before;
import org.junit.Test;

public class day16Test {

  private day16 a;

  @Before
  public void setUp() throws Exception {
    a = new day16();
  }

  @Test
  public void testDance() {
    assertEquals("baedc", a.dance(5, Arrays.asList("s1", "x3/4", "pe/b"), 1));
    assertEquals("ceadb", a.dance(5, Arrays.asList("s1", "x3/4", "pe/b"), 2));
  }
}
