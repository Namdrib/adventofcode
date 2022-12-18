#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2020/day/12

// north, east, south, west
array<int, 4> dx = { 0, 1, 0, -1};
array<int, 4> dy = {-1, 0, 1,  0};

map<char, int> dir_index_map = {{'N', 0}, {'E', 1}, {'S', 2}, {'W', 3}};

// simulate the ship's changing position in accordance with the instructions
size_t solve(const vector<string> &in, bool part_two)
{
	// start facing east
	long current_dir = dir_index_map['E'];

	// ship's current position
	long ship_x = 0;
	long ship_y = 0;

	// relative to the ship's current pos, only used for part two
	long waypoint_x = 10;
	long waypoint_y = -1;

	// process each instruction
	for (auto s : in)
	{
		char action = s[0];
		long num = extract_nums_from(s)[0];

		long target_waypoint_x;
		long target_waypoint_y;
		int num_rotations;

		switch (action)
		{
			case 'L':
				// transform the left rotation into an equivalent right rotation
				num *= -1;
				num += 360;
				// fallthrough
			case 'R':
				num_rotations = num / 90;
				num_rotations %= 4;

				if (part_two)
				{
					// rotate the waypoint left or right about the ship
					switch (num_rotations)
					{
						case 0:
							break;
						case 1:
							target_waypoint_x = -waypoint_y;
							target_waypoint_y = waypoint_x;
							break;
						case 2:
							target_waypoint_x = -waypoint_x;
							target_waypoint_y = -waypoint_y;
							break;
						case 3:
							target_waypoint_x = waypoint_y;
							target_waypoint_y = -waypoint_x;
							break;
					}
					waypoint_x = target_waypoint_x;
					waypoint_y = target_waypoint_y;
				}
				else
				{
					// rotate the ship itself left or right
					current_dir += num_rotations;
					current_dir %= 4;
				}
				break;

			case 'F':
				// move the ship either forwards or towards the waypoint
				if (part_two)
				{
					ship_x += waypoint_x * num;
					ship_y += waypoint_y * num;
				}
				else
				{
					ship_x += dx[current_dir] * num;
					ship_y += dy[current_dir] * num;
				}
				break;

			case 'N':
			case 'S':
			case 'E':
			case 'W':
				// move the ship or the waypoint a constant amount
				int movement_dir = dir_index_map[action];
				if (part_two)
				{
					waypoint_x += dx[movement_dir] * num;
					waypoint_y += dy[movement_dir] * num;
				}
				else
				{
					ship_x += dx[movement_dir] * num;
					ship_y += dy[movement_dir] * num;
				}
				break;
		}
	}

	return abs(ship_x) + abs(ship_y);
}

int main(int argc, char** argv)
{
	vector<string> input = split_istream_per_line(cin);

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}

