#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2020/day/7

// store a certain bag's colour and child bags (if any)
class bag
{
public:
	string colour;

	map<string, int> child_bags;

	bool is_empty()
	{
		return child_bags.empty();
	}
};

ostream& operator <<(ostream &os, const bag &b)
{
	os << "[" << b.colour << ": " << b.child_bags << "]";
	return os;
}

// read and store the bags input into a map<string, bag>
map<string, bag> parse_all_bags(vector<string> in)
{
	map<string, bag> bags;

	for (string s : in)
	{
		bag b;

		size_t second_space_pos = s.find(" ", s.find(" ") + 1);

		string colour = s.substr(0, second_space_pos);
		b.colour = colour;

		size_t contain_pos = s.find("contain ") + 8;
		string contains = s.substr(contain_pos);

		// there are child elements
		if (!(contains[0] == 'n'))
		{
			size_t pos = 0;
			string child_bag_desc;
			while ((pos = contains.find(", ")) != string::npos)
			{
				child_bag_desc = contains.substr(0, pos);
				contains.erase(0, pos + 2);

				size_t child_space_pos = child_bag_desc.find(" ");
				int num_child_bags = stoi(child_bag_desc.substr(0, child_space_pos));
				string child_bag_colour = child_bag_desc.substr(child_space_pos + 1, child_bag_desc.find("bag", child_space_pos) - 3);

				// for each bags it contains, populate child_bags
				b.child_bags[child_bag_colour] = num_child_bags;
			}
			pos = contains.find(".");
			child_bag_desc = contains.substr(0, pos);

			size_t child_space_pos = child_bag_desc.find(" ");
			int num_child_bags = stoi(child_bag_desc.substr(0, child_space_pos));
			string child_bag_colour = child_bag_desc.substr(child_space_pos + 1, child_bag_desc.find("bag", child_space_pos) - 3);

			b.child_bags[child_bag_colour] = num_child_bags;
		}

		bags[colour] = b;
	}

	return bags;
}

// returns true if `colour` bag contains `target` bag directly or indirectly
// this is a depth-first search
bool contains_target(map<string, bag> all_bags, map<string, bool> &discovered, string colour, string target)
{
	if (colour == target)
	{
		return true;
	}

	discovered[colour] = true;

	bool found_target = false;
	// for each child bag of this colour
	for (auto p : all_bags[colour].child_bags)
	{
		if (found_target)
		{
			break;
		}

		// if not discovered, recursively head down
		if (discovered.count(p.first) <= 0)
		{
			found_target += contains_target(all_bags, discovered, p.first, target);
		}
	}

	return found_target;
}

// memoise the worth of all the bags
map<string, int> bag_worth;

// counts how many bags are inside current_bag (including itself)
// use bag_worth to store pre-calculated results
long long count_bags(map<string, bag> all_bags, string current_bag)
{
	// already cached
	if (bag_worth.count(current_bag) > 0)
	{
		return bag_worth[current_bag];
	}

	// bag with no child bags is worth just itself
	if (all_bags[current_bag].is_empty())
	{
		bag_worth[current_bag] = 1;
		return bag_worth[current_bag];
	}

	// calculate the total worth of all child bags
	// counts the child (and their contents) as many times as specified
	// by the parent bag
	long long sum = 1; // including itself
	for (auto bag : all_bags[current_bag].child_bags)
	{
		long long bag_worth = count_bags(all_bags, bag.first);
		sum += bag_worth * bag.second;
	}

	// store and return the value of this bag
	bag_worth[current_bag] = sum;
	return bag_worth[current_bag];
}

int solve(const map<string, bag> &bags, bool part_two)
{
	int count = 0;

	string shiny_gold = "shiny gold";

	// return the total number of bags contained in the gold bag
	if (part_two)
	{
		// count_bags returns how much a bag is worth including itself
		// don't count the gold bag since we're interested in how many are IN it
		count = count_bags(bags, shiny_gold) - 1;
	}
	// return the number of types of bags that contain a shiny gold bag
	else // part one
	{
		for (auto b : bags)
		{
			if (b.first == shiny_gold)
			{
				continue;
			}
			map<string, bool> discovered;

			bool has_gold = contains_target(bags, discovered, b.first, shiny_gold);
			count += has_gold;
		}
	}

	return count;
}

int main()
{
	vector<string> input = split_istream_per_line(cin);
	map<string, bag> bags = parse_all_bags(input);

	cout << "Part 1: " << solve(bags, false) << endl;
	cout << "Part 2: " << solve(bags, true) << endl;
}

