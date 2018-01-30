import static org.junit.Assert.assertEquals;

import java.util.Scanner;

// http://adventofcode.com/2017/day/1

public class day01
{
	public day01()
	{
		;
	}

	public int solution(String input, boolean partTwo)
	{
		int sum = 0;

		for (int i = 0; i < input.length(); i++)
		{
			// Store the two digits to check
			char first = input.charAt(i);
			int nextPos = (i + ((partTwo) ? input.length()/2 : 1)) % input.length();
			char second = input.charAt(nextPos);
			
			if (first == second)
			{
				sum += (first - '0');
			}
		}

		return sum;
	}

	public static void main(String[] args)
	{
		day01 a = new day01();
		if (args.length > 0)
		{
			assertEquals(3, a.solution("1122", false));
			assertEquals(0, a.solution("1122", true));
			assertEquals(4, a.solution("1111", false));
			assertEquals(4, a.solution("1111", true));
			assertEquals(0, a.solution("1234", false));
			assertEquals(0, a.solution("1234", true));
			assertEquals(9, a.solution("91212129", false));
			assertEquals(6, a.solution("91212129", true));
			assertEquals(0, a.solution("1212", false));
			assertEquals(6, a.solution("1212", true));
			assertEquals(3, a.solution("1221", false));
			assertEquals(0, a.solution("1221", true));
			assertEquals(0, a.solution("123425", false));
			assertEquals(4, a.solution("123425", true));
			assertEquals(0, a.solution("123123", false));
			assertEquals(12, a.solution("123123", true));
			assertEquals(0, a.solution("12131415", false));
			assertEquals(4, a.solution("12131415", true));
			System.out.println("Tests successful!");
			return;
		}
		
		String input = new String();
		try (Scanner scanner = new Scanner(System.in))
		{
			System.out.print("Enter input: ");
			input = scanner.nextLine();
		}
		
		input = input.trim();
		System.out.println("Part 1: " + a.solution(input, false));
		System.out.println("Part 2: " + a.solution(input, true));
	}
}

