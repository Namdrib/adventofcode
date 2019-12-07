#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2019/day/5

int solve(vector<int> mem, bool part_two = false)
{
	const int puzzle_input = part_two ? 5 : 1;
	int last_output = 0;

	size_t ip = 0; // instruction pointer
	bool keep_running = true;
	while(keep_running && ip < mem.size())
	{
		// assume input is valid - won't write out of bounds
		int op_instruction = mem[ip];
		int opcode = op_instruction % 100;
		bool is_param1_immediate = (op_instruction / 100) & 1;
		bool is_param2_immediate = (op_instruction / 1000) & 1;
		bool is_param3_immediate = (op_instruction / 10000) & 1;

		int param1 = mem[ip + 1];
		int param2 = mem[ip + 2];
		int param3 = mem[ip + 3];

		// early access of mem[paramX] results in segfault
		int value1, value2;

		switch(opcode)
		{
			case 1: // ADD
				value1 = is_param1_immediate ? param1 : mem[param1];
				value2 = is_param2_immediate ? param2 : mem[param2];
				mem[param3] = value1 + value2;

				ip += 4;
				break;

			case 2: // MULTIPLY
				value1 = is_param1_immediate ? param1 : mem[param1];
				value2 = is_param2_immediate ? param2 : mem[param2];
				mem[param3] = value1 * value2;

				ip += 4;
				break;

			case 3: // INPUT
				mem[mem[ip + 1]] = puzzle_input;

				ip += 2;
				break;

			case 4: // OUTPUT
				last_output = mem[param1];
				cout << "  write " << last_output << endl;

				ip += 2;
				break;

			case 5: // JUMP-IF-TRUE
			case 6: // JUMP-IF-FALSE
				value1 = is_param1_immediate ? param1 : mem[param1];
				value2 = is_param2_immediate ? param2 : mem[param2];
				if ( (opcode == 5 ? (value1 != 0) :
				   /* opcode == 6 */ value1 == 0) )
				{
					ip = value2;
					break;
				}

				ip += 3;
				break;

			case 7: // LESS THAN
			case 8: // EQUALS
			{
				value1 = is_param1_immediate ? param1 : mem[param1];
				value2 = is_param2_immediate ? param2 : mem[param2];
				bool result = opcode == 7 ? (value1 < value2) : (value1 == value2);
				mem[param3] = result;

				ip += 4;
				break;
			}

			case 99: // HALT
				cout << "  stopped" << endl;
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
	vector<int> v = extract_nums_from(s);

	cout << "Part 1: " << solve(v, false) << endl;
	cout << "Part 2: " << solve(v, true) << endl;
}
