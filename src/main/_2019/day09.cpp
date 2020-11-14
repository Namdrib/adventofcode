#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2019/day/9

long long solve(map<size_t, long long> program, bool part_two = false)
{
	const long long puzzle_input = part_two ? 2 : 1;
	long long last_output = 0;

	size_t ip = 0; // instruction pointer
	bool keep_running = true;
	long long relative_base = 0;
	while (keep_running)
	{
		// assume input is valid - won't write out of bounds
		int op_instruction = program[ip];
		int opcode = op_instruction % 100;

		// modes: 0: position, 1: immediate, 2: relative
		int param1_mode = (op_instruction / 100) % 10;
		int param2_mode = (op_instruction / 1000) % 10;
		int param3_mode = (op_instruction / 10000) % 10;

		long long param1 = program[ip + 1];
		long long param2 = program[ip + 2];
		long long param3 = program[ip + 3];

		long long value1 = param1_mode == 1 ? param1 :
		                   param1_mode == 2 ? program[param1 + relative_base] :
		                   program[param1];
		long long value2 = param2_mode == 1 ? param2 :
		                   param2_mode == 2 ? program[param2 + relative_base] :
		                   program[param2];
		long long value3 = param3_mode == 2 ? param3 + relative_base : param3;

		switch (opcode)
		{
			case 1: // ADD
				program[value3] = value1 + value2;
				ip += 4;
				break;

			case 2: // MULTIPLY
				program[value3] = value1 * value2;
				ip += 4;
				break;

			case 3: // INPUT
				program[param1_mode == 2 ? param1 + relative_base : param1] = puzzle_input;
				ip += 2;
				break;

			case 4: // OUTPUT
				last_output = value1;
				ip += 2;
				break;

			case 5: // JUMP-IF-TRUE
				ip = (value1 != 0) ? value2 : ip + 3;
				break;

			case 6: // JUMP-IF-FALSE
				ip = (value1 == 0) ? value2 : ip + 3;
				break;

			case 7: // LESS THAN
			case 8: // EQUALS
				program[value3] = (opcode == 7) ? (value1 < value2) : (value1 == value2);
				ip += 4;
				break;

			case 9: // RELATIVE BASE
				relative_base += value1;
				ip += 2;
				break;

			case 99: // HALT
				keep_running = false;
				break;

			default:
				cout << "  something went wrong, opcode=" << opcode << endl;
				keep_running = false;
				break;
		}
	}

	return last_output;
}

int main()
{
	string s;
	getline(cin, s);
	vector<long long> v = extract_nums_from<long long>(s);

	map<size_t, long long> m;
	for (size_t i = 0; i < v.size(); i++)
	{
		m[i] = v[i];
	}

	cout << "Part 1: " << solve(m, false) << endl;
	cout << "Part 2: " << solve(m, true) << endl;
}
