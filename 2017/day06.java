import static org.junit.Assert.assertEquals;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

// http://adventofcode.com/2017/day/6

public class day06
{

	public day06()
	{
		;
	}

	public int numMovesToRepeat(int[] banks, boolean partTwo)
	{
		// For part 1, just a Set would suffice
		// For part 2, keep track of when the configuration was _first seen_
		Map<List<Integer>, Integer> previousStates = new HashMap<List<Integer>, Integer>();
		int numMoves = 0;

		while (!previousStates.containsKey(arrayToList(banks)))
		{
			// Save the current state
			previousStates.put(arrayToList(banks), numMoves);

			// Find position of largest item. Implicitly takes earliest
			int largest = 0;
			int largestIndex = 0;
			for (int i = 0; i < banks.length; i++)
			{
				if (banks[i] > largest)
				{
					largest = banks[i];
					largestIndex = i;
				}
			}

			// Distribute
			banks[largestIndex] -= largest;
			while (largest > 0)
			{
				largestIndex = (largestIndex + 1) % banks.length;
				banks[largestIndex]++;
				largest--;
			}

			numMoves++;
		}

		return numMoves - ((partTwo) ? previousStates.get(arrayToList(banks)) : 0);
	}

	// Array of primitives into List of Objects
	private List<Integer> arrayToList(int[] state)
	{
		List<Integer> out = new ArrayList<Integer>();
		for (int i : state)
		{
			out.add(i);
		}
		return out;
	}

	public static void main(String[] args)
	{
		day06 a = new day06();

		if (args.length > 0)
		{
			int[] input = new int[] { 0, 2, 7, 0 };
			assertEquals(5, a.numMovesToRepeat(input.clone(), false));
			assertEquals(4, a.numMovesToRepeat(input.clone(), true));

			System.out.println("Tests successful!");
			return;
		}

		List<Integer> input = new ArrayList<Integer>();

		// Take input, turn into usable form
		Scanner scanner = new Scanner(System.in);
		while (scanner.hasNextInt())
		{
			int temp = scanner.nextInt();
			input.add(temp);
		}
		scanner.close();

		int[] array = new int[input.size()];
		for (int i = 0; i < input.size(); i++)
			array[i] = input.get(i);
		System.out
				.println("Part 1: " + a.numMovesToRepeat(array.clone(), false));
		System.out
				.println("Part 2: " + a.numMovesToRepeat(array.clone(), true));

	}

}
