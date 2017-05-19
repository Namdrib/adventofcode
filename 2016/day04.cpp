#include <algorithm>
#include <cmath>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <utility>
#include <vector>
using namespace std;

// http://adventofcode.com/2016/day/4

// ----- Used to "flip" a map -----
// http://stackoverflow.com/questions/5056645/sorting-stdmap-using-value#5056797
template<typename A, typename B>
pair<B,A> flip_pair(const pair<A,B> &p)
{
	return pair<B,A>(p.second, p.first);
}

template<typename A, typename B>
multimap<B,A> flip_map(const map<A,B> &src)
{
	multimap<B,A> dst;
	transform(src.begin(), src.end(), inserter(dst, dst.begin()),
	          flip_pair<A,B>);
	return dst;
}
// ----- Used to "flip" a map -----


bool isValid(map<char, int> &charCount, const string &checksum)
{
	// Take the highest int in charCount,
	// put the corresponding char into a string	
	multimap<int, char> freq = flip_map(charCount);
	string sortedFreq;
	string partialFreq; // The letters of a single frequency
	for (auto it=freq.rbegin(); it!=freq.rend(); it++)
	{
		partialFreq+=it->second;
		// If the frequency is changing
		if (next(it)->first != it->first)
		{
			sort(partialFreq.begin(), partialFreq.end());
			sortedFreq += partialFreq;
			partialFreq = "";
		}
	}
	
	// Valid if sortedFreq starts with checksum
	return (checksum == sortedFreq.substr(0, checksum.size()));
}

void increment(char &c)
{
	if (c == 'z') c = 'a';
	else c++;
}

// Rotate c n times
void caesarCipher(string s, int n)
{
	for (auto &c : s)
	{
		if (c == '-') c = ' ';
		else
		{
			for (int i=0; i<n%26; i++)
			{
				increment(c);
			}
		}
	}
	cout << s << " | " << n << endl;
}

// Returns the sectorID if the checksum is valid, else 0
int getID(const string &name)
{
	// Build the character count
	map<char, int> charCount;
	size_t i;
	for (i=0; !isdigit(name[i]); i++)
	{
		if (isalpha(name[i])) charCount[name[i]]++;
	}
	
	// Get the numbers
	string sectorID_s;
	for (;isdigit(name[i]); i++)
	{
		sectorID_s += name[i];
	}
	
	// Get the checksum and validate
	int sectorID = atoi(sectorID_s.c_str());
	string checksum = name.substr(i+1, name.length()-i-2);
	return (isValid(charCount, checksum)) ? sectorID : 0;
}

int main()
{
	int sumRealID = 0; // Part 1 stuff
	
	for (string temp; getline(cin, temp);)
	{
		int ID = getID(temp);
		sumRealID += ID;
		
		// Part 2 stuff: do cipher
		if (ID)
		{
			size_t firstDigit = temp.find_first_of("0123456789");
			caesarCipher(temp.substr(0, firstDigit-1), ID);
		}
		
		// NOTE: WHEN RUNNING THE PROGRAM IN TERMINAL, RUN
		// `cat tests/day04_02.in | ./a | grep "north"` -> THIS'LL GET THE NUMBER
	}
	cout << sumRealID << endl;
}