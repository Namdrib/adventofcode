#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2016/day/09

size_t decomopressed_length_of(const string &s)
{
	// cout << s << endl;
	size_t out = 0;

	size_t i=0;
	// bool in_marker = false;
	// size_t start_pos, end_pos;

	for (i=0; i<s.size(); i++)
	{
		// cout << string(i, ' ') << "^" << " out: " << out << endl;
		// start reading marker
		if (s[i] == '(')
		{
			size_t match = s.find_first_of(')', i);
			string marker = s.substr(i+1, match-i-1);

			size_t x_pos = marker.find('x');
			size_t marker_length = stoi(marker.substr(0, x_pos));
			size_t marker_repeats = stoi(marker.substr(x_pos+1));
			out += marker_length * marker_repeats;
			i += marker.size() + marker_length;
			out--;
		}
		else
		{
			out++;
		}
	}

	// cout << "Length of " << s << ": " << out << endl;
	return out;
}

void expand(const string &s, size_t pos, size_t &out, string marker, size_t multiplier)
{
	// cout << "[EXPANDING] " << s << endl;
	for (size_t i=0; i<s.size(); i++)
	{
		// cout << "[EXPANDING] " << string(i, ' ') << "^" << " out: " << out << endl;
		if (s[i] == '(')
		{
			size_t match = s.find_first_of(')', i);
			string marker = s.substr(i+1, match-i-1);

			size_t x_pos = marker.find('x');
			size_t marker_length = stoi(marker.substr(0, x_pos));
			size_t marker_repeats = stoi(marker.substr(x_pos+1));

			expand(s.substr(match+1, marker_length), i, out, marker, multiplier * marker_repeats);
			i += marker.size() + marker_length;
			out -= multiplier;
		}
		else
		{
			out += multiplier;
		}
	}
}

size_t decomopressed_length_of_v2(const string &s)
{
	size_t out = 0;
	expand(s, 0, out, s, 1);

	cout << "Length of " << s << ": " << out << endl;
	return out;
}

int main()
{
	vector<string> input;
	for (string line; getline(cin, line);)
	{
		input.push_back(line);
	}

	// part 1 asserts
	assert(decomopressed_length_of("ADVENT") == 6);
	assert(decomopressed_length_of("A(1x5)BC") == 7);
	assert(decomopressed_length_of("(3x3)XYZ") == 9);
	assert(decomopressed_length_of("A(2x2)BCD(2x2)EFG") == 11);
	assert(decomopressed_length_of("(6x1)(1x3)A") == 6);
	assert(decomopressed_length_of("X(8x2)(3x3)ABCY") == 18);

	// part 2 asserts
	assert(decomopressed_length_of_v2("(3x3)XYZ") == 9);
	assert(decomopressed_length_of_v2("X(8x2)(3x3)ABCY") == 20);
	assert(decomopressed_length_of_v2("(7x10)(1x12)A") == 120); // easy version of below
	assert(decomopressed_length_of_v2("(27x12)(20x12)(13x14)(7x10)(1x12)A") == 241920);
	assert(decomopressed_length_of_v2("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN") == 445);

	size_t total_length1 = 0;
	size_t total_length2 = 0;
	for (string s : input)
	{
		total_length1 += decomopressed_length_of(s);
		total_length2 += decomopressed_length_of_v2(s);
	}
	cout << "Part 1: " << total_length1 << endl;
	cout << "Part 2: " << total_length2 << endl;
}
