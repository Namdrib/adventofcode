package _2017;

import static org.junit.Assert.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.junit.Before;
import org.junit.Test;

public class day06Test {

  private day06 a;
  List<Integer> input;

  @Before
  public void setUp() throws Exception {
    a = new day06();
    input = Arrays.asList(0, 2, 7, 0);
  }

  @Test
  public void testNumMovesToRepeat() {
    assertEquals(5, a.numMovesToRepeat(new ArrayList<>(input), false));
    assertEquals(4, a.numMovesToRepeat(new ArrayList<>(input), true));
  }

}
