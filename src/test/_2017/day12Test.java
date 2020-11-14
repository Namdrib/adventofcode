package _2017;

import static org.junit.Assert.*;
import static org.hamcrest.CoreMatchers.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.junit.Before;
import org.junit.Test;

public class day12Test {
  
  private day12 a;
  List<String> input;

  @Before
  public void setUp() throws Exception {
    a = new day12();
    input = new ArrayList<String>(Arrays.asList("0 <-> 2", "1 <-> 1",
        "2 <-> 0, 3, 4", "3 <-> 2, 4", "4 <-> 2, 3, 6", "5 <-> 6", "6 <-> 4, 5"));
    a.buildGraph(input);
  }

  @Test
  public void testProgramsWithID() {
    assertEquals(6, a.programsWithID(0).size());
  }

  @Test
  public void testNumberOfGroups() {
    assertEquals(2, a.numberOfGroups());
  }

}
