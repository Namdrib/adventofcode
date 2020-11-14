#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2019/day/2

int solve(vector<int> memory, bool part_two = false)
{
	if (part_two)
	{
		// worked this out by trial and error for my input
		// memory[1] seems to be a multiplier,
		// memory[2] is an addition on top of that
		memory[1] = 82;
		memory[2] = 50;
	}
	else
	{
		memory[1] = 12;
		memory[2] = 2;
	}

	int ip = 0; // instruction pointer
	bool keep_running = true;
	while (keep_running)
	{
		// assume input is valid - won't write out of bounds
		int opcode = memory[ip];
		int param3 = memory[ip + 3];
		int value1 = memory[memory[ip + 1]];
		int value2 = memory[memory[ip + 2]];

		switch(opcode)
		{
			case 1:
				memory[param3] = value1 + value2;
				break;

			case 2:
				memory[param3] = value1 * value2;
				break;

			case 99:
				keep_running = false;
				break;

			default:
				cout << "something went wrong, opcode=" << opcode << endl;
				break;
		}
		ip += 4; // jump to the next instruction
	}

	return part_two ? (100 * memory[1] + memory[2]) : memory[0];
}

int main()
{
	string s;
	getline(cin, s);
	vector<int> v = extract_nums_from(s);

	cout << "Part 1: " << solve(v, false) << endl;
	cout << "Part 2: " << solve(v, true) << endl;
}
