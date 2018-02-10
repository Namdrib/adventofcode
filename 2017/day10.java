import static org.junit.Assert.assertEquals;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Scanner;
import java.util.stream.IntStream;

// TODO : Part 2

// http://adventofcode.com/2017/day/10

public class day10
{
	List<Integer>	list;
	int				current;	// the current starting position
	int				skipSize;	// how much to increment current

	public day10()
	{
		;
	}

	// Rotate `list` starting from current to current + length (wrap around if necessary)
	// After rotating, move current forward by (length + skipSize), then increment skipSize
	public void knotRotate(int length)
	{
		if (length > list.size())
		{
			return;
		}
		
		int currentPlusLength = current + length;
		boolean overflow = (currentPlusLength > list.size());
		int overflowAmount = length - (list.size() - current);
		int boundary = overflow ? list.size() : currentPlusLength;
		
		System.out.println("rotating from " + current + " by " + length + " overflow? " + overflow);
		System.out.println("Boundary: " + boundary);
		
		// Find the area of interest to be reverse - reverse it
		List<Integer> selection = new ArrayList<>(list.subList(current, boundary));
		if (overflow)
		{
			List<Integer> beginning = new ArrayList<>(list.subList(0, overflowAmount));
			selection.addAll(beginning);
		}
		System.out.println("\tSelection: " + selection);
		Collections.reverse(selection);

		// Apply the reversed selection to the appropriate parts
		int i;
		for (i = current; i < boundary; i++)
		{
			list.set(i, selection.get(i - current));
		}
		i-= current;

		// Do overflowed part if necessary
		if (overflow)
		{
			System.out.println("Overflow part 2");
			for (int j = 0; j < overflowAmount; j++)
			{
				list.set(j, selection.get(j + i));
			}
		}

		// Admin stuff
		current += (length + skipSize);
		current %= list.size();
		skipSize++;
		
		System.out.println("New stuff:");
		System.out.println("\tList: " + list);
		System.out.println("\tItems: (c, s) " + current + " " + skipSize);
	}

	// Create the list of {start..end}
	public void init(int start, int end)
	{
		// Make the list
		int[] thing = IntStream.rangeClosed(start, end).toArray();
		list = new ArrayList<>(thing.length);
		for (int i : thing)
		{
			list.add(i);
		}

		current = 0;
		skipSize = 0;
	}

	// Perform each of the rotations
	public List<Integer> partOne(List<Integer> inputs)
	{
		for (int i : inputs)
		{
			knotRotate(i);
		}

		return list;
	}

	public static void main(String[] args)
	{
		day10 a = new day10();
		if (args.length > 0)
		{
			a.init(0, 4);
			List<Integer> input;
			input = new ArrayList<Integer>(Arrays.asList(3, 4, 1, 5));
			assertEquals(Arrays.asList(3, 4, 2, 1, 0), a.partOne(input));

			System.out.println("Tests successful!");
			return;
		}

		List<Integer> input = new ArrayList<>();

		// Take input, turn into usable form
		try (Scanner scanner = new Scanner(System.in))
		{
			if (scanner.hasNextLine())
			{
				String line = scanner.nextLine();
				String[] elements = line.split(",");

				for (String element : elements)
				{
					input.add(Integer.parseInt(element));
				}
			}
		}
		
		a.init(0, 255);
		List<Integer> afterRotations = a.partOne(input);
		System.out.println("Part 1: " + afterRotations.get(0) * afterRotations.get(1));
	}

}
