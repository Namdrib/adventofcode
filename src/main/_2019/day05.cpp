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
				value1 = is_param1_immediate ? param1 : mem[param1];
				value2 = is_param2_immediate ? param2 : mem[param2];
				bool result = opcode == 7 ? (value1 < value2) : (value1 == value2);
				mem[param3] = result;

				ip += 4;
				break;

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
	string s = "3,225,1,225,6,6,1100,1,238,225,104,0,1001,152,55,224,1001,224,-68,224,4,224,1002,223,8,223,1001,224,4,224,1,224,223,223,1101,62,41,225,1101,83,71,225,102,59,147,224,101,-944,224,224,4,224,1002,223,8,223,101,3,224,224,1,224,223,223,2,40,139,224,1001,224,-3905,224,4,224,1002,223,8,223,101,7,224,224,1,223,224,223,1101,6,94,224,101,-100,224,224,4,224,1002,223,8,223,101,6,224,224,1,224,223,223,1102,75,30,225,1102,70,44,224,101,-3080,224,224,4,224,1002,223,8,223,1001,224,4,224,1,223,224,223,1101,55,20,225,1102,55,16,225,1102,13,94,225,1102,16,55,225,1102,13,13,225,1,109,143,224,101,-88,224,224,4,224,1002,223,8,223,1001,224,2,224,1,223,224,223,1002,136,57,224,101,-1140,224,224,4,224,1002,223,8,223,101,6,224,224,1,223,224,223,101,76,35,224,1001,224,-138,224,4,224,1002,223,8,223,101,5,224,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1008,677,677,224,1002,223,2,223,1006,224,329,1001,223,1,223,8,677,226,224,102,2,223,223,1006,224,344,101,1,223,223,1107,226,226,224,1002,223,2,223,1006,224,359,1001,223,1,223,1108,677,226,224,102,2,223,223,1005,224,374,1001,223,1,223,1007,226,226,224,102,2,223,223,1006,224,389,1001,223,1,223,108,677,677,224,1002,223,2,223,1005,224,404,1001,223,1,223,1007,677,677,224,102,2,223,223,1005,224,419,1001,223,1,223,8,226,677,224,102,2,223,223,1005,224,434,101,1,223,223,1008,677,226,224,102,2,223,223,1006,224,449,1001,223,1,223,7,677,677,224,102,2,223,223,1006,224,464,1001,223,1,223,8,226,226,224,1002,223,2,223,1005,224,479,1001,223,1,223,7,226,677,224,102,2,223,223,1006,224,494,1001,223,1,223,7,677,226,224,1002,223,2,223,1005,224,509,101,1,223,223,107,677,677,224,102,2,223,223,1006,224,524,101,1,223,223,1007,677,226,224,102,2,223,223,1006,224,539,101,1,223,223,107,226,226,224,1002,223,2,223,1006,224,554,101,1,223,223,1008,226,226,224,102,2,223,223,1006,224,569,1001,223,1,223,1107,677,226,224,1002,223,2,223,1005,224,584,101,1,223,223,1107,226,677,224,102,2,223,223,1005,224,599,101,1,223,223,1108,226,677,224,102,2,223,223,1005,224,614,101,1,223,223,108,677,226,224,102,2,223,223,1005,224,629,101,1,223,223,107,226,677,224,102,2,223,223,1006,224,644,1001,223,1,223,1108,226,226,224,1002,223,2,223,1006,224,659,101,1,223,223,108,226,226,224,102,2,223,223,1005,224,674,101,1,223,223,4,223,99,226";

	vector<int> v = extract_nums_from(s);

	cout << "Part 1: " << solve(v, false) << endl;
	cout << "Part 2: " << solve(v, true) << endl;
}
