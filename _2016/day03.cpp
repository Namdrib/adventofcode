#include <algorithm>
#include <cmath>
#include <iostream>
#include <sstream>
#include <vector>
using namespace std;

// http://adventofcode.com/2016/day/3

// "In a valid triangle, the sum of any two sides 
// must be larger than the remaining side."
bool possible(int a, int b, int c)
{
	return (a+b > c &&
	        a+c > b &&
	        b+c > a);
}

int main()
{
	vector<vector<int>> triSpecs;
	for (string s; getline(cin, s);)
	{
		// Get the three legnths
		stringstream ss(s);
		vector<int> v(3);
		ss >> v[0] >> v[1] >> v[2];
		triSpecs.push_back(v);
		
	}
	
	// Loop for part 1
	int numPossiblePart1 = 0;
	for (size_t i=0; i<triSpecs.size(); i++)
	{
		if (possible(triSpecs[i][0], triSpecs[i][1], triSpecs[i][2])) numPossiblePart1++;
	}
	
	// Loop for part 2
	int numPossiblePart2 = 0;
	for (size_t i=0; i<triSpecs[0].size(); i++) // Across
	{
		for (size_t j=0; j<triSpecs.size()-2; j+=3) // Down
		{
			;
			if (possible(triSpecs[j][i], triSpecs[j+1][i], triSpecs[j+2][i])) numPossiblePart2++;
			cerr << "Latest: j=" << j << endl;
		}
	}
	
	cout << numPossiblePart1 << endl;
	cout << numPossiblePart2 << endl;
}
