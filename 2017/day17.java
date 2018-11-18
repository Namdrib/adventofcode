import static org.junit.Assert.assertEquals;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

// https://adventofcode.com/2017/day/17

public class day17
{

	public day17()
	{
		;
	}

	public int partOne(int numInsertions, int spinsPerInsert, int query)
	{
		List<Integer> buffer = new ArrayList<>();
		buffer.add(0);
		int position = 0;
		int counter = 1; // number being inserted

		// spin the buffer
		// perform numInsertions on buffer, spinning spinsPerInsert on each insert
		for (int i = 0; i < numInsertions; i++)
		{
			// perform spins
			position += spinsPerInsert;
			position %= buffer.size();

			// insert the number
			position++;
			buffer.add(position, counter);
			counter++;
		}

		// return the value after `query`
		int indexOfQuery = buffer.indexOf(query);
		int indexAfter = (indexOfQuery + 1) % buffer.size();
		return buffer.get(indexAfter);
	}

	// return the value after `target` after `numInsertions` insertions
	// at `spinsPerInsert` spins per insertion
	// simulating the buffer takes way too long
	// so we work it out without the buffer
	// only need to keep track of the number at the position `target+1`
	public int partTwo(int target, int numInsertions, int spinsPerInsert)
	{
		int position = 0;
		int counter = 1; // number being inserted
		int size = 1; // size of the buffer

		int valueAfterTarget = 0;

		// make a half-arsed simulation without manipulating a buffer
		// just use information I know like length, insertions, spins, etc.
		for (int i = 0; i < numInsertions; i++)
		{
			// perform spins
			position += spinsPerInsert;
			position %= size;

			// "insert" the number
			// if we are inserting directly after `target`, record it
			position++;
			if (position == (target + 1) % size)
			{
				valueAfterTarget = counter;
			}
			size++;
			counter++;
		}

		return valueAfterTarget;
	}

	public static void main(String[] args)
	{
		day17 a = new day17();
		int numInsertions = 2017;
		List<Integer> buffer = new ArrayList<>();
		buffer.add(0);

		if (args.length > 0)
		{
			assertEquals(638, a.partOne(numInsertions, 3, numInsertions));

			System.out.println("Tests successful!");
			return;
		}

		int spinsPerInsert;
		try (Scanner scanner = new Scanner(System.in))
		{
			spinsPerInsert = scanner.nextInt();
		}

		System.out.println("Part 1: " + a.partOne(numInsertions, spinsPerInsert, numInsertions));
		System.out.println("Part 2: " + a.partTwo(0, 50_000_000, spinsPerInsert));
	}
}
