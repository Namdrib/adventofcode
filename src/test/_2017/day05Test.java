package _2017;

import static org.junit.Assert.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.junit.Before;
import org.junit.Test;

public class day05Test {

  private day05 a;
  private List<Integer> input;

  @Before
  public void setUp() throws Exception {
    a = new day05();
    input = Arrays.asList(0, 3, 0, 1, -3);
  }

  @Test
  public void testNumMovesToEscape() {
    assertEquals(5, a.numMovesToEscape(new ArrayList<>(input), false));
    assertEquals(10, a.numMovesToEscape(new ArrayList<>(input), true));
  }

}
