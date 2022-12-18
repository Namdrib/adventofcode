package _2017;

import static org.junit.Assert.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.junit.Before;
import org.junit.Test;

public class day08Test {

  private day08 a;
  private List<String> input;

  @Before
  public void setUp() throws Exception {
    a = new day08();
  }

  @Test
  public void testLargestRegister() {
    input = new ArrayList<>(Arrays.asList("b inc 5 if a > 1", "a inc 1 if b < 5",
        "c dec -10 if a >= 1", "c inc -20 if c == 10"));
    int[] maxValues = a.largestRegister(input);
    assertEquals(2, maxValues.length);
    assertEquals(1, maxValues[0]);
    assertEquals(10, maxValues[1]);

  }

}
