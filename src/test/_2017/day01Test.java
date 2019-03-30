package _2017;

import static org.junit.Assert.*;
import org.junit.Before;
import org.junit.Test;

public class day01Test {

  private day01 a;

  @Before
  public void setUp() throws Exception {
    a = new day01();
  }

  @Test
  public void testSolution() {
    assertEquals(3, a.solution("1122", false));
    assertEquals(0, a.solution("1122", true));
    assertEquals(4, a.solution("1111", false));
    assertEquals(4, a.solution("1111", true));
    assertEquals(0, a.solution("1234", false));
    assertEquals(0, a.solution("1234", true));
    assertEquals(9, a.solution("91212129", false));
    assertEquals(6, a.solution("91212129", true));
    assertEquals(0, a.solution("1212", false));
    assertEquals(6, a.solution("1212", true));
    assertEquals(3, a.solution("1221", false));
    assertEquals(0, a.solution("1221", true));
    assertEquals(0, a.solution("123425", false));
    assertEquals(4, a.solution("123425", true));
    assertEquals(0, a.solution("123123", false));
    assertEquals(12, a.solution("123123", true));
    assertEquals(0, a.solution("12131415", false));
    assertEquals(4, a.solution("12131415", true));
  }

}
