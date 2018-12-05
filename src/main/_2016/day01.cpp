#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2016/day/1

// Part 1: Find how many steps away (Manhattan distance) the end of the directions are
// Part 2: How many steps away for _the first location that is visited twice_
// Note: this doesn't have to be a stopping location. Just passing through counts
int shortest_path(vector<string> directions, bool part_two)
{
	set<pair<int,int>> discovered_locations; // Locations that have been passed are added
	int delta_x = 0;
	int delta_y = 0;
	int net_dir = 0; // 0, north, a 90 degree rotation CLOCKWISE increments. 0 -> 1 -> 2 -> 3 -> 0

	for (auto direction : directions)
	{
		// Split into relevant information
		char dir = direction[0];
		int num_steps = atoi(direction.substr(1).c_str());
		// Face the new direction
		if (dir == 'L') net_dir+=3;
		else if (dir == 'R') net_dir++;
		net_dir %= 4;

		// For each step, check whether the location has been passed
		for (int j=0; j<num_steps; j++)
		{
			// Update position
			(net_dir == 0) ? delta_y-- :
			(net_dir == 1) ? delta_x++ :
			(net_dir == 2) ? delta_y++ :
			/* left */       delta_x-- ;

			// Part 2
			if (part_two)
			{
				// Check
				pair<int,int> current_location(delta_x, delta_y);
				if (discovered_locations.find(current_location) != discovered_locations.end())
				{
					return abs(delta_x) + abs(delta_y);
				}
				discovered_locations.insert(current_location);
			}
		}
	}

	return abs(delta_x) + abs(delta_y);
}

int main(int ac, char **av)
{
	// Run tests
	if (ac > 1)
	{
		// part 1
		assert(shortest_path(vector<string>({"R2", "L3"}), false) == 5);
		assert(shortest_path(vector<string>({"R2", "R2", "R2"}), false) == 2);
		assert(shortest_path(vector<string>({"R5", "L5", "R5", "R3"}), false) == 12);

		// part 2
		assert(shortest_path(vector<string>({"R8", "R4", "R4", "R8"}), true) == 4);

		return 0;
	}

	// Take and split input
	vector<string> directions;
	for (string temp; getline(cin, temp, ',');)
	{
		if (temp[0] == ' ') temp = temp.substr(1);
		directions.push_back(temp);
	}

	cout << "Part 1: " << shortest_path(directions, false) << endl;
	cout << "Part 2: " << shortest_path(directions, true) << endl;
}
