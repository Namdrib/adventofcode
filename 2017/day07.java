import static org.junit.Assert.assertEquals;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

// http://adventofcode.com/2017/day/7

public class day07
{
	List<day07Node> nodes;
	// Treat "root" as the "bottom"
	// Treat each of the programs being supported as children
	// Therefore, the, highest programs are leaf nodes at tree's ends
	public class day07Node
	{
		public String			name		= "";
		public int				weight		= 0;
		public day07Node		parent		= null;
		public List<day07Node>	children	= null;

		public day07Node(String name, int weight)
		{
			this.name = name;
			this.weight = weight;
		}
		
		// Part 2: weight stuff
		
		// recursively get weight of current and all children combined
		public int getTotalWeight()
		{
			int out = this.weight;
			if (children != null)
			{
				for (day07Node n : children)
				{
					out += n.getTotalWeight();
				}
			}
			return out;
		}
		
		public boolean hasChild(day07Node query)
		{
			for (day07Node child : children)
			{
				if (child.equals(query))
				{
					return true;
				}
			}
			return false;
		}
		
		// / Part 2: weight stuff

		public boolean equals(day07Node n)
		{
			return (this.name == n.name && this.weight == n.weight);
		}

		public String toString()
		{
			String out = name + "(" + weight + ")";
			if (children != null && children.size() > 0)
			{
				out += ":";
				for (day07Node child : children)
				{
					out += " " + child.name + "(" + child.getTotalWeight() + ")";
				}
			}
			if (parent != null)
			{
				out += " - p(" + parent.name + ")";
			}
			return out;
		}
	}
	
	public day07()
	{
		;
	}

	// Build relations of day07Nodes
	// Pass 1: build child-less nodes
	// Pass 2: build nodes with children
	public void buildTree(List<String> information)
	{
		this.nodes = new ArrayList<>();

		// Pass 1: build all nodes
		for (String s : information)
		{
			String[] parts = s.split(",? ");
			String name = parts[0];
			int weight = Integer
					.parseInt(parts[1].substring(1, parts[1].length() - 1));
			nodes.add(new day07Node(name, weight));
		}
//		System.out.println(nodes);

		// Pass 2: add all children (if applicable)
		for (String s : information)
		{
			String[] parts = s.split(",? ");
			if (parts.length > 3)
			{
				// Set the parent (current node)
				day07Node parent = null;
				for (day07Node n : nodes)
				{
					if (n.name.equals(parts[0]))
					{
						parent = n;
						break;
					}
				}

				// For each listed child name
				// Search nodes for this child and add to list of children
				// also set the child's parent to be the parent
				List<day07Node> children = new ArrayList<>();
				for (int i = 3; i < parts.length; i++)
				{
					for (day07Node n : nodes)
					{
						if (n.name.equals(parts[i]))
						{
							n.parent = parent;
							children.add(n);
							break;
						}
					}
				}

				parent.children = children;
			}
		}
	}

	// The one without a parent
	public day07Node getBottomNode()
	{
		for (day07Node n : nodes)
		{
			if (n.parent == null)
			{
				return n;
			}
		}
		return null;
	}
	
	public int getCorrectWeight()
	{
		ArrayList<day07Node> unbalanced = new ArrayList<>();
		for (day07Node n : nodes)
		{
			if (n.children == null || n.children.size() == 0) continue;
			
			Map<Integer, Integer> weightFrequency = new HashMap<>();
			for (day07Node child : n.children)
			{
				int totalWeight = child.getTotalWeight();
				int frequency = Collections.frequency(n.children, totalWeight);
				weightFrequency.put(totalWeight, frequency);
				
				if (weightFrequency.size() > 1)
				{
					unbalanced.add(child);
				}
			}
		}
		
		day07Node unbalancedNode;
		for (day07Node first : unbalanced)
		{
			boolean secondIsChildOfFirst = false;
			for (day07Node second : unbalanced)
			{
				if (first != second && first.hasChild(second))
				{
					secondIsChildOfFirst = true;
				}
			}
			if (!secondIsChildOfFirst)
			{
				System.out.println("Potentially unbalanced: " + first);
				
				System.out.println(first.parent + "\n");
			}
		}
		System.out.println("It's the one whose total weight (as a child) differs from the rest of its parents children");
		System.out.println("Its actual weight must be adjusted by the difference between its parents children and its own total weight");
		return 0;
	}
	
	private int getCorrectWeight(day07Node root)
	{
		ArrayList<day07Node> unbalanced = new ArrayList<>();
		// Get all the root's child's weights
		day07Node unbalancedNode = null;
		ArrayList<Integer> weights = new ArrayList<>();
		int benchmarkWeight = root.children.get(0).weight;
		for (int i=1; i<root.children.size(); i++)
		{
			if (root.children.get(i).weight != benchmarkWeight)
			{
				unbalanced.add(root.children.get(i));
			}
		}
		
		// Find which branch is unbalanced
		for (int i=0; i<unbalanced.size(); i++)
		{
			boolean hasChild = false;
			for (int j=0; j<unbalanced.size(); j++)
			{
				if (i != j)
				{
					if (unbalanced.get(i).hasChild(unbalanced.get(j)))
					{
						hasChild = true;
					}
				}
			}
			if (!hasChild)
			{
				day07Node unbalance = unbalanced.get(i);
				for (day07Node n : unbalance.children)
				{
					System.out.println(n + "'s total weight : " + n.getTotalWeight());
				}
			}
		}
		return 0;
	}
	
	private boolean isAllSameElement(List<Integer> list)
	{
		if (list == null || list.size() == 0) return true;
		
		int first = list.get(0);
		for (int i=1; i<list.size(); i++)
		{
			if (list.get(i) != first)
			{
				return false;
			}
		}
		return true;
	}

	public static void main(String[] args)
	{
		day07 a = new day07();

		if (args.length > 0)
		{
			a.buildTree(Arrays.asList(
				"pbga (66)",
				"xhth (57)",
				"ebii (61)",
				"havc (66)",
				"ktlj (57)",
				"fwft (72) -> ktlj, cntj, xhth",
				"qoyq (66)",
				"padx (45) -> pbga, havc, qoyq",
				"tknk (41) -> ugml, padx, fwft",
				"jptl (61)",
				"ugml (68) -> gyxo, ebii, jptl",
				"gyxo (61)",
				"cntj (57)"
			));
			assertEquals("tknk", a.getBottomNode().name);
			assertEquals(60, a.getCorrectWeight());

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

		System.out.println("building tree");
		a.buildTree(input);

		System.out.println("Part 1: " + a.getBottomNode().name);
		System.out.println("Part 2: " + a.getCorrectWeight());
	}
}

