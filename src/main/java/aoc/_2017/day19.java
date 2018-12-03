package aoc._2017;

import static org.junit.Assert.assertEquals;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

// http://adventofcode.com/2017/day/19

public class day19
{
	int x, y, dirX, dirY, numMoves;
	String letters;

	public day19()
	{
		init();
	}

	public void init()
	{
		x = 0;
		y = 0;
		dirX = 0;
		dirY = 1;
		numMoves = 0;
		letters = "";
	}

	// Read a network file into a list of strings
	public List<String> readNetwork(String filename)
	{
		List<String> out = new ArrayList<>();
		try (BufferedReader br = new BufferedReader(new FileReader(filename)))
		{
			String line;
			while ((line = br.readLine()) != null)
			{
				out.add(line);
			}
		}
		catch (FileNotFoundException e)
		{
			e.printStackTrace();
		}
		catch (IOException e)
		{
			e.printStackTrace();
		}

		return out;
	}

	// Take a network, traverse it and accumulate the letters
	// Return the resulting string
	// part 1 just needs out
	// part 2 needs numMoves
	public void solve(List<String> network)
	{
		// assume (0, 0) is top-left
		init();

		// find the starting column
		// in the first row, only one character isn't a space
		// this is the entry point. starting direction is always down
		String firstRow = network.get(0);
		for (int i = 0; i < firstRow.length(); i++)
		{
			if (firstRow.charAt(i) == '|')
			{
				x = i;
				break;
			}
		}

		// traverse it
		do
		{
			;
		} while (traverse(network));
	}

	// use current position (x, y) and bearing (dirX, dirY) to determine where to go next
	// apply the move by modifying the position and bearing
	// return true if a move can be made (and has been made)
	// return false if no possible move exists (surrounded by whitespace or boundary)
	boolean traverse(List<String> network)
	{
		char current = network.get(y).charAt(x);
		boolean moveMade = false; // the return value

		switch (current)
		{
			// Rely on previous bearing (dirX, dirY) to determine action
			// assume coming across one of these going the wrong way means keep going
			// e.g. if moving right and encountering a '|', keep moving right
			case '|': // fall through
			case '-':
				if (dirY != 0)
				{
					y += dirY;
					numMoves += Math.abs(dirY);
					moveMade = true;
				}
				if (dirX != 0)
				{
					x += dirX;
					numMoves += Math.abs(dirX);
					moveMade = true;
				}
				break;

			case '+':
				// need to look in every direction around the plus
				int[] deltaX = {0, 0, -1, 1};
				int[] deltaY = {-1, 1, 0, 0};
				for (int i = 0; i < deltaX.length; i++)
				{
					// don't look where we just came from
					if ((deltaX[i] == -dirX && (dirY == deltaY[i] && dirY == 0))
							|| (deltaY[i] == -dirY && (dirX == deltaX[i] && dirX == 0)))
					{
						continue;
					}

					int tempX = x + deltaX[i];
					int tempY = y + deltaY[i];
					// stop if new x,y is out of bounds
					if (tempY < 0 || tempY >= network.size() || tempX < 0
							|| tempX >= network.get(0).length())
					{
						continue;
					}

					char thing = network.get(tempY).charAt(tempX);
					// stop if looking at whitespace
					if (thing == ' ')
					{
						continue;
					}

					// make the move
					x = tempX;
					y = tempY;
					dirX = deltaX[i];
					dirY = deltaY[i];
					numMoves += Math.abs(deltaX[i]) + Math.abs(deltaY[i]);
					moveMade = true;
					break;
				}
				break;
			default:
				if (Character.isLetter(current))
				{
					letters += current;
					if (dirY != 0)
					{
						y += dirY;
						numMoves += Math.abs(dirY);
						moveMade = true;
					}
					if (dirX != 0)
					{
						x += dirX;
						numMoves += Math.abs(dirX);
						moveMade = true;
					}
				}
				break;
		}

		return moveMade;
	}

	String partOne()
	{
		return letters;
	}

	int partTwo()
	{
		return numMoves;
	}

	public static void main(String[] args)
	{
		day19 a = new day19();
		if (args.length > 0)
		{
			// perform tests
			List<String> network = a.readNetwork("2017/tests/day19_00.txt");
			a.solve(network);
			assertEquals("ABCDEF", a.partOne());
			assertEquals(38, a.partTwo());

			System.out.println("Tests successful!");
			return;
		}

		// Take input, turn into usable form
		String inputFile = null;
		try (Scanner scanner = new Scanner(System.in))
		{
			if (scanner.hasNextLine())
			{
				inputFile = scanner.next();
			}
		}

		List<String> network = a.readNetwork(inputFile);
		a.solve(network);

		System.out.println("Part 1: " + a.partOne());
		System.out.println("Part 2: " + a.partTwo());
	}
}
