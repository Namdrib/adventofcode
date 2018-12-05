#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/5

// return a potentially smaller version of s by:
// looking at adjacent characters
// if they are the same character but different case (e.g. a and A)
// delete them
// keep going until no more deletions can be made
string collapse(string s) {
	while (true) {
		if (s.empty()) {
			break;
		}

		bool got_match = false;
		for (size_t i=0; i<s.size()-1; i++) {
			char c = s[i];
			char next = s[i+1];

			// if c and next match, erase them
			if ((islower(c) && isupper(next) && toupper(c) == next)
					|| (isupper(c) && islower(next) && tolower(c) == next)) {
				s.erase(i, 2);
				got_match = true;
				i-=2;
			}
		}

		// could not collapse any further
		if (!got_match) {
			break;
		}
	}
	return s;
}

// return a version of s with no occurrences of c (lower or upper case)
string strip(string s, const char &c) {
	s.erase(remove_if(all(s), [&c](char ch){
		return tolower(ch) == tolower(c);
	}), s.end());
	return s;
}

int solve(string s, bool part_two) {

	if (part_two) {
		int min_size = INT_MAX;
		string min_collapsed;

		for (char c = 'a'; c <= 'z'; c++) {
			// strip all of that char (upper and lower)
			string temp = strip(s, c);
			int collapsed_size = collapse(temp).size();

			if (collapsed_size < min_size) {
				min_collapsed = temp;
				min_size = collapsed_size;
			}
		}
		return min_size;
	}

	return collapse(s).size();
}

int main() {
	string input;
	getline(cin, input);

	assert(collapse("aA") == "");
	assert(collapse("abBA") == "");
	assert(collapse("abAB") == "abAB");
	assert(collapse("aabAAB") == "aabAAB");
	assert(collapse("dabAcCaCBAcCcaDA") == "dabCBAcaDA");

	assert(solve("dabAcCaCBAcCcaDA", false) == 10);
	assert(solve("dabAcCaCBAcCcaDA", true) == 4);

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}
