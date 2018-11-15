import static org.junit.Assert.assertEquals;

import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

// http://adventofcode.com/2017/day/8

public class day09
{

	public day09()
	{
		;
	}

	// Clear the effect of '!' in input
	// Should be used as the first "filter"
	private String clearExclamation(String input)
	{
		String out = new String();
		for (int i = 0; i < input.length(); i++)
		{
			if (input.charAt(i) == '!')
			{
				i++;
			}
			else
			{
				out += input.charAt(i);
			}
		}
		return out;
	}

	// Loop through input until first '<'
	// ignore everything until first '>'
	// remove everything in between (inclusive)
	// repeat
	private String clearGarbage(String input)
	{
		String out = "";
		boolean inGarbage = false;
		for (int i = 0; i < input.length(); i++)
		{
			char current = input.charAt(i);
			if (inGarbage)
			{
				if (current == '>')
				{
					inGarbage = false;
				}
			}
			else
			{
				if (current == '<')
				{
					inGarbage = true;
				}
				else
				{
					out += current;
				}
			}
		}

		return out;
	}

	public int score(String input)
	{
		input = clearExclamation(input);
		input = clearGarbage(input);

		// At this point, should only be left with braces and commas
		// Loop through the string, accumulating potential "points" as a new "{" is encountered
		// When a "}" is matched, add those points to the score and reduce points by 1
		// basically each layer +1 point
		int score = 0;

		int pointsForClosing = 0;
		for (int i = 0; i < input.length(); i++)
		{
			char current = input.charAt(i);
			if (current == '{')
			{
				pointsForClosing++;
			}
			else if (current == '}')
			{
				score += pointsForClosing;
				pointsForClosing--;
			}
		}

		return score;
	}

	public int charactersInGarbage(String input)
	{
		input = clearExclamation(input);

		int out = 0;

		boolean counting = false;
		for (int i = 0; i < input.length(); i++)
		{
			char current = input.charAt(i);
			if (counting)
			{
				if (current == '>')
				{
					counting = false;
				}
				else
				{
					out++;
				}
			}
			else
			{
				if (current == '<')
				{
					counting = true;
				}
			}
		}

		return out;
	}

	public static void main(String[] args)
	{
		day09 a = new day09();

		if (args.length > 0)
		{
			// Helper functions
			List<String> garbageOnly = Arrays.asList(
				"<>", "<random characters>", "<<<<>", "<{}>", "<{o\"i,<{i<a>"
			);
			for (String s : garbageOnly)
			{
				assertEquals("", a.clearGarbage(s));
			}

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

			// Part 1
			assertEquals(1, a.score("{}"));
			assertEquals(6, a.score("{{{}}}"));
			assertEquals(5, a.score("{{},{}}"));
			assertEquals(16, a.score("{{{},{},{{}}}}"));
			assertEquals(1, a.score("{<a>,<a>,<a>,<a>}"));
			assertEquals(9, a.score("{{<ab>},{<ab>},{<ab>},{<ab>}}"));
			assertEquals(9, a.score("{{<!!>},{<!!>},{<!!>},{<!!>}}"));
			assertEquals(3, a.score("{{<a!>},{<a!>},{<a!>},{<ab>}}"));

			// Part 2
			assertEquals(0, a.charactersInGarbage("<>"));
			assertEquals(17, a.charactersInGarbage("<random characters>"));
			assertEquals(3, a.charactersInGarbage("<<<<>"));
			assertEquals(2, a.charactersInGarbage("<{!>}>"));
			assertEquals(0, a.charactersInGarbage("<!!>"));
			assertEquals(0, a.charactersInGarbage("<!!!>>"));
			assertEquals(10, a.charactersInGarbage("<{o\"i!a,<{i<a>"));

			System.out.println("Tests successful!");
			return;
		}

		String input = new String();
		try (Scanner scanner = new Scanner(System.in))
		{
			if (scanner.hasNextLine())
			{
				input = scanner.nextLine();
			}
		}

		System.out.println("Part 1: " + a.score(input));
		System.out.println("Part 2: " + a.charactersInGarbage(input));
	}
}

