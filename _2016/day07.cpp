#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

// INCOMPLETE

bool hasABBA(string in, size_t start, size_t end)
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

// Split a string into its [bracketed] and non-bracketed parts
// Non-bracketed parts are just the plain "string"
// Bracketed parts are parsed into "[string]"
vector<string> parseIP(string in)
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

bool supportsTLS(string in)
{
	// size_t bracketLeft = in.find("[");
	// size_t bracketRight = in.find("]");
	
	// string left = in.substr(0, bracketLeft);
	// string mid = in.substr(bracketLeft+1, in.size()-bracketRight-1);
	// string right = in.substr(bracketRight+1);
	// cerr << "|" << left << "|" << mid << "|" << right << "|" << endl;
	
	bool hasValidABBA = false;
	vector<string> parts(parseIP(in));
	for (size_t j=0; j<parts.size(); j++)
	{
		if (parts[j][0] == '[')
		{
			if (hasABBA(parts[j], 1, parts[j].size()-1))
			{
				// cerr << "Returning false!" << endl << endl;
				return false;
			}
		}
		else
		{
			if (hasABBA(parts[j], 0, parts[j].size()))
			{
				// cerr << "Found ABBA" << endl;
				hasValidABBA = true;
			}
		}
	}
	
	return hasValidABBA;
}

// Part 2 (INCOMPLETE)
bool supportsSSL(string in)
{
	
	vector<string> parts(parseIP(in));
	sort(parts.begin(), parts.end());
}

int main()
{
	vector<string> input;
	for (string temp; getline(cin, temp);)
	{
		input.push_back(temp);
	}
	
	// Part 1
	int numTLSEnabled = 0;
	for (size_t i=0; i<input.size(); i++)
	{
		if (supportsTLS(input[i])) numTLSEnabled++;
	}
	cout << numTLSEnabled << endl;
	
	// Part 2
	// int numSSLEnabled = 0;
	// for (size_t i=0; i<input.size(); i++)
	// {
		// if (supportsSSL(input[i])) numSSLEnabled++;
	// }
	// cout << numSSLEnabled << endl;
}
