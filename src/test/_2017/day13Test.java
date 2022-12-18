package _2017;

import static org.junit.Assert.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.junit.Before;
import org.junit.Test;

public class day13Test {
  
  private day13 a;
  List<String> input;

  @Before
  public void setUp() throws Exception {
    a = new day13();
    input = new ArrayList<>(Arrays.asList("0: 3", "1: 2", "4: 4", "6: 4"));
  }

  @Test
  public void testMakeTrip() {
    assertEquals(24, a.makeTrip(input));
  }

  @Test
  public void testLowestDelay() {
    assertEquals(10, a.lowestDelay(input));
  }

}
