#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2019/day/3

int solve(vector<string> line1, vector<string> line2, bool part_two = false)
{
	int num_steps = 0;
	int x = 0;
	int y = 0;

	// keep track of which coords have been hit
	// map<<x, y>, <has_cross?, num_steps>>
	map<pair<int, int>, pair<bool, int>> points_visited;

	for (auto s : line1)
	{
		char dir = s[0];
		int length = stoi(s.substr(1));

		for (int i=0; i<length; i++)
		{
			switch (dir)
			{
				case 'R':
					x++;
					break;

				case 'L':
					x--;
					break;

				case 'D':
					y++;
					break;

				case 'U':
					y--;
					break;
			}

			num_steps++;
			auto p = make_pair(x, y);
			if (points_visited.count(p) != 0)
			{
				points_visited[p] = make_pair(0, points_visited[p].second);
			}
			else
			{
				points_visited[p] = make_pair(0, num_steps);
			}
		}
	}

	// reset progress
	num_steps = x = y = 0;

	// keep track of which coords have been hit
	// and the int represents the line (1 for line1, 2 for line2, 3 for crossover)
	// map<pair<int, int>, int> m2;

	for (auto s : line2)
	{
		char dir = s[0];
		int length = stoi(s.substr(1));

		for (int i=0; i<length; i++)
		{
			switch (dir)
			{
				case 'R':
					x++;
					break;

				case 'L':
					x--;
					break;

				case 'D':
					y++;
					break;

				case 'U':
					y--;
					break;
			}

			auto p = make_pair(x, y);
			num_steps++;
			if (points_visited.count(p) != 0)
			{
				points_visited[p] = make_pair(1, points_visited[p].second + num_steps);
			}
		}
	}

	// Search through points_visited to find
	// the points where line1 and line2 have been through
	// calculate the output
	int answer = numeric_limits<int>::max();
	for (auto p : points_visited)
	{
		if (p.second.first == 1)
		{
			int distance = part_two ?
			               p.second.second :
			               abs(p.first.first) + abs(p.first.second);
			answer = min(answer, distance);
		}
	}

	return answer;
}

int main()
{
	string l1, l2;
	getline(cin, l1);
	getline(cin, l2);

	vector<string> line1, line2;
	stringstream ss1(l1);
	for (string temp; getline(ss1, temp, ',');)
	{
		line1.push_back(temp);
	}
	stringstream ss2(l2);
	for (string temp; getline(ss2, temp, ',');)
	{
		line2.push_back(temp);
	}

	cout << "Part 1: " << solve(line1, line2, false) << endl;
	cout << "Part 2: " << solve(line1, line2, true) << endl;
}
