package util;

public class IntegerPair extends Pair<Integer, Integer> {
  private static final long serialVersionUID = 7175347867071113757L;

  public IntegerPair() {
    super(0, 0);
  }

  public IntegerPair(Integer first, Integer second) {
    super(first, second);
  }

  public IntegerPair(IntegerPair rhs) {
    this(rhs.first, rhs.second);
  }
}
