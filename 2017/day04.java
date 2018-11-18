import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

// http://adventofcode.com/2017/day/4

public class day04
{

	public day04()
	{
		;
	}

	public int numCorrectPassphrases(List<String> inputs, boolean partTwo)
	{
		int out = 0;
		for (String s : inputs)
		{
			if (isValidPassphrase(s, partTwo)) out++;
		}

		return out;
	}

	public boolean isValidPassphrase(String input, boolean partTwo)
	{
		String[] words = input.split(" ");
		return !(containsDuplicates(words, partTwo));
	}

	// Returns true if more than one element identical
	private boolean containsDuplicates(String[] words, boolean partTwo)
	{
		// For anagrams, sorted words will look alike
		if (partTwo)
		{
			for (int i = 0; i < words.length; i++)
			{
				char[] temp = words[i].toCharArray();
				Arrays.sort(temp);
				words[i] = new String(temp);
			}
		}
		Arrays.sort(words);

		for (int i = 0; i < words.length - 1; i++)
		{
			if (words[i].equals(words[i + 1])) return true;
		}
		return false;
	}

	public static void main(String[] args)
	{
		day04 a = new day04();

		if (args.length > 0)
		{
			assertTrue(a.isValidPassphrase("aa bb cc dd ee", false));
			assertFalse(a.isValidPassphrase("aa bb cc dd aa", false));
			assertTrue(a.isValidPassphrase("aa bb cc dd aaa", false));

			assertTrue(a.isValidPassphrase("abcde fghij", true));
			assertFalse(a.isValidPassphrase("abcde xyz ecdab", true));
			assertTrue(a.isValidPassphrase("a ab abc abd abf abj", true));
			assertTrue(a.isValidPassphrase("iiii oiii ooii oooi oooo", true));
			assertFalse(a.isValidPassphrase("oiii ioii iioi iiio", true));
			System.out.println("Tests successful!");
			return;
		}

		List<String> inputs = new ArrayList<String>();

		try (Scanner scanner = new Scanner(System.in))
		{
			while (scanner.hasNextLine())
			{
				inputs.add(scanner.nextLine().trim());
			}
		}

		System.out.println("Part 1: " + a.numCorrectPassphrases(inputs, false));
		System.out.println("Part 2: " + a.numCorrectPassphrases(inputs, true));
	}
}
