#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2019/day/6

const string COM = "COM";
const string SAN = "SAN";
const string YOU = "YOU";

void get_distance(const map<string, set<string>> &adj_list, set<string> visited, string source, string target, int depth, int &depth_out)
{
	if (source == target)
	{
		depth_out = depth;
		return;
	}
	if (adj_list.find(source) == adj_list.end())
	{
		return;
	}
	visited.insert(source);

	// visit each unvisited child
	for (auto child : adj_list.at(source))
	{
		if (visited.find(child) == visited.end())
		{
			get_distance(adj_list, visited, child, target, depth+1, depth_out);
		}
	}
}

// perform dfs to get the distance between two nodes (source, target)
// assume weighting of exactly 1 between each connected node
// in the event where `source` is `COM`, gives the depth of `target`
int get_distance(const map<string, set<string>> &adj_list, string source, string target)
{
	int depth = 0;
	set<string> visited;
	get_distance(adj_list, visited, source, target, 0, depth);
	return depth;
}

int solve(map<string, set<string>> adj_list, set<string> nodes, bool part_two = false)
{
	int out = 0;

	if (part_two)
	{
		// find the planets beign orbited by SAN and YOU
		string san_parent, you_parent;
		for (auto p : adj_list)
		{
			if (p.second.find(SAN) != p.second.end())
			{
				san_parent = p.first;
			}
			if (p.second.find(YOU) != p.second.end())
			{
				you_parent = p.first;
			}
		}

		out = get_distance(adj_list, san_parent, you_parent);
	}
	else
	{
		// out depth of all nodes
		// (where depth is distance between COM and the node)
		for (auto node : nodes)
		{
			out += get_distance(adj_list, COM, node);
		}
	}

	return out;
}

int main()
{
	vector<string> input = split_istream_per_line(cin);

	map<string, set<string>> m;
	set<string> nodes;
	nodes.insert("COM");
	for (auto s : input)
	{
		string left = s.substr(0, s.find(')'));
		string right = s.substr(s.find(')') + 1);

		m[left].insert(right);
		m[right].insert(left);
		nodes.insert(right);
	}

	cout << "Part 1: " << solve(m, nodes, false) << endl;
	cout << "Part 2: " << solve(m, nodes, true) << endl;
}
