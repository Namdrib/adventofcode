import static org.junit.Assert.assertEquals;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

// http://adventofcode.com/2017/day/5

public class day05
{
	public day05()
	{
		;
	}

	public int numMovesToEscape(List<Integer> maze, boolean partTwo)
	{
		int numMoves = 0;

		int position = 0;

		while (position >= 0 && position < maze.size())
		{
			int oldPosition = position;
			position += maze.get(position);
			if (partTwo && maze.get(oldPosition) >= 3)
			{
				maze.set(oldPosition, maze.get(oldPosition) - 1);
			}
			else
			{
				maze.set(oldPosition, maze.get(oldPosition) + 1);
			}
			numMoves++;
		}

		return numMoves;
	}

	public static void main(String[] args)
	{
		day05 a = new day05();

		if (args.length > 0)
		{
			List<Integer> input = Arrays.asList(0, 3, 0, 1, -3);
			assertEquals(5, a.numMovesToEscape(new ArrayList<>(input), false));
			assertEquals(10, a.numMovesToEscape(new ArrayList<>(input), true));

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

		System.out.println("Part 1: " + a.numMovesToEscape(new ArrayList<>(input), false));
		System.out.println("Part 2: " + a.numMovesToEscape(new ArrayList<>(input), true));
	}
}
