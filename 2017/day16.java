import static org.junit.Assert.assertEquals;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

// https://adventofcode.com/2017/day/16

public class day16
{

	public day16()
	{
		;
	}

	public String dance(int numPrograms, List<String> moves, long times)
	{
		// Build the line of programs
		String original = new String();
		for (char c = 'a'; c - 'a' < numPrograms; c++)
		{
			original += c;
		}
		String line = new String(original);

		for (long i = 0; i < times; i++)
		{
			if (i % 1000000 == 0) System.out.println("Set " + i);
			for (String move : moves)
			{
				line = performMove(line, move);
			}

			// Find a cycle (a point after which the line is the same as original
			// then we know don't need to keep repeating that same set.
			if (i > 0 && line.equals(original))
			{
				System.out.println("same after " + (i + 1) + " times");
				times %= (i + 1); // zero-indexed
				i = -1; // loop increments i after statement
			}
		}

		return line;
	}

	private String performMove(String line, String move)
	{
		String temp = move.substring(1);
		char arr[] = line.toCharArray();
		switch (move.charAt(0))
		{
			case 's':
			{
				int amount = Integer.parseInt(temp);
				// Rotate arr to the right by temp, then put back into line
				String end = line.substring(0, line.length() - amount);
				String begin = line.substring(line.length() - amount);
				arr = (begin + end).toCharArray();
				break;
			}
			case 'x':
			{
				String[] parts = temp.split("/");
				int a = Integer.parseInt(parts[0]);
				int b = Integer.parseInt(parts[1]);
				char swap = arr[a];
				arr[a] = arr[b];
				arr[b] = swap;
				break;
			}
			case 'p':
			{
				char a = move.charAt(1);
				char b = move.charAt(3);

				int aPos = line.indexOf(a);
				int bPos = line.indexOf(b);
				char swap = arr[aPos];
				arr[aPos] = arr[bPos];
				arr[bPos] = swap;
				break;
			}
			default:
				System.err.println("Error, first char: " + line.charAt(0));
		}
		return new String(arr);
	}

	public static void main(String[] args)
	{
		day16 a = new day16();
		if (args.length > 0)
		{
			assertEquals("baedc", a.dance(5, Arrays.asList("s1", "x3/4", "pe/b"), 1));
			assertEquals("ceadb", a.dance(5, Arrays.asList("s1", "x3/4", "pe/b"), 2));

			System.out.println("Tests successful!");
			return;
		}

		List<String> input = new ArrayList<>();

		// Take input, turn into usable form
		try (Scanner scanner = new Scanner(System.in))
		{
			String[] moves = scanner.nextLine().split(",");
			for (String s : moves)
			{
				input.add(s);
			}
		}

		System.out.println("Part 1: " + a.dance(16, input, 1));
		System.out.println("Part 2: " + a.dance(16, input, 1000000000));
	}
}
