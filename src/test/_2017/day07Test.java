package _2017;

import static org.junit.Assert.*;
import java.util.Arrays;
import org.junit.Before;
import org.junit.Test;

public class day07Test {

  private day07 a;

  @Before
  public void setUp() throws Exception {
    a = new day07();
  }

  @Test
  public void testEverything() {
    a.buildTree(Arrays.asList("pbga (66)", "xhth (57)", "ebii (61)", "havc (66)", "ktlj (57)",
        "fwft (72) -> ktlj, cntj, xhth", "qoyq (66)", "padx (45) -> pbga, havc, qoyq",
        "tknk (41) -> ugml, padx, fwft", "jptl (61)", "ugml (68) -> gyxo, ebii, jptl", "gyxo (61)",
        "cntj (57)"));
    assertEquals("tknk", a.getBottomNode().name);
    // assertEquals(60, a.getCorrectWeight());
  }

}
