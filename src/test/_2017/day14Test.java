package _2017;

import static org.junit.Assert.*;
import static org.hamcrest.CoreMatchers.*;
import java.util.Arrays;
import java.util.List;
import org.junit.Before;
import org.junit.Test;

public class day14Test {

  private day14 a;
  private List<String> hashes;
  private List<List<Integer>> grid;

  @Before
  public void setUp() throws Exception {
    a = new day14();
    hashes = a.generateHashes("flqrgnkx");
    grid = a.generateGrid(hashes);
  }

  @Test
  public void testGenerateGrid() {
    assertThat(a.generateGrid(Arrays.asList("a0c20170")),
        is(Arrays.asList(Arrays.asList(-1, 0, -1, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0,
            0, 0, 0, 0, -1, 0, -1, -1, -1, 0, 0, 0, 0))));
  }

  @Test
  public void testPartOne() {
    assertEquals(8108, a.partOne(grid));
  }

  @Test
  public void testPartTwo() {
    assertEquals(1242, a.partTwo(grid));
  }

}
