#include <bits/stdc++.h>
using namespace std;

#define all(c) (c).begin(), (c).end()

// http://adventofcode.com/2017/day/22

template <typename S, typename T>
ostream& operator << (ostream &os, pair<S, T> &p)
{
	os << "<" << p.first << ", " << p.second << ">";
	return os;
}

map<pair<int, int>, char> readInfected(const vector<string> &v, pair<int, int> &startCoords)
{
	map<pair<int, int>, char> out;

	int i, j;
	for (i=0; i<v.size(); i++)
	{
		for (j=0; j<v[i].size(); j++)
		{
			if (v[i][j] == '#')
			{
				out[make_pair(j, i)] = 'i';
			}
		}
	}

	startCoords = make_pair((j-1)/2, (i-1)/2);
	return out;
}

int solve(map<pair<int, int>, char> m, pair<int, int> node, int numBursts, bool partTwo = false)
{
	char state = 'c';
	int direction = 0;
	int dirX[] = {0, 1, 0, -1};
	int dirY[] = {-1, 0, 1, 0};
	int numInfectingMoves = 0;

	for (int i=0; i<numBursts; i++)
	{
		state = (m.find(node) == m.end()) ? 'c' : m[node];

		char targetState;
		switch (state)
		{
			case 'c':
				if (partTwo)
				{
					targetState = 'w';
				}
				else
				{
					targetState = 'i';
					numInfectingMoves++;
				}
				direction -= 1;
				break;
			case 'f':
				targetState = 'c';
				direction -= 2;
				break;
			case 'i':
				targetState = partTwo ? 'f' : 'c';
				direction -= 3;
				break;
			case 'w':
				targetState = 'i';
				numInfectingMoves++;
				break;
			default:
				break;
		}

		m[node] = targetState;

		// move
		if (direction < 0)
		{
			direction += 4;
		}

		node.first += dirX[direction];
		node.second += dirY[direction];
	}

	return numInfectingMoves;
}

int main()
{
	vector<string> infectedFile;
	for (string temp; getline(cin, temp);)
	{
		infectedFile.push_back(temp);
	}

	pair<int, int> start;
	map<pair<int, int>, char> infected = readInfected(infectedFile, start);
	cout << "Part 1: " << solve(infected, start, 10000, false) << endl;
	cout << "Part 2: " << solve(infected, start, 10000000, true) << endl;
}
