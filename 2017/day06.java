import static org.junit.Assert.assertEquals;
import java.util.ArrayList;
import java.util.Arrays;
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

	public int numMovesToRepeat(List<Integer> banks, boolean partTwo)
	{
		// For part 1, just a Set would suffice
		// For part 2, keep track of when the configuration was _first seen_
		Map<List<Integer>, Integer> previousStates = new HashMap<List<Integer>, Integer>();
		int numMoves = 0;

		while (!previousStates.containsKey(banks))
		{
			// Save the current state
			previousStates.put(banks, numMoves);

			// Find position of largest item. Implicitly takes earliest
			int largest = 0;
			int largestIndex = 0;
			for (int i = 0; i < banks.size(); i++)
			{
				if (banks.get(i) > largest)
				{
					largest = banks.get(i);
					largestIndex = i;
				}
			}

			// Distribute
			banks.set(largestIndex, banks.get(largestIndex) - largest);
			while (largest > 0)
			{
				largestIndex = (largestIndex + 1) % banks.size();
				banks.set(largestIndex, banks.get(largestIndex) + 1);
				largest--;
			}
			numMoves++;
		}

		return numMoves - ((partTwo) ? previousStates.get(banks) : 0);
	}

	public static void main(String[] args)
	{
		day06 a = new day06();

		if (args.length > 0)
		{
			List<Integer> input = Arrays.asList(0, 2, 7, 0);
			assertEquals(5, a.numMovesToRepeat(new ArrayList<>(input), false));
			assertEquals(4, a.numMovesToRepeat(new ArrayList<>(input), true));

			System.out.println("Tests successful!");
			return;
		}

		List<Integer> input = new ArrayList<Integer>();

		// Take input, turn into usable form
		try (Scanner scanner = new Scanner(System.in))
		{
			while (scanner.hasNextInt())
			{
				int temp = scanner.nextInt();
				input.add(temp);
			}
		}

		System.out.println("Part 1: " + a.numMovesToRepeat(new ArrayList<>(input), false));
		System.out.println("Part 2: " + a.numMovesToRepeat(new ArrayList<>(input), true));
	}
}

