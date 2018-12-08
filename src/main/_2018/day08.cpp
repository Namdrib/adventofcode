#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/8

int recurse(const vector<int> &input, int start, int &metadata_sum, int &value_sum, int depth) {

	int num_children = input[start];
	int num_metadata = input[start+1];

	// cout << "Node " << depth << " has " << num_children << " children, " << num_metadata << " metadata" << endl;

	while (num_children--) {
		start = recurse(input, start+2, metadata_sum, value_sum, depth+1);
	}

	for (int i=start + 2; i < start + num_metadata + 2; i++) {
		// cout << "metadata for node " << depth << ": " << input[i] << endl;
		metadata_sum += input[i];
	}

	return start + num_metadata;
}

// use bfs to solve dependencies
int solve(vector<int> input, bool part_two) {
	int metadata = 0;
	int value = 0;

	recurse(input, 0, metadata, value, 0);

	return (part_two) ? value : metadata;
}

int main() {
	vector<int> input = split_istream_by_whitespace<int>(cin);

	cout << "Part 1: " << solve(input, false) << endl;
	// cout << "Part 2: " << solve(input, true) << endl;
}
