#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2016/day/15

class day15_disk
{
public:
	int id;
	int num_positions;
	int start_pos;

	day15_disk()
	{
		;
	}

	day15_disk(int id, int num_positions, int start_pos)
	{
		this->id = id;
		this->num_positions = num_positions;
		this->start_pos = start_pos;
	}

	// whether position will be 0 in n seconds
	bool pos_zero_in_seconds(int n) const
	{
		return (start_pos + n) % num_positions == 0;
	}
};

int solve(const vector<day15_disk> &input)
{
	int out = -1;

	int next_cycle = input[0].num_positions - input[0].start_pos - 1;
	int period = input[0].num_positions;

	// only check for those where the first disk will be aligned
	for (int i = next_cycle; ; i += period)
	{
		// for each disk
		bool bounced = false;
		for (size_t j = 0; j < input.size(); j++)
		{
			int time = i + j + 1;
			if (!input[j].pos_zero_in_seconds(time))
			{
				bounced = true;
				break;
			}
		}

		// at this point, made it through all the disks, or bounced
		// if bounced, then keep searching, otherwise return
		if (!bounced)
		{
			out = i;
			break;
		}
	}
	return out;
}

int main()
{
	vector<day15_disk> input;
	for (string line; getline(cin, line);)
	{
		vi numbers = extract_nums_from(line);
		input.push_back(day15_disk(numbers[0], numbers[1], numbers[3]));
	}

	cout << "Part 1: " << solve(input) << endl;

	input.push_back(day15_disk(-1, 11, 0));
	cout << "Part 2: " << solve(input) << endl;
}
