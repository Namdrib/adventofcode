import static org.junit.Assert.assertEquals;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Scanner;

// https://adventofcode.com/2017/day/DAY

public class dayDAY
{
	public dayDAY()
	{
		;
	}

	public int partOne()
	{
		return 0;
	}

	public int partTwo()
	{
		return 0;
	}

	public static void main(String[] args)
	{
		dayDAY a = new dayDAY();
		if (args.length > 0)
		{
			// perform tests

			assertEquals(0, a.partOne());
			assertEquals(0, a.partTwo());

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

		System.out.println("Part 1: " + a.partOne());
		System.out.println("Part 2: " + a.partTwo());
	}
}
