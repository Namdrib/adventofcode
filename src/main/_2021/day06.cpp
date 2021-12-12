#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2021/day/6

// simulate one day passing for a school of lanternfish
// but instead of simulating the individual lanternfish,
// keep track of how many of each time of lanternfish there is left
// that way we can batch the ageing process
map<int, size_t> tick(const map<int, size_t> &remaining_lanternfish_time)
{
	map<int, size_t> out;

	// decrease all lanternfish timers by 1
	for (int i = 0; i < 8; i++)
	{
		out[i] = remaining_lanternfish_time.at(i+1);
	}

	// except for those on zero
	out[8] = remaining_lanternfish_time.at(0);
	out[6] += remaining_lanternfish_time.at(0);

	return out;
}

size_t part_one(map<int, size_t> remaining_lanternfish_time, int n)
{
	for (int i = 1; i <= n; i++)
	{
		remaining_lanternfish_time = tick(remaining_lanternfish_time);
	}

	// not casting the 0 leads to wacky behaviour
	return accumulate(all(remaining_lanternfish_time), size_t(0),
			[](size_t acc, const pair<int, size_t> &p){return acc + p.second;});
}

size_t part_two(map<int, size_t> in, int n)
{
	return part_one(in, n);
}

int main()
{
	string s;
	getline(cin, s);
	vector<int> input = extract_nums_from<int>(s);
	map<int, size_t> remaining_lanternfish_time;
	for (int i = 0; i <= 8; i++)
	{
		remaining_lanternfish_time[i] = 0;
	}
	for (auto i : input)
	{
		remaining_lanternfish_time[i]++;
	}

	cout << "Part 1: " << part_one(remaining_lanternfish_time, 80) << endl;
	cout << "Part 2: " << part_two(remaining_lanternfish_time, 256) << endl;
}
