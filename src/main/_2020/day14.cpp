#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2020/day/14

// generate every possible string from a given mask
// every X splits into a version of the string with a 0 and a 1 in that pos
// e.g. 100X0 -> 10000 and 10010
void generate_masks_from(vector<string> &out, string mask, size_t i)
{
	for (; i < mask.size(); i++)
	{
		if (mask[i] == 'X') // generate a 0 and 1 mask from this position
		{
			mask[i] = '0';
			generate_masks_from(out, mask, i + 1);
			mask[i] = '1';
			generate_masks_from(out, mask, i + 1);
			break;
		}
	}
	if (i == mask.size())
	{
		out.push_back(mask);
		return;
	}
}

// apply mask s to n, where s consists of 'X', '1' and '0'
// s[0] is most significant bit, s[s.size() - 1] is least significant bit
// 1 denotes we should set that bit in n, and 0 to clear
size_t apply_mask(const string &s, size_t n)
{
	size_t len = s.size();
	for (size_t i = 0; i < len; i++)
	{
		size_t pos = len - i - 1;
		size_t one = 1;
		if (s[i] == '1') // set bit
		{
			n |= (one << pos);
		}
		else if (s[i] == '0') // clear bit
		{
			n &= ~(one << pos);
		}
	}
	return n;
}

// apply a mask (orig_mask) to n
// use the original mask unless there was an 'X'
// in that case, use the floating mask
// this method should be called multiple times with every possible floating mask
size_t apply_mask_floating(const string &orig_mask, const string &floating_mask, size_t n)
{
	size_t len = orig_mask.size();
	for (size_t i = 0; i < len; i++)
	{
		size_t pos = len - i - 1;
		size_t one = 1;
		if (orig_mask[i] == '0')
		{
			continue;
		}
		else if (orig_mask[i] == '1')
		{
			n |= (one << pos);
		}
		else if (orig_mask[i] == 'X')
		{
			if (floating_mask[i] == '1')
			{
				n |= (one << pos);
			}
			else if (floating_mask[i] == '0') // clear bit
			{
				n &= ~(one << pos);
			}
		}
	}
	return n;
}

size_t solve(const vector<string> &in, bool part_two)
{
	map<size_t, size_t> mem;
	string mask;

	for (auto s : in)
	{
		if (s[1] == 'a')
		{
			// update the mask
			mask = s.substr(7);
		}
		else
		{
			// read the destination and value to write
			vector<size_t> nums = extract_nums_from<size_t>(s);

			// apply the mask to the value (if applicable)
			size_t value = nums[1];
			if (!part_two)
			{
				value = apply_mask(mask, value);
			}

			// write value to address(es)
			vector<size_t> addresses;
			if (part_two)
			{
				vector<string> floating_masks;
				generate_masks_from(floating_masks, mask, 0);
				for (auto floating_mask : floating_masks)
				{
					size_t address = apply_mask_floating(mask, floating_mask, nums[0]);
					addresses.push_back(address);
				}
			}
			else
			{
				addresses.push_back(nums[0]);
			}

			for (auto address : addresses)
			{
				mem[address] = value;
			}
		}
	}

	return accumulate(all(mem), 0ull,
			[](size_t acc, const pair<size_t, size_t> &p){
			return acc + p.second;
			});
}

int main(int argc, char** argv)
{
	vector<string> input = split_istream_per_line(cin);

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}

