#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2016/day/16

string expand(string a) {

	string b = a;
	reverse(all(b));
	for (size_t i = 0; i < b.size(); i++) {
		if (b[i] == '0') {
			b[i] = '1';
		}
		else {
			b[i] = '0';
		}
	}

	return a + "0" + b;
}

string solve(string input, int disk_size, bool part_two) {

	string s = input;

	// expand to fit disk size
	while (s.size() < disk_size) {
		s = expand(s);
	}

	s.resize(disk_size);

	string checksum = s;

	// calculate checksum
	while (checksum.size() % 2 == 0) {
		string new_checksum;
		for (size_t i = 0; i < checksum.size(); i += 2) {
			new_checksum += (checksum[i] == checksum[i+1]) ? "1" : "0";
		}
		checksum = new_checksum;
	}

	return checksum;
}

int main()
{
	string input;
	cin >> input;

	assert(expand("1") == "100");
	assert(expand("0") == "001");
	assert(expand("11111") == "11111000000");
	assert(expand("111100001010") == "1111000010100101011110000");
	assert(solve("10000", 20, false) == "01100");

	cout << "Part 1: " << solve(input, 272, false) << endl;
	cout << "Part 2: " << solve(input, 35651584, true) << endl;
}
