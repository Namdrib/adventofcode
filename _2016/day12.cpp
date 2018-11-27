#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2016/day/12

class day12
{
public:
	map<string, int> registers;

	day12()
	{
		;
	}

	// if in is a number, return the numerical representation
	// otherwise return the value at resisters[in]
	int value_of(const string &in)
	{
		try
		{
			return stoi(in);
		}
		catch (const invalid_argument &ia)
		{
			return registers[in];
		}
	}

	void solve(const vector<vector<string>> &input)
	{
		for (size_t i=0; i<input.size(); i++)
		{
			const auto &instruction = input[i];
			const auto &opcode = instruction[0];
			if (opcode == "cpy")
			{
				registers[instruction[2]] = value_of(instruction[1]);
			}
			else if (opcode == "inc")
			{
				registers[instruction[1]]++;
			}
			else if (opcode == "dec")
			{
				registers[instruction[1]]--;
			}
			else if (opcode == "jnz")
			{
				if (value_of(instruction[1]) != 0)
				{
					i += value_of(instruction[2]) - 1; // offset the loop's ++
				}
			}
			else
			{
				cout << "Invalid instruction: " << instruction << endl;
			}
		}
		cout << registers << endl;
	}
};

int main()
{
	vector<vector<string>> tokenised_input;
	for (string line; getline(cin, line);)
	{
		vector<string> out = split_str_by_whitespace<string>(line);
		tokenised_input.push_back(out);
	}

	day12 a;
	a.solve(tokenised_input);

	cout << "Part 1: " << a.registers["a"] << endl;
	a.registers.clear();
	a.registers["c"] = 1;
	a.solve(tokenised_input);
	cout << "Part 2: " << a.registers["a"] << endl;
}
