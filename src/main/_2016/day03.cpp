#include <bits/stdc++.h>
#include "../util/helpers.cpp"
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
	vector<vector<int>> tri_specs;
	for (string s; getline(cin, s);)
	{
		// Get the three legnths
		stringstream ss(s);
		vector<int> v(3);
		ss >> v[0] >> v[1] >> v[2];
		tri_specs.push_back(v);
	}

	// Part 1
	int part1 = accumulate(all(tri_specs), 0, [](int acc, vector<int> v){
		return acc + possible(v[0], v[1], v[2]);
	});

	// Loop for part 2
	int part2 = 0;
	for (size_t i=0; i<tri_specs[0].size(); i++) // Across
	{
		for (size_t j=0; j<tri_specs.size()-2; j+=3) // Down
		{
			if (possible(tri_specs[j][i], tri_specs[j+1][i], tri_specs[j+2][i])) part2++;
		}
	}

	cout << "Part 1: " << part1 << endl;
	cout << "Part 2: " << part2 << endl;
}
