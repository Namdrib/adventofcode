import static org.junit.Assert.assertEquals;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

// https://adventofcode.com/2017/day/18

public class day18
{

	Map<String, Long> registers; // <name, value>
	List<Long> soundsPlayed;
	List<Long> recoveredSounds;

	public day18()
	{
		registers = new HashMap<>();
		soundsPlayed = new ArrayList<>();
		recoveredSounds = new ArrayList<>();
	}

	public List<String> readFile(String inputFile)
	{
		List<String> out = new ArrayList<>();

		try (BufferedReader br = new BufferedReader(new FileReader(inputFile)))
		{
			for (String line; (line = br.readLine()) != null;)
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

	/**
	 * Determine whether s refers to a register entry or a value
	 * 
	 * @param s either a register entry or a value
	 * @return true if the value given by <code>s</code> is a register entry
	 */
	private boolean isRegisterEntry(String s)
	{
		try
		{
			Long.parseLong(s);
		}
		catch (Exception ex)
		{
			return true;
		}
		return false;
	}

	/**
	 * Return the value being referred to by s (whether directly or indirectly)
	 * 
	 * @param s either a register entry or a value
	 * @return the value given by register.get(s) if s is a register entry or the value s represents
	 */
	private long valueOf(String s)
	{
		return isRegisterEntry(s) ? registers.getOrDefault(s, 0L) : Long.parseLong(s);
	}

	/**
	 * Modify <code>registers</code> appropriately according to the provided instruction
	 * 
	 * A list of all instructions are as follows:
	 * <ul>
	 * <li><code>snd X</code> plays a sound with a frequency equal to the value of X.
	 * <li><code>set X Y</code> sets register X to the value of Y.
	 * <li><code>add X Y</code> increases register X by the value of Y.
	 * <li><code>mul X Y</code> sets register X to the result of multiplying the value contained in register X by the value of Y.
	 * <li><code>mod X Y</code> sets register X to the remainder of dividing the value contained in register X by the value of Y (that is, it sets X to the result of X modulo Y).
	 * <li><code>rcv X</code> recovers the frequency of the last sound played, but only when the value of X is not zero. (If it is zero, the command does nothing.)
	 * <li><code>jgz X Y</code> jumps with an offset of the value of Y, but only if the value of X is greater than zero. (An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)
	 * </ul>
	 * 
	 * Assume all instructions are correctly formatted
	 * 
	 * @param instruction instruction to process
	 */
	private void processInstructions(List<String> instructions)
	{
		int count = 0;
		insLoop:
		for (int i = 0; i < instructions.size(); i++, count++)
		{
			// System.out.println("count " + String.format("%0 4d", count) + ", ins " + String.format("% 03d", i) + ": " + instructions.get(i));
			String[] parts = instructions.get(i).split(" ");
			boolean actionTaken = false;

			switch (parts[0])
			{
				case "snd":
					// System.out.println("\tPlaying " + valueOf(parts[1]));
					soundsPlayed.add(valueOf(parts[1]));
					// System.out.println("\tSounds: " + soundsPlayed);
					break;

				case "set":
					registers.put(parts[1], valueOf(parts[2]));
					// System.out.println("\tRegister[" + parts[1] + "] = " + valueOf(parts[1]));
					break;

				case "add":
					registers.put(parts[1], registers.getOrDefault(parts[1], 0L) + valueOf(parts[2]));
					// System.out.println("\tRegister[" + parts[1] + "] = " + valueOf(parts[1]));
					break;

				case "mul":
					registers.put(parts[1], registers.getOrDefault(parts[1], 0L) * valueOf(parts[2]));
					// System.out.println("\tRegister[" + parts[1] + "] = " + valueOf(parts[1]));
					break;

				case "mod":
					registers.put(parts[1], registers.getOrDefault(parts[1], 0L) % valueOf(parts[2]));
					// System.out.println("\tRegister[" + parts[1] + "] = " + valueOf(parts[1]));
					break;

				case "rcv":
					// System.out.println("Recovering! " + valueOf(parts[1]));
					if (valueOf(parts[1]) != 0)
					{
						// System.out.println("\tRecovering " + soundsPlayed.get(soundsPlayed.size()-1));
						recoveredSounds.add(soundsPlayed.get(soundsPlayed.size()-1));
						// System.out.println("\tRecovered sounds: " + recoveredSounds);
						actionTaken = true;
						break insLoop;
					}
					if (!actionTaken)
					{
						// System.out.println("\tSkipping");
					}
					break;

				case "jgz":
					if (valueOf(parts[1]) > 0)
					{
						i--;
						i += valueOf(parts[2]);
						actionTaken = true;
					}
					if (!actionTaken)
					{
						// System.out.println("\tSkipping");
					}
					break;

				default:
					break;
			}
			// System.out.println("Registers: " + registers);
		}
	}

	public long partOne(List<String> instructions)
	{
		processInstructions(instructions);
		return recoveredSounds.get(0);
	}

	public int partTwo()
	{
		return 0;
	}

	public static void main(String[] args)
	{
		day18 a = new day18();
		if (args.length > 0)
		{
			// perform tests
			String testFile = "2017/tests/day18_00.in";
			List<String> instructions = a.readFile(testFile);

			assertEquals(4, a.partOne(instructions));
			assertEquals(0, a.partTwo());

			System.out.println("Tests successful!");
			return;
		}

		// Read a file name containing the instructions
		String inputFile = "";
		try (Scanner scanner = new Scanner(System.in))
		{
			if (scanner.hasNextLine())
			{
				inputFile = scanner.nextLine();
			}
		}

		// Do something with the input and a
		List<String> instructions = a.readFile(inputFile);
		System.out.println("Part 1: " + a.partOne(instructions));
		System.out.println("Part 2: " + a.partTwo());
	}
}
