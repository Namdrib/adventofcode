#include <bits/stdc++.h>
#include <unistd.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2019/day/19

class intcode_runner
{
public:
	map<size_t, long long> program;
	size_t ip;
	long long relative_base;
	bool keep_running;

	vector<int> input;
	size_t input_index;

	intcode_runner(const vector<long long> &program)
	{
		for (size_t i = 0; i < program.size(); i++)
		{
			this->program[i] = program[i];
		}

		ip = 0;
		relative_base = 0;
		keep_running = true;
	}

	void set_input(const vector<int> &input)
	{
		this->input = input;
		input_index = 0;
	}

	long long process_intcode()
	{
		long long last_output = 0;

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
				{
					int current_input = input[input_index];
					// cerr << "input is " << current_input << endl;
					program[param1_mode == 2 ? param1 + relative_base : param1] = current_input;
					input_index++;
					ip += 2;
					break;
				}

				case 4: // OUTPUT
					last_output = value1;
					ip += 2;
					return last_output;
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
};

// find the value at position (x, y)
int get_value_at(vector<long long> v, int x, int y)
// int get_value_at(intcode_runner icr, int x, int y)
{
	intcode_runner icr(v);
	int out = 0;
	icr.set_input(vector<int>{x, y});
	while (icr.keep_running)
	{
		out = icr.process_intcode();
	}

	cout << "out = " << out << endl;
	return out;
}

int solve(vector<long long> v, bool part_two)
{
	if (part_two)
	{
		// v[0] = 2;
	}

	// const int x_start = 350;
	// const int y_start = 500;
	// const int x_end = 425;
	// const int y_end = 550;
	const int x_start = 0;
	const int y_start = 10;
	const int x_end = 0;
	const int y_end = 10;
	vector<vector<int>> board(y_end - y_start, vector<int>(x_end - x_start, 0));

	int out = 0;
	for (size_t y = y_start; y < y_end; y++)
	{
		for (size_t x = x_start; x < x_end; x++)
		{
			// intcode_runner icr(v);
			int output = get_value_at(v, x, y);
			// icr.set_input(vector<int>{x, y});
			// while (icr.keep_running)
			// {
			// 	int output = icr.process_intcode();
			// 	cout << "get_at(" << x << ", " << y << ") = " << output << endl;
				// if (output > 0)
				{
					board[y - y_start][x - x_start] = output;
					out++;
				}
			// }
		}
	}

	for (auto i : board)
	{
		cout << i << endl;
	}

	return out;
}

int main()
{
	string s;
	getline(cin, s);
	vector<long long> v = extract_nums_from<long long>(s);

	cout << "Part 1: " << solve(v, false) << endl;
	// cout << "Part 2: " << solve(v, true) << endl;
}
