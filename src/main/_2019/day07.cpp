#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2019/day/7

class amplifier
{
public:
	vector<int> program;
	int ip;
	queue<int> inputs;

	amplifier(vector<int> program)
	{
		this->program = program;
		ip = 0;
	}
};

int run_program(vector<int> program, vector<amplifier> amplifiers)
{
	int last_output = 0;

	size_t current_amp = 0;
	size_t ip = 0; // instruction pointer
	bool keep_running = true;
	while (keep_running && ip < program.size())
	{
		int op_instruction = program[ip];
		int opcode = op_instruction % 100;
		bool is_param1_immediate = (op_instruction / 100) & 1;
		bool is_param2_immediate = (op_instruction / 1000) & 1;
		bool is_param3_immediate = (op_instruction / 10000) & 1;

		int param1 = program[ip + 1];
		int param2 = program[ip + 2];
		int param3 = program[ip + 3];

		int value1 = is_param1_immediate ? param1 : (param1 < (int) program.size()) ? program[param1] : 0;
		int value2 = is_param2_immediate ? param2 : (param2 < (int) program.size()) ? program[param2] : 0;

		switch (opcode)
		{
			case 1: // ADD
				program[param3] = value1 + value2;
				ip += 4;
				break;

			case 2: // MULTIPLY
				program[param3] = value1 * value2;
				ip += 4;
				break;

			case 3: // INPUT
				program[param1] = amplifiers[current_amp].inputs.front();
				amplifiers[current_amp].inputs.pop();
				ip += 2;
				break;

			case 4: // OUTPUT
				last_output = program[param1];
				ip += 2;

				// rotate amplifiers
				// 1. save the current amp so it picks up at the next instruction
				amplifiers[current_amp].program = program;
				amplifiers[current_amp].ip = ip;

				// 2. move to and start using the next one
				current_amp = (current_amp + 1) % amplifiers.size();
				program = amplifiers[current_amp].program;
				ip = amplifiers[current_amp].ip;

				// 3. pass the output of the previous amp to the new one
				amplifiers[current_amp].inputs.push(last_output);
				break;

			case 5: // JUMP-IF-TRUE
				ip = (value1 != 0) ? value2 : ip + 3;
				break;

			case 6: // JUMP-IF-FALSE
				ip = (value1 == 0) ? value2 : ip + 3;
				break;

			case 7: // LESS THAN
			case 8: // EQUALS
				program[param3] = (opcode == 7) ? (value1 < value2) : (value1 == value2);
				ip += 4;
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

int solve(vector<int> program, bool part_two)
{
	vector<int> phase_sequence;
	if (part_two)
	{
		phase_sequence = vector<int>{5, 6, 7, 8, 9};
	}
	else
	{
		phase_sequence = vector<int>{0, 1, 2, 3, 4};
	}

	int max_signal = 0;
	vector<int> best_sequence = phase_sequence;
	do
	{
		queue<int> input;
		int signal_strength = 0;

		// initialise amplifiers
		vector<amplifier> amplifiers(5, program);
		for (size_t i = 0; i < phase_sequence.size(); i++)
		{
			amplifiers[i].inputs.push(phase_sequence[i]);
		}
		amplifiers[0].inputs.push(signal_strength);

		// run the programs with all the amplifiers
		// program exit signals the end of the whole chain
		signal_strength = run_program(program, amplifiers);

		if (signal_strength > max_signal)
		{
			max_signal = signal_strength;
			best_sequence = phase_sequence;
		}

	} while (next_permutation(all(phase_sequence)));

	return max_signal;
}

int main()
{
	string s;
	getline(cin, s);
	vector<int> v = extract_nums_from(s);

	// cout << "Part 1: " << solve(v, false) << endl;
	cout << "Part 2: " << solve(v, true) << endl;
}
