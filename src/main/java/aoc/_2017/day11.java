package aoc._2017;

import static org.junit.Assert.assertEquals;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

// http://adventofcode.com/2017/day/11

// Part 1: 1134 too high

// Flat-topped hexagon movement

public class day11
{

	// ----- Hex helpers -----
	public static class Cube
	{
		int x, y, z;

		public Cube()
		{
			this(0, 0, 0);
		}

		public Cube(int x, int y, int z)
		{
			this.x = x;
			this.y = y;
			this.z = z;
		}

		public Cube(Cube c)
		{
			this(c.x, c.y, c.z);
		}

		public void moveBy(int x, int y, int z)
		{
			this.x += x;
			this.y += y;
			this.z += z;
		}

		public void moveBy(Cube c)
		{
			moveBy(c.x, c.y, c.z);
		}

		public boolean equals(Cube c)
		{
			return this.x == c.x && this.y == c.y && this.z == c.z;
		}

		public int distanceTo(Cube c)
		{
			return (Math.abs(this.x - c.x) + Math.abs(this.y - c.y) + Math.abs(this.z - c.z)) / 2;
		}

		public String toString()
		{
			return "(" + this.x + "," + this.y + "," + this.z + ")";
		}
	}

	// The direction to move
	private Map<String, Cube> flatToppedCubeDirections;
	{
		Map<String, Cube> temp = new HashMap<>();
		temp.put("ne", new day11.Cube(1, 0, -1));
		temp.put("n",  new day11.Cube(0, 1, -1));
		temp.put("nw", new day11.Cube(-1, 1, 0));
		temp.put("sw", new day11.Cube(-1, 0, 1));
		temp.put("s",  new day11.Cube(0, -1, 1));
		temp.put("se", new day11.Cube(1, -1, 0));
		flatToppedCubeDirections = Collections.unmodifiableMap(temp);
	}

	private Cube cubeDirection(String direction)
	{
		return flatToppedCubeDirections.getOrDefault(direction, new Cube(0, 0, 0));
	}

	private Cube cubeNeighbour(Cube in, String direction)
	{
		return cubeAdd(in, cubeDirection(direction));
	}

	private Cube cubeAdd(Cube a, Cube b)
	{
		return new Cube(a.x + b.x, a.y + b.y, a.z + b.z);
	}

	// ----- Hex helpers -----

	public day11()
	{
		;
	}

	public int[] fewestStepsTo(List<String> input)
	{
		// Navigate from start to ending position
		final Cube origin = new Cube(0, 0, 0);
		Cube position = new Cube(origin);
		int furthest = 0;
		for (String s : input)
		{
			position = cubeNeighbour(position, s);
			furthest = Math.max(furthest, position.distanceTo(origin));
		}

		return new int[] { position.distanceTo(origin), furthest };
	}

	public static void main(String[] args)
	{
		day11 a = new day11();
		if (args.length > 0)
		{
			assertEquals(3, (a.fewestStepsTo(Arrays.asList("ne", "ne", "ne"))[0]));
			assertEquals(0, (a.fewestStepsTo(Arrays.asList("ne", "ne", "sw", "sw"))[0]));
			assertEquals(2, (a.fewestStepsTo(Arrays.asList("ne", "ne", "s", "s"))[0]));
			assertEquals(3, (a.fewestStepsTo(Arrays.asList("se", "sw", "se", "sw", "sw"))[0]));
			assertEquals(0, (a.fewestStepsTo(Arrays.asList("n", "ne", "nw", "s", "sw", "se"))[0]));

			System.out.println("Tests successful!");
			return;
		}

		List<String> input = new ArrayList<>();

		// Take input, turn into usable form
		try (Scanner scanner = new Scanner(System.in))
		{
			if (scanner.hasNextLine())
			{
				String line = scanner.nextLine();
				String[] elements = line.split(",");

				for (String element : elements)
				{
					input.add(element);
				}
			}
		}

		int[] result = a.fewestStepsTo(input);
		System.out.println("Part 1: " + result[0]);
		System.out.println("Part 2: " + result[1]);
	}
}
