package _2017;

import static org.junit.Assert.*;
import java.util.Arrays;
import java.util.List;
import org.junit.Before;
import org.junit.Test;

public class day09Test {

  private day09 a;

  @Before
  public void setUp() throws Exception {
    a = new day09();
  }

  @Test
  public void testClearExclamation() {
    // For garbage
    assertEquals("<{}>", a.clearExclamation("<{!>}>"));
    assertEquals("<>", a.clearExclamation("<!!>"));
    assertEquals("<>", a.clearExclamation("<!!!>>"));
    assertEquals("<{o\"i,<{i<a>", a.clearExclamation("<{o\"i!a,<{i<a>"));

    // For normal
    assertEquals("{}", a.clearExclamation("{}"));
    assertEquals("{{{}}}", a.clearExclamation("{{{}}}"));
    assertEquals("{{},{}}", a.clearExclamation("{{},{}}"));
    assertEquals("{{{},{},{{}}}}", a.clearExclamation("{{{},{},{{}}}}"));
    assertEquals("{<{},{},{{}}>}", a.clearExclamation("{<{},{},{{}}>}"));
    assertEquals("{<a>,<a>,<a>,<a>}", a.clearExclamation("{<a>,<a>,<a>,<a>}"));
    assertEquals("{{<a>},{<a>},{<a>},{<a>}", a.clearExclamation("{{<a>},{<a>},{<a>},{<a>}"));
    assertEquals("{{<},{<},{<},{<a>}}", a.clearExclamation("{{<!>},{<!>},{<!>},{<a>}}"));
    assertEquals("{{<>},{<>},{<>},{<>}}", a.clearExclamation("{{<!!>},{<!!>},{<!!>},{<!!>}}"));
    assertEquals("{{<a},{<a},{<a},{<ab>}}", a.clearExclamation("{{<a!>},{<a!>},{<a!>},{<ab>}}"));
  }

  public void testClearGarbage() {
    List<String> garbageOnly =
        Arrays.asList("<>", "<random characters>", "<<<<>", "<{}>", "<{o\"i,<{i<a>");
    for (String s : garbageOnly) {
      assertEquals("", a.clearGarbage(s));
    }
  }

  @Test
  public void testScore() {
    assertEquals(1, a.score("{}"));
    assertEquals(6, a.score("{{{}}}"));
    assertEquals(5, a.score("{{},{}}"));
    assertEquals(16, a.score("{{{},{},{{}}}}"));
    assertEquals(1, a.score("{<a>,<a>,<a>,<a>}"));
    assertEquals(9, a.score("{{<ab>},{<ab>},{<ab>},{<ab>}}"));
    assertEquals(9, a.score("{{<!!>},{<!!>},{<!!>},{<!!>}}"));
    assertEquals(3, a.score("{{<a!>},{<a!>},{<a!>},{<ab>}}"));
  }

  @Test
  public void testCharactersInGarbage() {
    assertEquals(0, a.charactersInGarbage("<>"));
    assertEquals(17, a.charactersInGarbage("<random characters>"));
    assertEquals(3, a.charactersInGarbage("<<<<>"));
    assertEquals(2, a.charactersInGarbage("<{!>}>"));
    assertEquals(0, a.charactersInGarbage("<!!>"));
    assertEquals(0, a.charactersInGarbage("<!!!>>"));
    assertEquals(10, a.charactersInGarbage("<{o\"i!a,<{i<a>"));
  }

}
