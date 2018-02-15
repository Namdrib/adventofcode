import static org.junit.Assert.assertEquals;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

// https://adventofcode.com/2017/day/13

public class day13
{
	public class FirewallLayer
	{
		int		depth;		// how many layers deep into the firewall (starting with 0);
		int		range;		// how far this layer scans
		int		current;	// where the scanner currently is (should be between 0, range-1 (inclusive))
		boolean	direction;	// false to scan "down" (0 to range-1), true to scan "up" (range-1 to 0)

		FirewallLayer()
		{
			this(0);
		}

		FirewallLayer(int range)
		{
			this(0, range);
		}

		FirewallLayer(int depth, int range)
		{
			this.depth = Math.max(0, depth);
			this.range = Math.max(0, range);

			init();
		}

		void init()
		{
			current = 0;
			direction = false;
		}

		// Make the scanner tick along one position.
		// Check for change in direction if necessary
		void tick()
		{
			if (!direction)
			{
				current++;
				if (current == range - 1)
				{
					direction = !direction;
				}
			}
			else
			{
				current--;
				if (current == 0)
				{
					direction = !direction;
				}
			}
		}

	}

	public day13()
	{
		;
	}
	
	private Map<Integer, FirewallLayer> init(List<String> input)
	{
		Map<Integer, FirewallLayer> firewall = new HashMap<>();
		
		String[] elements = input.toArray(new String[input.size()]);
		for (String s : elements)
		{
			String[] temp = s.split("(:\\ )");

			int depth = Integer.parseInt(temp[0]);
			int range = Integer.parseInt(temp[1]);

			firewall.put(depth, new FirewallLayer(depth, range)); // Maybe don't need ctor depth
			// firewall.add(new FirewallLayer(depth, range));
		}
		
		return firewall;
	}

	public int makeTrip(List<String> input)
	{
		Map<Integer, FirewallLayer> firewall = init(input);
		int lastLayer = Integer.parseInt(input.get(input.size()-1).split(":\\ ")[0]);

		// Run simulation
		int cost = 0;
		int packetDepth = -1;

		while (packetDepth < lastLayer)
		{
			packetDepth++;
			FirewallLayer currentLayer = firewall.get(packetDepth);

			// Check caught
			if (currentLayer != null)
			{
				if (currentLayer.current == 0)
				{
					cost += packetDepth * currentLayer.range;
				}
			}

			// Advance all scanners
			for (FirewallLayer layer : firewall.values())
			{
				layer.tick();
			}
		}

		return cost;
	}
	
	// Returns true if the packet will get caught trying to run with delay `delay`
	// Caught if a given layer's scanner is at position 0 when packet reaches it
	// Since it's oscillating, the period is `2 * (layer.range - 1)`
	private boolean getCaughtWithDelay(Map<Integer, FirewallLayer> firewall, int delay)
	{
		for (FirewallLayer layer : firewall.values())
		{
			if ((layer.depth + delay) % (2 * (layer.range - 1)) == 0)
			{
				return true;
			}
		}
		return false;
	}

	// A sign of being caught is cost > 0
	// Therefore, try every delay until makeTrip(input, i) == 0
	// Want to delay lowest length of time to pass through without caught
	int lowestDelay(List<String> input)
	{
		Map<Integer, FirewallLayer> firewall = init(input);
		
		for (int i=0; ; i++)
		{
			if (!getCaughtWithDelay(firewall, i))
			{
				return i;
			}
		}
	}

	public static void main(String[] args)
	{
		day13 a = new day13();
		if (args.length > 0)
		{
			List<String> input;
			input = new ArrayList<>(
					Arrays.asList("0: 3", "1: 2", "4: 4", "6: 4"));

			assertEquals(24, a.makeTrip(input));
			assertEquals(10, a.lowestDelay(input));

			System.out.println("Tests successful!");
			return;
		}

		List<String> input = new ArrayList<>();

		// Take input, turn into usable form
		try (Scanner scanner = new Scanner(System.in))
		{
			while (scanner.hasNextLine())
			{
				String line = scanner.nextLine();
				input.add(line);
			}
		}

		System.out.println("Part 1: " + a.makeTrip(input));
		System.out.println("Part 2: " + a.lowestDelay(input));
	}
}
