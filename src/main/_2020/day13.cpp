#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2020/day/13

// calculate the minimum time for a given set of buses
// taking into account starting time and how much to iterate by when
// looking for subsequent iems
size_t min_time_for_buses(const vector<int> &bus_ids,
		const map<int, int> &bus_id_idx, size_t bus_limit, size_t starting_time,
		size_t iteration_factor)
{
	// start at starting_time, and add multiples of iteration_factor
	// until all buses from 0 to bus_limit satisfy the criteria
	size_t current_time;
	for (current_time = starting_time; ; current_time += iteration_factor)
	{
		bool good = true;

		// for every valid bus
		// check to see if they ALL factor into current_time (plus offset)
		// ie the 0th bus leaves at time current_time, 1st bus leaves at current_time + 1, ...
		for (size_t i = 0; i <= bus_limit; i++)
		{
			if (bus_ids.at(i) != -1)
			{
				size_t value_with_offset = (current_time + bus_id_idx.at(bus_ids.at(i)));
				if (value_with_offset % bus_ids.at(i) != 0)
				{
					good = false;
					break;
				}
			}
		}

		if (good)
		{
			break;
		}
	}
	return current_time;
}

// find the first time for which all busses depart one after another
size_t solve_part_two(vector<int> bus_ids)
{
	// store the original idices of the bus_ids
	map<int, int> bus_id_idx;
	for (size_t i = 0; i < bus_ids.size(); i++)
	{
		if (bus_ids[i] != -1)
		{
			bus_id_idx[bus_ids[i]] = i;
		}
	}

	size_t running_product = 1;
	size_t cum_time = 0;

	// for each valid cumulative bus
	// determine the time required for all buses to loop back to the station
	for (size_t i = 1; i < bus_ids.size(); i++)
	{
		if (bus_ids[i] != -1)
		{
			// get the first time all buses up to i get back to station
			cum_time = min_time_for_buses(bus_ids, bus_id_idx, i, cum_time, running_product);

			// the next iteration amount requried for the cumulative buses to loop back to station
			running_product *= bus_ids[i];
		}
	}

	return cum_time;
}

// figure out how long we need to wait until we can depart
size_t solve(const vector<int> &in, int timestamp, bool part_two)
{
	if (part_two)
	{
		return solve_part_two(in);
	}
	map<int, long> first_departure_after_timestamp;

	// find out how when each bus first departs after timestamp
	for (auto i : in)
	{
		if (i != -1)
		{
			long min_iterations = ceil(timestamp / static_cast<double>(i));
			long time_till_departure = i * min_iterations;
			first_departure_after_timestamp[i] = time_till_departure;
		}
	}

	// find the first bus that departs after that time
	auto q = *min_element(all(first_departure_after_timestamp),
			[](const pair<int, long> &a, const pair<int, long> &b){
			return a.second < b.second;
			});

	return q.first * (q.second - timestamp);
}

int main(int argc, char** argv)
{
	vector<string> raw_input = split_istream_per_line(cin);
	int timestamp = stoi(raw_input[0]);
	vector<string> bus_id_strings = split_string_by(raw_input[1], ",");
	vector<int> input;
	for (auto s : bus_id_strings)
	{
		if (s == "x")
		{
			input.push_back(-1);
		}
		else
		{
			input.push_back(stoi(s));
		}
	}

	cout << "Part 1: " << solve(input, timestamp, false) << endl;
	cout << "Part 2: " << solve(input, timestamp, true) << endl;
}

