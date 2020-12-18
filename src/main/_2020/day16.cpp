#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2020/day/16

typedef vector<int> ticket;

class ticket_validator
{
	public:
		string name;
		vector<pair<int, int>> ranges;

		// return true if n fits somewhere in one of the ranges
		bool valid_num(int n) const
		{
			return any_of(all(ranges), [n](const pair<int, int> &range){
					return n >= range.first && n <= range.second;
					});
		}
};

ostream& operator << (ostream& os, const ticket_validator &tv)
{
	os << tv.name << ": ";
	for (auto p : tv.ranges)
	{
		os << p << ", ";
	}
	return os;
}

// read the input into validators, my ticket and nearby tickets
void parse_input(const vector<string> &in,
		vector<ticket_validator> &ticket_validators,
		ticket &my_ticket,
		vector<ticket> &nearby_tickets)
{
	// what type of thing we're looking at
	// could be any of the ticket fields, "your ticket" or "nearby tickets"
	size_t batch = 0;
	regex validator_regex("(.*): (\\d+)-(\\d+) or (\\d+)-(\\d+)");

	// parse in into sections (validators, my ticket, nearby tickets)
	for (size_t i = 0; i < in.size(); i++)
	{
		if (in[i] == "")
		{
			batch++;
			continue;
		}

		// fuck parsing in c++
		switch (batch)
		{
			case 0: // read validators
				{
					smatch sm;
					regex_match(in[i], sm, validator_regex);

					ticket_validator tv;
					vector<int> tv_range_nums;
					// i == 0 is the WHOLE match
					for (size_t i = 1; i < sm.size(); i++)
					{
						ssub_match sub_match = sm[i];
						string sms = sub_match.str();
						if (i == 1)
						{
							tv.name = sms;
						}
						else
						{
							tv_range_nums.push_back(stoll(sms));
						}
					}

					tv.ranges.push_back(make_pair(tv_range_nums[0], tv_range_nums[1]));
					tv.ranges.push_back(make_pair(tv_range_nums[2], tv_range_nums[3]));
					ticket_validators.push_back(tv);
					break;
				}

			case 1: // parse your ticket
				i++;
				my_ticket = extract_nums_from<int>(in[i]);
				break;

			case 2: // parse nearby tichets;
				i++;
				while (i < in.size())
				{
					nearby_tickets.push_back(extract_nums_from<int>(in[i]));
					i++;
				}
		}
	}
}

// used for part one
// return true iff any of t's fields have NO matches in any tv ranges
size_t is_ticket_possibly_valid(const ticket &t,
		const vector<ticket_validator> &tvs)
{
	size_t ticket_error_rate = 0;
	for (auto i : t)
	{
		// if this returns true, the ticket value is NOT valid
		// ie it is not a valid num for any tv in tvs
		if (!any_of(all(tvs), [i](const ticket_validator &tv){
					return tv.valid_num(i);
					}))
		{
			ticket_error_rate += i;
		}
	}

	return ticket_error_rate;
}

// work out which positions correspond to which ticket fields
map<string, size_t> map_field_to_ticket_index(
		const vector<ticket_validator> &ticket_validators,
		const vector<ticket> &valid_nearby_tickets)
{
	// which vector index is associated with a field name
	map<string, size_t> field_pos;

	// a nicer way of keeping track of all field_pos.second
	set<size_t> occupied_positions;

	// since some fields can appear in more than one index
	// do until all fields mapped:
	// for each field, find out how many positions it can fit in
	// find the field(s) which only fit in ONE position
	// - solidify those fields
	// - remove those positions from the search space
	size_t num_fields = valid_nearby_tickets[0].size();
	while (field_pos.size() < num_fields)
	{
		map<string, vector<size_t>> potential_field_positions;

		// find all of the potential field positions that haven't been done
		for (const auto &tv : ticket_validators)
		{
			if (field_pos.count(tv.name) != 0)
			{
				continue;
			}

			// search all indices that haven't been done
			for (size_t i = 0; i < num_fields; i++)
			{
				if (occupied_positions.count(i))
				{
					continue;
				}

				// found a potential match!
				if (all_of(all(valid_nearby_tickets), [i, tv](const ticket &nt){
							return tv.valid_num(nt[i]);
							}))
				{
					potential_field_positions[tv.name].push_back(i);
				}
			}
		}

		// isolate the ones where there is only one possibility
		for (const auto &p : potential_field_positions)
		{
			if (p.second.size() == 1)
			{
				occupied_positions.insert(p.second[0]);
				field_pos[p.first] = p.second[0];
			}
		}
	}

	return field_pos;
}

size_t solve(const vector<string> &in, bool part_two)
{
	// parse the input into usable format
	vector<ticket_validator> ticket_validators;
	ticket my_ticket;
	vector<ticket> nearby_tickets;

	parse_input(in, ticket_validators, my_ticket, nearby_tickets);

	// used in part two
	vector<ticket> valid_nearby_tickets;

	// work out which tickets have invalid values - prune them out
	// this then becomes the input for part two
	size_t ticket_scanning_error_rate = 0;
	for (auto nearby_ticket : nearby_tickets)
	{
		size_t rate = is_ticket_possibly_valid(nearby_ticket, ticket_validators);
		if (rate != 0)
		{
			ticket_scanning_error_rate += rate;
		}
		else
		{
			valid_nearby_tickets.push_back(nearby_ticket);
		}
	}

	if (!part_two)
	{
		return ticket_scanning_error_rate;
	}

	// part two
	map<string, size_t> field_pos = map_field_to_ticket_index(
			ticket_validators, valid_nearby_tickets);

	// calculate the product of all "departure" fields on my ticket
	size_t departure_value_product = 1;
	for (const auto &p : field_pos)
	{
		if (p.first.find("departure") != string::npos)
		{
			departure_value_product *= my_ticket[p.second];
		}
	}

	return departure_value_product;
}

int main(int argc, char** argv)
{
	vector<string> input = split_istream_per_line(cin);

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}
