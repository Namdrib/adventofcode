#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

int decomopressed_length_of(const string &s)
{
	cout << s << endl;
	int out = 0;

	size_t i=0;
	bool in_marker = false;
	size_t start_pos, end_pos;

	for (i=0; i<s.size(); i++)
	{
		cout << string(i, ' ') << "^" << " out: " << out << endl;
		// start reading marker
		if (s[i] == '(')
		{
			size_t match = s.find_first_of(')', i);
			string marker = s.substr(i+1, match-i-1);

			size_t x_pos = marker.find('x');
			int marker_length = stoi(marker.substr(0, x_pos));
			int marker_repeats = stoi(marker.substr(x_pos+1));
			out += marker_length * marker_repeats;
			i += marker.size() + marker_length;
			out--;
		}
		else
		{
			out++;
		}
	}

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

	assert(decomopressed_length_of("ADVENT") == 6);
	assert(decomopressed_length_of("A(1x5)BC") == 7);
	assert(decomopressed_length_of("(3x3)XYZ") == 9);
	assert(decomopressed_length_of("A(2x2)BCD(2x2)EFG") == 11);
	assert(decomopressed_length_of("(6x1)(1x3)A") == 6);
	assert(decomopressed_length_of("X(8x2)(3x3)ABCY") == 18);

	int total_length = 0;
	for (string s : input)
	{
		total_length += decomopressed_length_of(s);
	}
	cout << "Part 1: " << total_length << endl;
}