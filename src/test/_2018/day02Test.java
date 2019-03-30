package _2018;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;
import java.util.Arrays;
import org.junit.Before;
import org.junit.Test;

public class day02Test {

  private day02 a;

  @Before
  public void setUp() throws Exception {
    a = new day02();
  }

  @Test
  public void testPartOne() {
    assertEquals("12", a.partOne(
        Arrays.asList("abcdef", "bababc", "abbcde", "abcccd", "aabcdd", "abcdee", "ababab")));
  }

  @Test
  public void testPartTwo() {
    assertEquals("fgij",
        a.partTwo(Arrays.asList("abcde", "fghij", "klmno", "pqrst", "fguij", "axcye", "wvxyz")));
  }

  @Test
  public void testHasN() {
    assertTrue(a.hasN("Hello", 'l', 2));
    assertFalse(a.hasN("Hello", 'l', 3));
    assertFalse(a.hasN("Hello", 'l', 1));
    assertTrue(a.hasN("Hello", 'z', 0));
    assertTrue(a.hasN("Hello", 'L', 0));
    assertTrue(a.hasN("1234", '1', 1));
  }

  @Test
  public void testNumDiffLetters() {
    assertEquals(0, a.numDiffLetters("same", "same"));
    assertEquals(4, a.numDiffLetters("same", "different"));
    assertEquals(4, a.numDiffLetters("different", "same"));
  }

}
