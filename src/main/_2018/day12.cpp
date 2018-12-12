#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/12

string process(const string &input, map<string, char> rules) {

	string next_gen;
	for (size_t i = 2; i<input.size() - 1; i++) {
		string sub = input.substr(i-2, 5);
		char next = (rules.count(sub)) ? rules[sub] : '.';
		next_gen += next;
	}

	return next_gen;
}

size_t solve(string input, map<string, char> rules, size_t num_generations, bool part_two) {

	size_t out, prev;
	out = prev = 0;
	set<string> seen;

	int start = 0; // not sure if it's supposed to go negative, but it really does
	size_t i=0;
	for (i=0; i<num_generations; i++) {

		// pad lhs with '.' if necessary
		size_t first_plant = input.find_first_of("#");
		if (first_plant != string::npos) {
			int diff = 5 - first_plant;
			if (diff > 0) {
				string temp(diff, '.');
				input = temp + input;
				start += diff - 2; // not sure why this is correct
			}
		}

		// pad rhs with '.' if necessary
		size_t last_plant = input.find_last_of("#");
		if (last_plant != string::npos) {
			int diff = (last_plant + 5) - input.size();
			if (diff > 0) {
				string temp(diff, '.');
				input += temp;
			}
		}

		// process and break early if state encountered previously
		input = process(input, rules);
		if (seen.count(input) > 0) {
			break;
		}
		seen.insert(input);

		// sum of indices that contain plants
		// offset by start
		prev = out;
		out = 0;
		for (size_t i=0; i<input.size(); i++) {
			if (input[i] == '#') {
				out += i - start;
			}
		}
	}

	// there is a growth pattern
	// use this to calculate the remaining sum
	if (part_two) {
		out += (50000000000 - i) * (out - prev);
	}

	return out;
}

int main() {
	vector<string> input = split_istream_per_line(cin);

	map<string, char> rules;
	string start = input[0].substr(input[0].find_last_of(" ")+1);\

	for (size_t i=2; i<input.size(); i++) {
		string temp = input[i];
		string pattern = temp.substr(0, temp.find(" "));
		string result = temp.substr(temp.find_last_of(" ")+1);
		rules[pattern] = result[0];
	}

	cout << "Part 1: " << solve(start, rules, 20, false) << endl;
	cout << "Part 2: " << solve(start, rules, 50000000000, true) << endl;
}
