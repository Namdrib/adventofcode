package _2017;

import static org.junit.Assert.assertEquals;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;
import util.IntegerPair;

// https://adventofcode.com/2017/day/22

public class day22
{
	int startX, startY;
	Map<IntegerPair, InfectionState> infectedNodes; // <x, y>

	// use direction in conjunction with dirX and dirY to get direction
	// in terms of change in x and y
	int direction = 0;
	final static int[] dirX = {
			0, 1, 0, -1
	};
	final static int[] dirY = {
			-1, 0, 1, 0
	};

	private enum InfectionState
	{
		CLEAN, WEAKENED, INFECTED, FLAGGED
	};

	public day22()
	{
		;
	}

	/**
	 * Initialise the program state by reading an infected file
	 * 
	 * @param infectedFile path to file containing a grid of dots and hashes
	 * @return a set of infected nodes, each node given by an IntegerPair
	 */
	private Map<IntegerPair, InfectionState> readInfected(String infectedFile)
	{
		Map<IntegerPair, InfectionState> out = new HashMap<>();

		try (BufferedReader br = new BufferedReader(new FileReader(infectedFile)))
		{
			int width = 0;
			int i = 0;
			for (String line; (line = br.readLine()) != null; i++)
			{
				width = line.length();
				for (int j = 0; j < width; j++)
				{
					if (line.charAt(j) == '#')
					{
						out.put(new IntegerPair(j, i), InfectionState.INFECTED);
					}
				}
			}
			startX = (width - 1) / 2;
			startY = (i - 1) / 2;
		}
		catch (FileNotFoundException e)
		{
			e.printStackTrace();
		}
		catch (IOException e)
		{
			e.printStackTrace();
		}
		System.out.println(out);
		return out;
	}

	/**
	 * 
	 * @param initialInfected
	 * @param numBursts the number of bursts of activity
	 * @param partTwo
	 * @return the number of bursts that cause an infection
	 */
	public int solve(Map<IntegerPair, InfectionState> initialInfected, int numBursts,
			boolean partTwo)
	{
		infectedNodes = new HashMap<>(initialInfected);
		IntegerPair currentNode = new IntegerPair(startX, startY);
		direction = 0;
		int numInfectingMoves = 0;
		
		long startTime = 0, endTime = 0;
		startTime = System.nanoTime();

		// Simulate
		for (int i = 0; i < numBursts; i++)
		{
			// See whether current tile is infected
			IntegerPair temp = null;
			InfectionState is = InfectionState.CLEAN;
			for (IntegerPair ip : infectedNodes.keySet())
			{
				if (ip.equals(currentNode))
				{
					temp = ip;
					is = infectedNodes.get(ip);
					break;
				}
			}
			infectedNodes.remove(temp);

			if (partTwo)
			{
				InfectionState targetState = null;
				switch (is)
				{
					case CLEAN:
						targetState = InfectionState.WEAKENED;
						direction -= 1;
						break;
					case FLAGGED:
						targetState = InfectionState.CLEAN;
						direction -= 2;
						break;
					case INFECTED:
						targetState = InfectionState.FLAGGED;
						direction -= 3;
						break;
					case WEAKENED:
						targetState = InfectionState.INFECTED;
						numInfectingMoves++;
						break;
					default:
						break;
				}
//				if (targetState != InfectionState.CLEAN)
				{
					infectedNodes.put(new IntegerPair(currentNode), targetState);
				}
			}
			else
			{
				if (temp == null)
				{
					// turn left
					direction -= 1;

					// infect current
					infectedNodes.put(new IntegerPair(currentNode), InfectionState.INFECTED);
					numInfectingMoves++;
				}
				else
				{
					// turn right
					direction -= 3;

					// clean current
//					infectedNodes.remove(temp);
				}
			}

			// handle direction under/overflow
			if (direction < 0)
			{
				direction += dirX.length;
			}

			// move 1 step in direction
			currentNode.first += dirX[direction];
			currentNode.second += dirY[direction];

			if (i > 0 && i % 50_000 == 0)
			{
				endTime = System.nanoTime();
				long timeTaken = (endTime - startTime) / 1_000_000;
				System.out.println(i + " took " + timeTaken + " ms, map size: " + infectedNodes.size());
				startTime = endTime;
			}
			// if (i < 8 || i == 69)
			// {
			// System.out.println("After i = " + i);
			// System.out.println(infectedNodes);
			// System.out.println(initialNode + " facing " + direction);
			// System.out.println("Num infecting moves = " + numInfectingMoves);
			// System.out.println("----------");
			// }
		}

		return numInfectingMoves;
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
		day22 a = new day22();
		if (args.length > 0)
		{
			// perform tests
			Map<IntegerPair, InfectionState> infected = a.readInfected("_2017/tests/day22_00.in");
			assertEquals(5, a.solve(infected, 7, false));
			assertEquals(41, a.solve(infected, 70, false));
			assertEquals(5_587, a.solve(infected, 10_000, false));
			assertEquals(26, a.solve(infected, 100, true));
			assertEquals(2_511_944, a.solve(infected, 10_000_000, true));

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

		Map<IntegerPair, InfectionState> infected = a.readInfected(input);
		System.out.println("Part 1: " + a.solve(infected, 10_000, false));
		System.out.println("Part 1: " + a.solve(infected, 10_000_000, true));
		// System.out.println("Part 1: " + a.partOne());
		// System.out.println("Part 2: " + a.partTwo());
	}
}
