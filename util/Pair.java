package util;

import java.io.Serializable;

public class Pair<T1, T2> implements Serializable
{
	private static final long serialVersionUID = -6581543748509391734L;
	public T1 first;
	public T2 second;
	
	public Pair()
	{
		this.first = null;
		this.second = null;
	}

	public Pair(T1 first, T2 second)
	{
		this.first = first;
		this.second = second;
	}

	public Pair(Pair<T1, T2> rhs)
	{
		this.first = rhs.first;
		this.second = rhs.second;
	}

	@Override
	public String toString()
	{
		return "(" + first.toString() + ", " + second.toString() + ")";
	}

	@Override
	public boolean equals(Object o)
	{
		if (!(o instanceof Pair)) return false;
		@SuppressWarnings("unchecked")
		Pair<T1, T2> other = (Pair<T1, T2>) o;
		return this.first.equals(other.first) && this.second.equals(other.second);
	}
}
