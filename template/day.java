package template;

import static org.junit.Assert.assertEquals;
import java.io.*;
import java.util.*;

// https://adventofcode.com/YEAR/day/DAY

public interface day
{

	public <E> String solve(List<E> input, boolean partTwo);

	public String partOne(List<String> input);

	public String partTwo(List<String> input);

	public static void main(String[] args)
	{
		// day a = new day();
		if (args.length > 0)
		{
			// perform tests

			// assertEquals("0", a.partOne());
			// assertEquals("0", a.partTwo());

			System.out.println("Tests successful!");
			return;
		}

		// Take input, turn into usable form
		String input = null;
		try (Scanner scanner = new Scanner(System.in))
		{
			if (scanner.hasNextLine())
			{
				input = scanner.next();
			}
		}

		// Do something with the input and a

		// System.out.println("Part 1: " + a.partOne());
		// System.out.println("Part 2: " + a.partTwo());
	}
}
