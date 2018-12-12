#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/12

string process(const string &input, map<string, char> rules) {

	string next_gen;
	for (int i = 2; i<input.size() - 1; i++) {
		string sub = input.substr(i-2, 5);
		// cout << "s: " << string(i-1, ' ') << sub << endl;
		next_gen += (rules[sub] == '#') ? "#" : ".";
	}

	return next_gen;
}

// No output value
// Manually determine the correct output
int solve(string input, map<string, char> rules, size_t num_generations, bool part_two) {

	set<string> seen;

	int start = 0;
	for (size_t i=0; i<num_generations; i++) {

		// pad lhs with '.' if necessary
		size_t first_plant = input.find_first_of("#");
		if (first_plant != string::npos) {
			int diff = 5 - first_plant;
			if (diff > 0) {
				string temp(diff, '.');
				input = temp + input;
				start += temp.size() - 2;
				// cout << "\tappend front: " << temp << endl;
			}
		}

		// pad rhs with '.' if necessary
		size_t last_plant = input.find_last_of("#");
		if (last_plant != string::npos) {
			// cout << "\tlast plant at " << last_plant << endl;
			int diff = (last_plant + 5) - input.size();
			// cout << "\tdiff : " << last_plant << " - " << input.size() << " = " << diff << endl;
			if (diff > 0) {
				string temp(diff, '.');
				// cout << "\tappend back: " << temp << endl;
				input += temp;
			}
		}

		seen.insert(input);
		input = process(input, rules);

		if (seen.count(input) > 0) {
			cout << "seen " << input << " before, breaking" << endl;
			break;
		}
		// cout << setw(2) << setfill(' ') << i+1 << ": " << input << endl;
		// cout << "\tstart is at " << start << endl;
	}

	int out = 0;
	for (size_t i=0; i<input.size(); i++) {
		if (input[i] == '#') {
			out += i - start;
		}
	}
	return out;

	// return accumulate(all(input), 0, [](int a, char b) {
	// 	return a + (b == '#');
	// });
}

int main() {
	// int input;
	// cin >> input;
	vector<string> input = split_istream_per_line(cin);

	map<string, char> rules;
	string start = input[0].substr(input[0].find_last_of(" ")+1);\

	for (size_t i=2; i<input.size(); i++) {
		string temp = input[i];
		string pattern = temp.substr(0, temp.find(" "));
		string result = temp.substr(temp.find_last_of(" ")+1);
		rules[pattern] = result[0];
	}

	// part 1
	// assert(solve(18, false) == "33,45");
	// assert(solve(42, false) == "21,61");

	// part 2
	// assert(solve(18, true) == "90,269,16");
	// assert(solve(42, true) == "232,251,12");

	cout << "Part 1: " << solve(start, rules, 20, false) << endl;
	cout << "Part 2: " << solve(start, rules, 50000000000, true) << endl;
}
