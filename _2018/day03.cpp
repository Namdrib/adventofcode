#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/3

class claim
{
public:
	int id;
	int x, y; // position
	int w, h; // size

	claim()
	{
		id = x = y = w = h = 0;
	}

	claim(int id, int x, int y, int w, int h)
	{
		this->id = id;
		this->x = x;
		this->y = y;
		this->w = w;
		this->h = h;
	}

	// returns true iff the rectangle described by this intersects with the
	// rectangle decribed by rhs
	// if a.intersects(b), then b.intersects(a)
	const bool intersects(const claim &rhs) const
	{
		return !(x + w < rhs.x || rhs.x + rhs.w < x
			|| y + h < rhs.y || rhs.y + rhs.h < y);
	}
};

// turn a vector of strings in the format "#id @ x,y: wxh"
// into a vector of claims with id, x, y, w and h
vector<claim> readClaims(const vector<string> &v)
{
	vector<claim> out;
	for (auto s : v)
	{
		vector<string> tokens;
		stringstream ss(s);
		for (string token; getline(ss, token, ' ');)
		{
			tokens.push_back(token);
		}

		int id = stoi(tokens[0].substr(1));

		size_t pos_comma = tokens[2].find_first_of(',');
		int x = stoi(tokens[2].substr(0, pos_comma));
		int y = stoi(tokens[2].substr(pos_comma+1, tokens[2].size()-pos_comma-2));

		size_t pos_x = tokens[3].find_first_of('x');
		int w = stoi(tokens[3].substr(0, pos_x));
		int h = stoi(tokens[3].substr(pos_x+1));

		out.push_back(claim(id, x, y, w, h));
	}
	return out;
}

int solve(vector<claim> claims, bool partTwo = false)
{
	// the frequency at which the pair<x, y> is covered by a claim
	map<pair<int, int>, int> freq;

	for (size_t k = 0; k < claims.size(); k++)
	{
		auto p = claims[k];
		if (partTwo)
		{
			// if (none_of(all(claims), [it, p](claim c){return (*it != c) && p.intersects(c);}))
			// {
			// 	return p.id;
			// }
			// part 2: return the claim with no overlaps
			bool overlap = false;
			for (size_t l = 0; l < claims.size(); l++)
			{
				if (k == l) continue;
				if (p.intersects(claims[l]))
				{
					overlap = true;
					break;
				}
			}
			if (!overlap)
			{
				return p.id;
			}
		}
		else
		{
			// part 1: increase the frequency with which pair<i, j> has been seen
			for (int i = p.y; i < p.y + p.h; i++)
			{
				for (int j = p.x; j < p.x + p.w; j++)
				{
					freq[make_pair(i, j)]++;
				}
			}
		}
	}

	// the number of <x, y> that have been covered at least twice
	return accumulate(all(freq), 0, [](int acc, pair<pair<int, int>, int> entry){
		return acc + (entry.second >= 2);
	});
}

int main()
{
	vector<string> claimStrings;
	for (string temp; getline(cin, temp);)
	{
		claimStrings.push_back(temp);
	}

	vector<claim> claims = readClaims(claimStrings);
	cout << "Part 1: " << solve(claims, false) << endl;
	cout << "Part 2: " << solve(claims, true) << endl;
}
