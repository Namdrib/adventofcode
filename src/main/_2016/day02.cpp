#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2016/day/2

string get_code(const vector<string> &instructions, bool part_two)
{
	// Part 1
	const vector<string> keypad1 {
		{"123"},
		{"456"},
		{"789"}
	};
	// Part 2
	const vector<string> keypad2 {
		{"  1  "},
		{" 234 "},
		{"56789"},
		{" ABC "},
		{"  D  "}
	};
	const vector<string> *keypad = part_two ? &keypad2 : &keypad1;
	const int DIM = keypad->size();

	// Starting point: '5'
	int x=0, y=0;
	for (int i=0; i<DIM; i++)
	{
		for (int j=0; j<DIM; j++)
		{
			if (find(all((*keypad)[i]), '5') != ((*keypad)[i].end()))
			{
				x = j;
				y = i;
				goto FOUND_START_LOCATION;
			}
		}
	}
	FOUND_START_LOCATION:

	string out;
	for (auto instruction : instructions)
	{
		// A single line of instructions
		for (auto dir : instruction)
		{
			// Work out which direction to go,
			// and whether the new key is valid
			int delta_x = 0;
			int delta_y = 0;
			if (dir == 'U') delta_y = -1;
			if (dir == 'D') delta_y = 1;
			if (dir == 'L') delta_x = -1;
			if (dir == 'R') delta_x = 1;
			// Going out of bounds of the keypad
			if (y + delta_y < 0 || y + delta_y >= DIM ||
			    x + delta_x < 0 || x + delta_x >= DIM ||
			    (*keypad)[y+delta_y][x+delta_x] == ' ')
				continue;
			else
			{
				y += delta_y;
				x += delta_x;
			}
		}

		// Store the ith passcode entry
		out += (*keypad)[y][x];
	}
	return out;
}

int main()
{
	vector<string> instructions;
	for (string temp; getline(cin, temp);)
	{
		instructions.push_back(temp);
	}

	cout << "Part 1: " << get_code(instructions, false) << endl;
	cout << "Part 2: " << get_code(instructions, true) << endl;
}
