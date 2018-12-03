package _2017;

import static org.junit.Assert.assertEquals;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.Set;

// http://adventofcode.com/2017/day/12

public class day12
{
	Map<Integer, ArrayList<day12Node>> adjList;

	public class day12Node
	{
		public int ID;
		public int groupID;

		day12Node()
		{
			this(-1);
		}

		day12Node(int ID)
		{
			this(ID, -1);
		}

		day12Node(int ID, int groupID)
		{
			this.ID = ID;
			this.groupID = groupID;
		}
	}

	public day12()
	{
		;
	}

	// Read through input and build an adjacency list
	// each node is a program, each edge is a pipe
	public void buildGraph(List<String> input)
	{
		adjList = new HashMap<>();

		for (String s : input)
		{
			// Add node
			int node = Integer.parseInt(s.substring(0, s.indexOf(" ")));
			adjList.putIfAbsent(node, new ArrayList<>());

			// Add node's neighbours
			String[] neighbours = s.substring(s.indexOf("<-> ") + 4).split(", ");
			for (String neighbour : neighbours)
			{
				adjList.get(node).add(new day12Node(Integer.parseInt(neighbour)));
			}
		}
	}

	// Set all the groupIDs of a list to groupID if they're not already set
	// return true if the groupID was assigned
	private boolean setGroupIDs(List<day12Node> list, int groupID)
	{
		if (list.isEmpty()) return false;

		if (list.get(0).groupID == -1)
		{
			for (day12Node node : list)
			{
				node.groupID = groupID;
			}
			return true;
		}
		else
		{
			return false;
		}
	}

	// Do a bfs and "touch" everything that can be reached
	public Set<Integer> programsWithID(int id)
	{
		Set<Integer> connectedPrograms = new HashSet<>();

		Set<Integer> fringe = new HashSet<>(); // programs to visit
		Set<Integer> closed = new HashSet<>(); // programs already visited
		fringe.add(id);

		while (!fringe.isEmpty())
		{
			// Get next, mark as connected, mark as part of the group
			int current = fringe.iterator().next();
			fringe.remove(current);
			connectedPrograms.add(current);
			setGroupIDs(adjList.get(current), id);

			if (closed.contains(current))
			{
				continue;
			}

			// Add all of current's neighbours to fringe
			for (Iterator<day12Node> it = adjList.get(current).iterator(); it.hasNext();)
			{
				int neighbour = it.next().ID;
				if (!closed.contains(neighbour))
				{
					fringe.add(neighbour);
				}
			}
			closed.add(current);
		}

		return connectedPrograms;
	}

	// Bad approach: run programsWithID for every ID
	// In the end, each program's ID should be set
	// Iterate through them to count how many there are
	public int numberOfGroups()
	{
		Map<Integer, ArrayList<day12Node>> temp = new HashMap<>(adjList);

		for (Map.Entry<Integer, ArrayList<day12Node>> entry : temp.entrySet())
		{
			programsWithID(entry.getKey());
		}

		// Count number of different groupIDs that occur in temp
		Set<Integer> seenGroups = new HashSet<>();
		for (Map.Entry<Integer, ArrayList<day12Node>> entry : temp.entrySet())
		{
			seenGroups.add(entry.getValue().iterator().next().groupID);
		}
		return seenGroups.size();
	}

	public static void main(String[] args)
	{
		day12 a = new day12();

		if (args.length > 0)
		{
			ArrayList<String> input = new ArrayList<String>(Arrays.asList(
				"0 <-> 2",
				"1 <-> 1",
				"2 <-> 0, 3, 4",
				"3 <-> 2, 4",
				"4 <-> 2, 3, 6",
				"5 <-> 6",
				"6 <-> 4, 5"
			));

			a.buildGraph(input);
			assertEquals(6, a.programsWithID(0).size());
			assertEquals(2, a.numberOfGroups());

			System.out.println("Tests successful!");
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

		a.buildGraph(input);
		System.out.println("Part 1: " + a.programsWithID(0).size());
		System.out.println("Part 2: " + a.numberOfGroups());
	}
}
