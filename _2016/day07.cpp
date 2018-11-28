#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;


// Split a string into its [bracketed] and non-bracketed parts
// Non-bracketed parts are just the plain "string"
// Bracketed parts are parsed into "[string]"
vector<string> parseIP(const string &in)
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

bool hasABBA(const string &in, size_t start, size_t end)
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
bool supportsTLS(const string &in)
{
	bool hasValidABBA = false;
	vector<string> parts(parseIP(in));
	for (auto part : parts)
	{
		if (part[0] == '[')
		{
			if (hasABBA(part, 1, part.size()-1))
			{
				return false;
			}
		}
		else
		{
			if (hasABBA(part, 0, part.size()))
			{
				hasValidABBA = true;
			}
		}
	}

	return hasValidABBA;
}

// Part 2
bool supportsSSL(const string &in)
{
	vector<string> parts(parseIP(in));
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
		assert(supportsTLS("abba[mnop]qrst"));
		assert(!supportsTLS("abcd[bddb]xyyx"));
		assert(!supportsTLS("aaaa[qwer]tyui"));
		assert(supportsTLS("ioxxoj[asdfgh]zxcvbn"));

		// part 2
		assert(supportsSSL("aba[bab]xyz"));
		assert(!supportsSSL("xyx[xyx]xyx"));
		assert(supportsSSL("aaa[kek]eke"));
		assert(supportsSSL("zazbz[bzb]cdb"));

		return 0;
	}

	// Take input line-by-line
	vector<string> input;
	for (string temp; getline(cin, temp);)
	{
		input.push_back(temp);
	}

	// Part 1
	int numTLSEnabled = 0;
	for (string s : input)
	{
		if (supportsTLS(s)) numTLSEnabled++;
	}
	cout << "Part 1: " << numTLSEnabled << endl;
	
	// Part 2
	int numSSLEnabled = 0;
	for (string s : input)
	{
		if (supportsSSL(s)) numSSLEnabled++;
	}
	cout << "Part 2: " << numSSLEnabled << endl;
}
