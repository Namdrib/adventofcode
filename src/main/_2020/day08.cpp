#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2020/day/8

string uncorrupt_instruction(const string &s)
{
	if (s == "nop")
	{
		return "jmp";
	}
	else
	{
		return "nop";
	}
}

vector<pair<string, int>> get_instructions(const vector<string> &in)
{
	vector<pair<string, int>> instructions;
	for (auto s : in)
	{
		// parse the instruction
		// could probably be done better since this might infinite loop
		size_t space_pos = s.find(" ");
		string ins = s.substr(0, space_pos);
		string raw_target = s.substr(space_pos + 1);
		long target = stol(raw_target);

		instructions.push_back(make_pair(ins, target));
	}

	return instructions;
}

size_t run_program(const vector<pair<string, int>> &in, bool &looped)
{
	long acc = 0; // the running register

	size_t pc = 0; // keep track of where the program is up to

	// keep track of which instructions we've visited
	// used to determine whether there has been a loop in the execution
	vector<int> visited_count(in.size(), 0);

	// run the program until either:
	// - looped (part 1 exit condition)
	// - successful program termination (part 2 exit condition)
	while (pc != in.size() && !looped)
	{
		visited_count[pc]++;

		// part 1 exit condition, presence of a loop
		if (visited_count[pc] > 1)
		{
			looped = true;
			break;
		}

		// fetch the instruction to execute
		string ins = in[pc].first;
		int target = in[pc].second;

		// execute the instruction
		// do nothing, execute the next instruction next
		if (ins == "nop")
		{
			pc++;
			continue;
		}
		// increments acc by target
		else if (ins == "acc")
		{
			acc += target;
		}
		// jumps relative current position by target
		else if (ins == "jmp")
		{
			pc += target - 1; // offset from the default increment
		}

		pc++;
	}

	return acc;
}

size_t solve(const vector<string> &in, bool part_two)
{
	vector<pair<string, int>> instructions = get_instructions(in);
	// just run the program
	if (!part_two)
	{
		bool looped = false; // just a placeholder to satify run conditions
		return run_program(instructions, looped);
	}

	// part 2: one-by-one uncorrupt the instructions by swapping a single
	// nop -> jmp or vice versa
	for (size_t i = 0; i < in.size(); i++)
	{
		vector<pair<string, int>> instructions_copy = instructions;

		// only run the program after mutating an instruction
		string current_ins = instructions_copy[i].first;
		if (current_ins == "nop" || current_ins == "jmp")
		{
			instructions_copy[i].first = uncorrupt_instruction(current_ins);

			bool looped = false;
			long result = run_program(instructions_copy, looped);

			// ignore programs that contain loops
			if (!looped)
			{
				return result;
			}
		}
	}

	return 0;
}

int main(int argc, char** argv)
{
	vector<string> input = split_istream_per_line(cin);

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}

