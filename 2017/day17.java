//import static org.junit.Assert.assertEquals;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

// https://adventofcode.com/2017/day/17

public class day17
{
	
	public day17()
	{
		;
	}

	// perform numInsertions on buffer, spinning spinsPerInsert on each insert
	public void spin(List<Integer> buffer, int numInsertions, int spinsPerInsert)
	{
		int position = 0;
		int counter = 1;
		for (int i=0; i<numInsertions; i++)
		{
			// perform spins
			position += spinsPerInsert;
			position %= buffer.size();

			// insert the number
			position++;
			buffer.add(position, counter);
			counter++;
		}
//		printBuffer(buffer, position);
		return;
	}
	
	private void printBuffer(List<Integer> buffer, int position)
	{
	    for (int i=0; i<buffer.size(); i++)
	    {
	        if (i == position)
	        {
	          System.out.print("(");
	        }
            System.out.print(buffer.get(i));
            if (i == position)
            {
              System.out.print(")");
            }
            if (i < buffer.size()-1)
            {
              System.out.print(" ");
            }
	    }
	    System.out.println();
	}

	public int valueAfter(List<Integer> buffer, int query)
	{
		int indexOfQuery = buffer.indexOf(query);
		int indexAfter = (indexOfQuery + 1) % buffer.size();
		return buffer.get(indexAfter);
	}

	public static void main(String[] args)
	{
		day17 a = new day17();
		int numInsertions = 2017;
		List<Integer> buffer = new ArrayList<>();
		buffer.add(0);

		if (args.length > 0)
		{
			a.spin(buffer, numInsertions, 3);
//			assertEquals(638, a.valueAfter(buffer, numInsertions));

			System.out.println("Tests successful!");
			return;
		}

		int spinsPerInsert;
		try (Scanner scanner = new Scanner(System.in))
		{
			spinsPerInsert = scanner.nextInt();
		}

		a.spin(buffer, numInsertions, spinsPerInsert);
		System.out.println("Part 1: " + a.valueAfter(buffer, numInsertions));
		buffer.clear();
		buffer.add(0);
		a.spin(buffer, 50000000, spinsPerInsert);
        System.out.println("Part 2: " + a.valueAfter(buffer, 0));
	}
}
