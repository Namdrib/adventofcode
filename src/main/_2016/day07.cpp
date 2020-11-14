#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2016/day/7

// Split a string into its [bracketed] and non-bracketed parts
// Non-bracketed parts are just the plain "string"
// Bracketed parts are parsed into "[string]"
vector<string> parse_ip(const string &in)
{
	vector<string> out;
	string temp;
	for (size_t i=0; i<in.size(); i++)
	{
		temp += in[i];
		if (in[i+1] == '[' || in[i] == ']' || i == in.size()-1)
		{
			out.push_back(temp);
			temp = "";
		}
	}
	return out;
}

bool has_abba(const string &in, size_t start, size_t end)
{
	for (size_t i=start; i<end-2; i++)
	{
		if (in[i] == in[i+3] &&
		    in[i+1] == in[i+2] &&
			in[i] != in[i+1])
			return true;
	}
	return false;
}

// Part 1
bool supports_tls(const string &in)
{
	bool has_valid_abba = false;
	vector<string> parts(parse_ip(in));
	for (auto part : parts)
	{
		if (part[0] == '[')
		{
			if (has_abba(part, 1, part.size()-1))
			{
				return false;
			}
		}
		else
		{
			if (has_abba(part, 0, part.size()))
			{
				has_valid_abba = true;
			}
		}
	}

	return has_valid_abba;
}

// Part 2
bool supports_ssl(const string &in)
{
	vector<string> parts(parse_ip(in));
	sort(rall(parts)); // guarantee all the [] come last

	set<string> aba; // all the aba patterns in the input
	for (auto part : parts)
	{
		if (part[0] == '[') // look for bab
		{
			// offsets for the []
			for (size_t j=1; j<part.size()-3; j++)
			{
				if (part[j] == part[j+2] && part[j] != part[j+1])
				{
					string sub = part.substr(j, 3);
					ostringstream os;
					os << sub[1] << sub[0] << sub[1];
					if (aba.count(os.str()))
					{
						return true;
					}
				}
			}
		}
		else // look for aba
		{
			for (size_t j=0; j<part.size()-2; j++)
			{
				if (part[j] == part[j+2] && part[j] != part[j+1])
				{
					string sub = part.substr(j, 3);
					aba.insert(sub);
				}
			}
		}
	}
	return false;
}

int main(int ac, char **av)
{
	// Run tests
	if (ac > 1)
	{
		// part 1
		assert(supports_tls("abba[mnop]qrst"));
		assert(!supports_tls("abcd[bddb]xyyx"));
		assert(!supports_tls("aaaa[qwer]tyui"));
		assert(supports_tls("ioxxoj[asdfgh]zxcvbn"));

		// part 2
		assert(supports_ssl("aba[bab]xyz"));
		assert(!supports_ssl("xyx[xyx]xyx"));
		assert(supports_ssl("aaa[kek]eke"));
		assert(supports_ssl("zazbz[bzb]cdb"));

		return 0;
	}

	// Take input line-by-line
	vector<string> input;
	for (string temp; getline(cin, temp);)
	{
		input.push_back(temp);
	}

	// Part 1
	int part1 = accumulate(all(input), 0, [](int acc, string s){return acc + supports_tls(s);});
	cout << "Part 1: " << part1 << endl;

	// Part 2
	int part2 = accumulate(all(input), 0, [](int acc, string s){return acc + supports_ssl(s);});
	cout << "Part 2: " << part2 << endl;
}
