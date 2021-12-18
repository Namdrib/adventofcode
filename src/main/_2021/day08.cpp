#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2021/day/08

// seven-segment display
// a single line of input should be parsed into a single ssd_entry
class ssd_entry
{
private:
	// link together the signal pattern s and the number n
	void link(string s, int n)
	{
		segments_to_digit[s] = n;
		segments_of_digit[n] = s;
	}

public:
	vector<string> signal_patterns;
	vector<string> four_digit_output;

	map<string, int> segments_to_digit;
	map<int, string> segments_of_digit;

	size_t four_digit_value;

	ssd_entry(const vector<string> &signal_patterns, const vector<string> &four_digit_output) : signal_patterns(signal_patterns), four_digit_output(four_digit_output)
	{
		// make it easier to do comparisons later on
		for (auto &s : this->signal_patterns)
		{
			sort(all(s));
		}

		for (auto &s : this->four_digit_output)
		{
			sort(all(s));
		}

		deduce_numbers();

		set_num();
	}

	// deduce which wires lead to which segments
	void deduce_numbers()
	{
		// numbers with a unique number of segments (1, 4, 7, 8)
		string signal_one   = *find_if(all(signal_patterns), [](const string &s){return s.size() == 2;});
		string signal_seven = *find_if(all(signal_patterns), [](const string &s){return s.size() == 3;});
		string signal_four  = *find_if(all(signal_patterns), [](const string &s){return s.size() == 4;});
		string signal_eight = *find_if(all(signal_patterns), [](const string &s){return s.size() == 7;});

		link(signal_one, 1);
		link(signal_seven, 7);
		link(signal_four, 4);
		link(signal_eight, 8);

		for (const auto &s : signal_patterns)
		{
			if (s.size() == 6)
			{
				// 9 has length 6 and contains all of the segments of 4 (DEPENDS ON 4)
				if (all_of(all(segments_of_digit[4]), [s](char c){return s.find(c) != string::npos;}))
				{
					link(s, 9);
				}

				// 6 has length 6 and does not contain all of the segments of 1 (DEPENDS ON 1)
				if (!all_of(all(segments_of_digit[1]), [s](char c){return s.find(c) != string::npos;}))
				{
					link(s, 6);
				}
			}
		}

		// 0 has length 6 and is neither 6 nor 9 (DEPENDS ON 6, 9)
		for (const auto &s : signal_patterns)
		{
			if (s.size() == 6 && !(s == segments_of_digit[6] || s == segments_of_digit[9]))
			{
				link(s, 0);
			}
		}

		for (const auto &s : signal_patterns)
		{
			if (s.size() == 5)
			{
				// 3 has length 5 and contains all of the segments of 7 (DEPENDS ON 7)
				if (all_of(all(segments_of_digit[7]), [s](char c){return s.find(c) != string::npos;}))
				{
					link(s, 3);
				}

				// 5 has length 5 and is a subset of the segments of 6 (DEPENDS ON 6)
				string temp = segments_of_digit[6];
				if (all_of(all(s), [temp](char c){return temp.find(c) != string::npos;}))
				{
					link(s, 5);
				}
			}
		}

		// 2 has length 5 and is neither 3 nor 5 (DEPENDS ON 3, 5)
		for (const auto &s : signal_patterns)
		{
			if (s.size() == 5 && !(s == segments_of_digit[3] || s == segments_of_digit[5]))
			{
				link(s, 2);
			}
		}
	}

	// work out what number the four_digit_output represents
	void set_num()
	{
		size_t out = 0;
		for (size_t i = 0; i < four_digit_output.size(); i++)
		{
			size_t num = segments_to_digit[four_digit_output[i]];
			num *= pow(10, four_digit_output.size() - i - 1);
			out += num;
		}
		four_digit_value = out;
	}
};

// sum of all of the 1s, 4s, 7s and 8s in the output area of all entries
size_t part_one(const vector<ssd_entry> &ssd_entries)
{
	size_t sum = 0;

	for (auto se : ssd_entries)
	{
		for (auto s : se.four_digit_output)
		{
			sum += (s.size() == 2 || s.size() == 3 || s.size() == 4 || s.size() == 7);
		}
	}

	return sum;
}

// sum of all of the output digits (treat it as a 4-digit number)
size_t part_two(const vector<ssd_entry> &ssd_entries)
{
	return accumulate(all(ssd_entries), static_cast<size_t>(0), [](size_t acc, const ssd_entry &se){return acc + se.four_digit_value;});
}

int main()
{
	// read the fold instructions
	vector<string> input = split_istream_per_line(cin);

	// read the input into ssd_entries
	vector<ssd_entry> ssd_entries;

	for (const auto s : input)
	{
		size_t pipe_pos = s.find("|");
		string before = s.substr(0, pipe_pos - 1);
		string after = s.substr(pipe_pos + 2);

		vector<string> digits_before_pipe = split_str_by_whitespace<string>(before);
		vector<string> digits_after_pipe = split_str_by_whitespace<string>(after);

		ssd_entries.push_back(ssd_entry(digits_before_pipe, digits_after_pipe));
	}

	cout << "Part 1: " << part_one(ssd_entries) << endl;
	cout << "Part 2: " << part_two(ssd_entries) << endl;
}
