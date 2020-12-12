#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2020/day/11

// delta in x/y. starts going upwards, rotate clockwise
array<int, 8> dx = { 0,  1, 1, 1, 0, -1, -1, -1};
array<int, 8> dy = {-1, -1, 0, 1, 1,  1,  0, -1};

// calcualte the number occupied seats visible from in[row][col]
int calc_num_visible_occupied_seats(const vector<string> &in, long row, long col, bool part_two)
{
	int num_visible_occupied_seats = 0;

	// for part one, only look at adjacent seats (scale = 1)
	// for part two, look down that entire direction until a seat is found
	const long scale_limit = (part_two) ? in.size() : 1;

	// for each direction
	for (size_t dir = 0; dir < dx.size(); dir++)
	{
		// look from closest until we find a seat
		for (long scale = 0; scale < scale_limit; scale++)
		{
			long new_x = col + dx[dir] * (scale + 1);
			long new_y = row + dy[dir] * (scale + 1);

			if (new_y < 0 || new_y >= in.size()) continue;
			if (new_x < 0 || new_x >= in[new_y].size()) continue;
			if (new_y == row && new_x == col) continue;

			// we have found a seat, stop looking further in this direction
			if (in[new_y][new_x] != '.')
			{
				if (in[new_y][new_x] == '#')
				{
					num_visible_occupied_seats++;
				}
				break;
			}
		}
	}

	return num_visible_occupied_seats;
}

// determine what a in[row][col] would become
char process_rules(const vector<string> &in, long row, long col, bool part_two)
{
	int num_visible_occupied_seats = calc_num_visible_occupied_seats(in, row, col, part_two);

	const int visible_seat_tolerance = (part_two) ? 5 : 4;
	if (in[row][col] == 'L')
	{
		if (num_visible_occupied_seats == 0)
		{
			return '#';
		}
	}
	else if (in[row][col] == '#')
	{
		if (num_visible_occupied_seats >= visible_seat_tolerance)
		{
			return 'L';
		}
	}

	return in[row][col];
}

// perform a step of conway's game of life, returning the resulting state
vector<string> step(const vector<string> &in, bool part_two)
{
	vector<string> out(in.size(), string(in[0].size(), ' '));

	for (long i = 0; i < in.size(); i++)
	{
		for (long j = 0; j < in[i].size(); j++)
		{
			char c = process_rules(in, i, j, part_two);
			out[i][j] = c;
		}
	}

	return out;
}

size_t solve(const vector<string> &in, bool part_two)
{
	size_t out = 0;

	vector<string> prev = in;
	vector<string> working_copy;

	// keep stepping until there are no changes
	while (true)
	{
		working_copy = step(prev, part_two);

		if (working_copy == prev)
		{
			break;
		}
		prev = working_copy;
	}

	// count num '#' in all of working_copy
	size_t num_seats = 0;
	for (auto s : working_copy)
	{
		for (auto c : s)
		{
			if (c == '#')
			{
				num_seats++;
			}
		}
	}
	out = num_seats;

	return out;
}

int main()
{
	vector<string> input = split_istream_per_line(cin);

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}
