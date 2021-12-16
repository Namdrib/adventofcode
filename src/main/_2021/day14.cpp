#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2021/day/14

// simulate one round of polymer insertion
// but instead of simulating the action polymer insertion
// keep track of how many of each element pair there is
// that way we can batch the polymer insertion process
// (very similar to the lanternfish problem (day06)
map<string, size_t> perform_polymer_insertion(const map<string, size_t> &current_polymer_pairs, const map<string, string> &pair_insertion_rules)
{
	map<string, size_t> out;

	for (auto p : current_polymer_pairs)
	{
		// e.g. "NN" -> "NC" and "CN"
		string half_1 = p.first.substr(0, 1) + pair_insertion_rules.at(p.first);
		string half_2 = pair_insertion_rules.at(p.first) + p.first.substr(1);

		out[half_1] += p.second;
		out[half_2] += p.second;
	}

	return out;
}

size_t part_one(map<string, size_t> current_polymer_pairs, const map<string, string> &pair_insertion_rules, const size_t num_iterations)
{
	// simulate the polymer insertion for (size_t i = 0; i < num_iterations; i++)
	for (size_t i = 0; i < num_iterations; i++)
	{
		current_polymer_pairs = perform_polymer_insertion(current_polymer_pairs, pair_insertion_rules);
	}

	// count how many of each element there are
	map<char, size_t> element_counts;
	for (const auto &p : current_polymer_pairs)
	{
		element_counts[p.first[0]] += p.second;
		element_counts[p.first[1]] += p.second;
	}

	// divide all by 2 because each element is counted in two pairs
	for (auto &p : element_counts)
	{
		p.second /= 2;
	}

	// quantity of most common element - quantity of least common element
	const auto minmax_frequent_element = minmax_element(all(element_counts), [](const pair<char, size_t> &p, const pair<char, size_t> &q){return p.second < q.second;});

	size_t num_min_element = minmax_frequent_element.first->second;
	size_t num_max_element = minmax_frequent_element.second->second;
	return num_max_element - num_min_element + 1;
}

size_t part_two(map<string, size_t> current_polymer_pairs, const map<string, string> &pair_insertion_rules, const size_t num_iterations)
{
	return part_one(current_polymer_pairs, pair_insertion_rules, num_iterations);
}

int main()
{
	vector<string> input = split_istream_per_line(cin);

	// keep track of the counts of polymer pairs rather than the actual polymer
	string polymer_template = input[0];
	map<string, size_t> current_polymer_pairs;
	for (size_t i = 0; i < polymer_template.size() - 1; i++)
	{
		current_polymer_pairs[polymer_template.substr(i, 2)]++;
	}

	// build up the pair insertion rules
	map<string, string> pair_insertion_rules;
	for (size_t i = 2; i < input.size(); i++)
	{
		size_t dash_pos = input[i].find(" -> ");
		string character_pair = input[i].substr(0, 2);
		string insertion = input[i].substr(dash_pos + 4);

		pair_insertion_rules[character_pair] = insertion;
	}

	cout << "Part 1: " << part_one(current_polymer_pairs, pair_insertion_rules, 10) << endl;
	cout << "Part 2: " << part_two(current_polymer_pairs, pair_insertion_rules, 40) << endl;
}
