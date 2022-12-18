#include <bits/stdc++.h>
#include <unistd.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2019/day/14

class resource
{
public:
	int amount;
	string name;

	vector<resource> dependencies;

	// resource(const string &name, int amount, const vector<resource> &dependencies)
	resource(const string &name, int amount)
	{
		this->name = name;
		this->amount = amount;
		// this->dependencies = dependencies;
	}

	friend ostream& operator << (ostream &os, resource r)
	{
		os << r.amount << " " << r.name;
		return os;
	}

	bool operator < (const resource &a) const
	{
		return name < a.name;
	}
};

int ore_required_for(map<resource, vector<resource>> requirements, map<string, int> &resource_pool, resource target)
{
	while resource_pool contains anything other than ORE,
		for each item in resource_pool that isn't ORE
			look at the requirements
	for (auto r : requirements[target])
	{

	}
}

int solve(map<resource, vector<resource>> requirements, bool part_two)
{
	int out = 0;

	for (auto i : v)
	{

	}

	return out;
}

int main()
{
	map<resource, vector<resource>> reaction_requirements;
	for (string temp; getline(cin, temp);)
	{
		size_t delim = temp.find(" => ");
		string reagent_string = temp.substr(0, delim);
		string output_string = temp.substr(delim + 4);

		delim = output_string.find(" ");
		resource output(output_string.substr(delim + 1), stoi(output_string.substr(0, delim)));

		cout << "to make " << output << endl;
		vector<resource> reagents;
		vector<string> reagents_string = split_str_by_whitespace<string>(reagent_string);
		for (size_t i = 0; i < reagents_string.size(); i += 2)
		{
			int amount = stoi(reagents_string[i]);
			string name = reagents_string[i + 1];
			if (i + 2 < reagents_string.size())
			{
				name = name.substr(0, name.size() - 1);
			}

			resource input(name, amount);
			cout << "  " << input << endl;
			reagents.push_back(input);
		}

		reaction_requirements[output] = reagents;


		// cout << result << " requries " << reagent_sring << endl;
		// reaction_requirements[resource] = reagents;
	}

	cout << reaction_requirements << endl;

	cout << "Part 1: " << solve(reaction_requirements, false) << endl;
	// cout << "Part 2: " << solve(v, true) << endl;
}


/*

map<pair<int, string>, vector<pair<int, string>>
*/