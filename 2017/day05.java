import static org.junit.Assert.assertEquals;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

// http://adventofcode.com/2017/day/5

public class day05
{

	public day05()
	{
		;
	}

	public int numMovesToEscape(int[] maze, boolean partTwo)
	{
		int numMoves = 0;

		int position = 0;

		while (position >= 0 && position < maze.length)
		{
			int oldPosition = position;
			position += maze[position];
			if (partTwo && maze[oldPosition] >= 3)
			{
				maze[oldPosition]--;
			}
			else
			{
				maze[oldPosition]++;
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
			int[] input = new int[] { 0, 3, 0, 1, -3 };
			assertEquals(5, a.numMovesToEscape(input.clone(), false));
			assertEquals(10, a.numMovesToEscape(input.clone(), true));

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
		{
			array[i] = input.get(i);
		}
		System.out.println("Part 1: " + a.numMovesToEscape(array.clone(), false));
		System.out.println("Part 2: " + a.numMovesToEscape(array.clone(), true));

	}

}
