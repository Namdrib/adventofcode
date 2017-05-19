#include <cmath>
#include <iostream>
#include <set>
#include <utility>
#include <vector>
using namespace std;

// http://adventofcode.com/2016/day/1

// Part 1: Find how many steps away (Manhattan distance) the end of the directions are
// Part 2: How many steps away for _the first location that is visited twice_
// Note: this doesn't have to be a stopping location. Just passing through counts
int shortestPath(vector<string> directions)
{
	set<pair<int,int>> discoveredLocations; // Locations that have been passed are added
	int deltaX = 0;
	int deltaY = 0;
	int netDir = 0; // 0, north, a 90 degree rotation CLOCKWISE increments. 0 -> 1 -> 2 -> 3 -> 0
	
	for (size_t i=0; i<directions.size(); i++)
	{
		// Split into relevant information
		char dir = directions[i][0];
		int numSteps = atoi(directions[i].substr(1).c_str());
		// Face the new direction
		if (dir == 'L') netDir+=3;
		else if (dir == 'R') netDir++;
		netDir %= 4;
		
		// For each step, check whether the location has been passed
		for (int j=0; j<numSteps; j++)
		{
			// Update position
			(netDir == 0) ? deltaY -- :
			(netDir == 1) ? deltaX ++ :
			(netDir == 2) ? deltaY ++ :
			/* left */      deltaX -- ;
			
			// ** PART 2: COMMENT OUT FOR PART 1 **
			// Check
			pair<int,int> currentLocation(deltaX, deltaY);
			if (discoveredLocations.find(currentLocation) != discoveredLocations.end())
			{
				cerr << "Already been to (" << deltaX << "," << deltaY << ")" << endl;
				return abs(deltaX) + abs(deltaY);
			}
			discoveredLocations.insert(currentLocation);
		}
	}
	
	cerr << "(" << deltaX << "," << deltaY << ")" << endl;
	return abs(deltaX) + abs(deltaY);
}

int main()
{
	// Take and split input
	vector<string> directions;
	for (string temp; getline(cin, temp, ',');)
	{
		if (temp[0] == ' ') temp = temp.substr(1);
		directions.push_back(temp);
	}
	
	cout << shortestPath(directions) << endl;
}