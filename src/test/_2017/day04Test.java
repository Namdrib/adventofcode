package _2017;

import static org.junit.Assert.*;
import org.junit.Before;
import org.junit.Test;

public class day04Test {

  private day04 a;

  @Before
  public void setUp() throws Exception {
    a = new day04();
  }

  @Test
  public void testIsValidPassphrase() {
    // part 1
    assertTrue(a.isValidPassphrase("aa bb cc dd ee", false));
    assertFalse(a.isValidPassphrase("aa bb cc dd aa", false));
    assertTrue(a.isValidPassphrase("aa bb cc dd aaa", false));

    // part 2
    assertTrue(a.isValidPassphrase("abcde fghij", true));
    assertFalse(a.isValidPassphrase("abcde xyz ecdab", true));
    assertTrue(a.isValidPassphrase("a ab abc abd abf abj", true));
    assertTrue(a.isValidPassphrase("iiii oiii ooii oooi oooo", true));
    assertFalse(a.isValidPassphrase("oiii ioii iioi iiio", true));
  }

}
