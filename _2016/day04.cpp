#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2016/day/4

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

bool is_valid(map<char, int> &char_count, const string &checksum)
{
	// Take the highest int in char_count,
	// put the corresponding char into a string	
	multimap<int, char> freq = flip_map(char_count);
	string sorted_freq;
	string partial_freq; // The letters of a single frequency
	for (auto it=freq.rbegin(); it!=freq.rend(); it++)
	{
		partial_freq += it->second;
		// If the frequency is changing
		if (next(it)->first != it->first)
		{
			sort(all(partial_freq));
			sorted_freq += partial_freq;
			partial_freq = "";
		}
	}

	// Valid if sorted_freq starts with checksum
	return (checksum == sorted_freq.substr(0, checksum.size()));
}

void increment(char &c)
{
	if (c == 'z') c = 'a';
	else c++;
}

// Rotate c n times
void caesar_cipher(string s, int n)
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

// Returns the sector_id if the checksum is valid, else 0
int get_id(const string &name)
{
	// Build the character count
	map<char, int> char_count;
	size_t i;
	for (i=0; !isdigit(name[i]); i++)
	{
		if (isalpha(name[i])) char_count[name[i]]++;
	}

	// Get the numbers
	string sector_id_s;
	for (;isdigit(name[i]); i++)
	{
		sector_id_s += name[i];
	}

	// Get the checksum and validate
	int sector_id = atoi(sector_id_s.c_str());
	string checksum = name.substr(i+1, name.length()-i-2);
	return (is_valid(char_count, checksum)) ? sector_id : 0;
}

int main()
{
	int sum_real_id = 0; // Part 1 stuff

	for (string temp; getline(cin, temp);)
	{
		int id = get_id(temp);
		sum_real_id += id;

		// Part 2 stuff: do cipher
		if (id)
		{
			size_t first_digit_pos = temp.find_first_of("0123456789");
			caesar_cipher(temp.substr(0, first_digit_pos-1), id);
		}
	}
	cout << "Part 1: " << sum_real_id << endl;
	cout << "Part 2: grep for \"north\"" << endl;
}
