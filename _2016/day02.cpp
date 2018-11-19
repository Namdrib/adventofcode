#include <algorithm>
#include <cmath>
#include <iostream>
#include <set>
#include <utility>
#include <vector>
using namespace std;

// http://adventofcode.com/2016/day/2

string getCode(const vector<string> &instructions)
{
	// Part 1
	vector<vector<char>> keypad1 {
		{'1', '2', '3'},
		{'4', '5', '6'},
		{'7', '8', '9'}
	};
	// Part 2
	vector<vector<char>> keypad2 {
		{' ', ' ', '1', ' ', ' '},
		{' ', '2', '3', '4', ' '},
		{'5', '6', '7', '8', '9'},
		{' ', 'A', 'B', 'C', ' '},
		{' ', ' ', 'D', ' ', ' '}
	};
	vector<vector<char>> *keypad = &keypad2;
	const int DIM = keypad->size();
	
	// Starting point: '5'
	int x, y;
	for (int i=0; i<DIM; i++)
	{
		for (int j=0; j<DIM; j++)
		{
			if (find((*keypad)[i].begin(), (*keypad)[i].end(), '5') != ((*keypad)[i].end()))
			{
				x = j;
				y = i;
				goto FOUND_START_LOCATION;
			}
		}
	}
	FOUND_START_LOCATION:
	
	string out;
	for (size_t i=0; i<instructions.size(); i++)
	{
		// A single line of instructions
		for (size_t j=0; j<instructions[i].size(); j++)
		{
			// Work out which direction to go,
			// and whether the new key is valid
			int deltaX = 0;
			int deltaY = 0;
			char dir = instructions[i][j];
			if (dir == 'U') deltaY = -1;
			if (dir == 'D') deltaY = 1;
			if (dir == 'L') deltaX = -1;
			if (dir == 'R') deltaX = 1;
			// Going out of bounds of the keypad
			if (y+deltaY < 0 || y+deltaY >= DIM ||
			    x+deltaX < 0 || x+deltaX >= DIM ||
			    (*keypad)[y+deltaY][x+deltaX] == ' ')
				continue;
			else
			{
				y += deltaY;
				x += deltaX;
			}
			// cerr << "line " << i << ": moved to " << (*keypad)[y][x] << endl;
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
	
	cout << getCode(instructions) << endl;
}
