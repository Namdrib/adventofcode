#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2020/day/5

// for a given seat configuration, calculate its row and column
// essentially a binary search in two dimensions
pair<int, int> calculate_seat_coords(const string &s)
{
	int row_min = 0;
	int row_max = 127;

	int col_min = 0;
	int col_max = 7;

	// calculate the row
	for (size_t i = 0; i < 7; i++)
	{
		double halfway = (row_min + (row_max - row_min) / 2.0);
		if (s[i] == 'F')
		{
			row_max = floor(halfway);
		}
		else if (s[i] == 'B')
		{
			row_min = ceil(halfway);
		}
	}

	// calculate the column
	for (size_t i = 7; i < 10; i++)
	{
		double halfway = (col_min + (col_max - col_min) / 2.0);
		if (s[i] == 'L')
		{
			col_max = floor(halfway);
		}
		else if (s[i] == 'R')
		{
			col_min = ceil(halfway);
		}
	}

	return pair<int, int>{row_min, col_max};
}

size_t solve(const vector<string> &in, bool part_two = false)
{
	// calculate all the seat IDs
	vector<int> seat_ids(in.size());
	for (size_t i = 0; i < in.size(); i++)
	{
		pair<int, int> seat_coords = calculate_seat_coords(in[i]);
		int seat_id = seat_coords.first * 8 + seat_coords.second;
		seat_ids[i] = seat_id;
	}

	// makes it easier to process both parts
	sort(all(seat_ids));

	if (part_two)
	{
		// part 2: find the missing seat (the one non-consecutive one)
		for (size_t i = 0; i < seat_ids.size() - 1; i++)
		{
			// find the gap in the seats
			if (seat_ids[i + 1] - seat_ids[i] > 1)
			{
				return seat_ids[i] + 1;
			}
		}
	}
	else
	{
		// part 1: return the highest seat id
		// since it was pre-sorted, this is the highest
		return seat_ids.back();
	}

	return 0;
}


int main(int argc, char** argv)
{
	vector<string> input = split_istream_per_line(cin);

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}
