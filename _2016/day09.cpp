#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2016/day/9

// "expand" the string s by multiplying certain substrings by a certain length
// performing an actual expansion on the string would take far too long and be far too large
// so just use a number `out` to keep track of the total length of expansion
// since we don't need to know the final string
//
// s: the string to expand
// out: the cumulative length (pass by ref)
// multiplier: how many times to count a character when it is encountered
//  this is the product of all the markers that came before it
// part_two: whether to recursively expand "markers"
void expand(const string &s, size_t &out, size_t multiplier, const bool part_two)
{
	for (size_t i=0; i<s.size(); i++)
	{
		if (s[i] == '(')
		{
			// see where the marker ends
			size_t match = s.find_first_of(')', i);
			string marker = s.substr(i+1, match-i-1);

			// extract the items within the marker
			size_t x_pos = marker.find('x');
			size_t marker_length = stoi(marker.substr(0, x_pos));
			size_t marker_repeats = stoi(marker.substr(x_pos+1));

			// for part two, we want to recursively expand markers
			if (part_two)
			{
				// after each recursion - the stack handles resetting multiplier
				// this avoids a costly manual division after the recursive call
				expand(s.substr(match+1, marker_length), out, multiplier * marker_repeats, part_two);
			}
			else
			{
				// for part one, skip the entire expanded section
				out += marker_length * marker_repeats;
			}

			i += marker.size() + marker_length;
			out -= multiplier;
		}
		else // normal character. repeat this char `multiplier` times
		{
			out += multiplier;
		}
	}
}

// wrapper function for the recursive `expand`
size_t decomopressed_length_of(const string &s, const bool part_two)
{
	size_t out = 0;
	expand(s, out, 1, part_two);
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
	assert(decomopressed_length_of("ADVENT", false) == 6);
	assert(decomopressed_length_of("A(1x5)BC", false) == 7);
	assert(decomopressed_length_of("(3x3)XYZ", false) == 9);
	assert(decomopressed_length_of("A(2x2)BCD(2x2)EFG", false) == 11);
	assert(decomopressed_length_of("(6x1)(1x3)A", false) == 6);
	assert(decomopressed_length_of("X(8x2)(3x3)ABCY", false) == 18);

	// part 2 asserts
	assert(decomopressed_length_of("(3x3)XYZ", true) == 9);
	assert(decomopressed_length_of("X(8x2)(3x3)ABCY", true) == 20);
	assert(decomopressed_length_of("(7x10)(1x12)A", true) == 120); // easy version of below
	assert(decomopressed_length_of("(27x12)(20x12)(13x14)(7x10)(1x12)A", true) == 241920);
	assert(decomopressed_length_of("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN", true) == 445);

	size_t total_length1 = 0;
	size_t total_length2 = 0;
	for (string s : input)
	{
		total_length1 += decomopressed_length_of(s, false);
		total_length2 += decomopressed_length_of(s, true);
	}
	cout << "Part 1: " << total_length1 << endl;
	cout << "Part 2: " << total_length2 << endl;
}
