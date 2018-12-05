#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2016/day/8

// `rotate column`
void shift_column(vector<string> &v, int col, int num_moves)
{
	while (num_moves--)
	{
		char temp = v[v.size()-1][col];
		for (int i=v.size()-1; i>0; i--)
		{
			v[i][col] = v[i-1][col];
		}
		v[0][col] = temp;
	}
}

// `rotate row`
void shift_row(vector<string> &v, int row, int num_moves)
{
	while (num_moves--)
	{
		char temp = v[row][v[row].size()-1];
		for (int i=v[row].size()-1; i>0; i--)
		{
			v[row][i] = v[row][i-1];
		}
		v[row][0] = temp;
	}
}

// `rect`
void init(vector<string> &v, int rows, int cols)
{
	for (int i=0; i<rows; i++)
	{
		fill_n(v[i].begin(), cols, '#');
	}
}

void parse_string(string instruction, vector<string> &v)
{
	// Tokenise `instruction`
	vector<string> instructions;
	stringstream ss(instruction);
	for (string temp; ss >> temp;)
	{
		instructions.push_back(temp);
	}

	// Perform the instruction with appropriate args
	if (instructions[0] == "rect")
	{
		size_t x_pos = instructions[1].find("x");
		int num_cols = atoi(instructions[1].substr(0, x_pos).c_str());
		int num_rows = atoi(instructions[1].substr(x_pos+1).c_str());
		init(v, num_rows, num_cols);
	}
	else // Rotate
	{
		string thing = instructions[1];
		int element = atoi(instructions[2].substr(instructions[2].find("=")+1).c_str());
		int amount = atoi(instructions[4].c_str());
		if (thing == "column") shift_column(v, element, amount);
		else shift_row(v, element, amount);
	}
}

// Count how many pixels are lit (#)
int count_pixels(const vector<string> &v)
{
	return accumulate(all(v), 0, [](int acc, string row){
		return acc + count(all(row), '#');
	});
}

int main()
{
	vector<string> demo(3, string( 7, '.'));
	vector<string> full(6, string(50, '.'));
	vector<string> *screen = &full;

	for(string temp; getline(cin, temp);)
	{
		parse_string(temp, *screen);

		// output v
		for (auto row : *screen)
		{
			cout << row << endl;
		} cout << endl;
	}
	cout << "Part 1: " << count_pixels(*screen) << endl;
	cout << "Part 2: read the ascii art on the last entry" << endl;
}
