package template;

import java.util.*;

// https://adventofcode.com/YEAR/day/DAY

public abstract class day
{
	/**
	 * solve and partX can treat each other like wrapper functions
	 * 
	 * sometimes they can both be under the same function with an if/else
	 * to determine switching logic between the two parts rather than
	 * copy/pasting entire functions of logic
	 * 
	 * if the two functions are entirely different, edit them to not call solve()
	 * 
	 * @param input
	 * @param partTwo whether to solve for partTwo
	 * @return
	 */
	public String solve(List<String> input, boolean partTwo)
	{
		String out = null;

		// TODO here

		return out;
	}

	/**
	 * Return the solution to a day's part 1
	 * @param input
	 * @return the solution to the day's part 1
	 */
	public String partOne(List<String> input)
	{
		return solve(input, false);
	}

	/**
	 * Return the solution to a day's part 2
	 * @param input
	 * @return the solution to the day's part 2
	 */
	public String partTwo(List<String> input)
	{
		return solve(input, true);
	}

//	public static void main(String[] args)
//	{
//		day a = new day01();
//		if (args.length > 0)
//		{
//			// perform tests
//
//			 assertEquals("0", a.partOne(Arrays.asList()));
//			 assertEquals("0", a.partTwo(Arrays.asList()));
//
//			System.out.println("Tests successful!");
//			return;
//		}
//
//		// Take input, turn into usable form
//		String filename = "_YEAR/dayDAY_01.in";
//		List<String> input = Util.readFileIntoListString(filename);
//
//		// Do something with the input and a
//		System.out.println("Part 1: " + a.partOne(input));
//		System.out.println("Part 2: " + a.partTwo(input));
//	}
}
