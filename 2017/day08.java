import static org.junit.Assert.assertEquals;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

//http://adventofcode.com/2017/day/8

public class day08
{

	public day08()
	{
		;
	}

	// Evaluate a comparison in the form of `int [comparisonString] int`
	private boolean compare(int left, String comparison, int right)
	{
		switch (comparison)
		{
		case "==":
			return (left == right);

		case "!=":
			return (left != right);

		case "<":
			return (left < right);

		case "<=":
			return (left <= right);

		case ">":
			return (left > right);

		case ">=":
			return (left >= right);
		default:
			System.err.println("Invalid comparison: " + comparison);
			return false;
		}
	}

	// Returns int[2]{ currentMaxValue, maxEverValue }
	public int[] largestRegister(List<String> instructions)
	{
		Map<String, Integer> registers = new HashMap<>();
		int maxEverValue = Integer.MIN_VALUE;

		// Parse instructions
		for (String instruction : instructions)
		{
			String[] parts = instruction.split(" ");
			if (parts.length < 6)
			{
				System.out.println("Bad instruction: " + instruction);
				continue;
			}

			// Action (the thing to do if condition is true)
			String targetReg = parts[0];
			int mod = Integer.parseInt(parts[2]);
			if (parts[1].equals("dec")) mod *= -1;

			// Condition (skip 3 - that's the "if")
			String conditionReg = parts[4];
			String comparison = parts[5];
			int compareValue = Integer.parseInt(parts[6]);

			// Create any non-existing registers
			registers.putIfAbsent(targetReg, 0);
			registers.putIfAbsent(conditionReg, 0);

			int targetRegValue = registers.get(targetReg);
			int conditionRegValue = registers.get(conditionReg);

			// Check the condition, modify if necessary
			if (compare(conditionRegValue, comparison, compareValue))
			{
				int newValue = targetRegValue + mod;
				maxEverValue = Math.max(maxEverValue, newValue);
				registers.put(targetReg, newValue);
			}
		}

		// Find highest register
		int maxRegValue = Collections.max(registers.values());
		return new int[] { maxRegValue, maxEverValue };
	}

	public static void main(String[] args)
	{
		day08 a = new day08();

		if (args.length > 0)
		{
			ArrayList<String> input = new ArrayList<>(Arrays.asList(
				"b inc 5 if a > 1",
				"a inc 1 if b < 5",
				"c dec -10 if a >= 1",
				"c inc -20 if c == 10"
			));
			int[] maxValues = a.largestRegister(input);
			assertEquals(2, maxValues.length);
			assertEquals(1, maxValues[0]);
			assertEquals(10, maxValues[1]);

			System.out.println("Tests successful!");
			return;
		}

		List<String> input = new ArrayList<>();

		// Take input, turn into usable form
		try (Scanner scanner = new Scanner(System.in))
		{
			while (scanner.hasNextLine())
			{
				String temp = scanner.nextLine();
				input.add(temp);
			}
		}

		int[] maxValues = a.largestRegister(input);
		System.out.println("Part 1: " + maxValues[0]);
		System.out.println("Part 2: " + maxValues[1]);
	}
}

