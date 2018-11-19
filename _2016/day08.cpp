#include <algorithm>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

// http://adventofcode.com/2016/day/8

// `rotate column`
void shiftColumn(vector<string> &v, int col, int numMoves)
{
	while (numMoves--)
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
void shiftRow(vector<string> &v, int row, int numMoves)
{
	while (numMoves--)
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

void parseString(string instruction, vector<string> &v)
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
		size_t xPos = instructions[1].find("x");
		int numCols = atoi(instructions[1].substr(0, xPos).c_str());
		int numRows = atoi(instructions[1].substr(xPos+1).c_str());
		init(v, numRows, numCols);
	}
	else // Rotate
	{
		string thing = instructions[1];
		int element = atoi(instructions[2].substr(instructions[2].find("=")+1).c_str());
		int amount = atoi(instructions[4].c_str());
		if (thing == "column") shiftColumn(v, element, amount);
		else shiftRow(v, element, amount);
	}
}

// Count how many pixels are lit (#)
int countPixels(const vector<string> &v)
{
	int out = 0;
	for (auto row : v)
	{
		out += count(row.begin(), row.end(), '#');
	}
	return out;
}

int main()
{
	vector<string> demo(3, string( 7, '.'));
	vector<string> full(6, string(50, '.'));
	vector<string> *screen = &full;
	
	for(string temp; getline(cin, temp);)
	{
		parseString(temp, *screen);
		
		// output v
		for (auto row : *screen)
		{
			cout << row << endl;
		} cout << endl;
	}
	cout << countPixels(*screen) << endl;
}
