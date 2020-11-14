package _2017;

import static org.junit.Assert.*;
import static org.hamcrest.CoreMatchers.*;
import java.util.Arrays;
import org.junit.Before;
import org.junit.Test;

public class day11Test {

  private day11 a;

  @Before
  public void setUp() throws Exception {
    a = new day11();
  }

  @Test
  public void testFewestStepsTo() {
    assertThat(a.fewestStepsTo(Arrays.asList("ne", "ne", "ne")), is(new int[] {3, 3}));
    assertThat(a.fewestStepsTo(Arrays.asList("ne", "ne", "sw", "sw")), is(new int[] {0, 2}));
    assertThat(a.fewestStepsTo(Arrays.asList("ne", "ne", "s", "s")), is(new int[] {2, 2}));
    assertThat(a.fewestStepsTo(Arrays.asList("se", "sw", "se", "sw", "sw")), is(new int[] {3, 3}));
    assertThat(a.fewestStepsTo(Arrays.asList("n", "ne", "nw", "s", "sw", "se")),
        is(new int[] {0, 2}));
  }

}
