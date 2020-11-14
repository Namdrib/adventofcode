#include <bits/stdc++.h>
#include <unistd.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2019/day/17

class intcode_runner
{
public:
	map<size_t, long long> program;
	size_t ip;
	long long relative_base;
	bool keep_running;

	vector<string> input;
	int input_i, input_j;

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

	void set_input(const vector<string> &input)
	{
		this->input = input;
		input_i = input_j = 0;
	}

	long long process_intcode(long long a)
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

			char c = '0';
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
					if (input_j == input[input_i].size())
					{
						c = '\n';
						input_j = 0;
						input_i++;
					}
					else
					{
						c = input[input_i][input_j];
						input_j++;
					}

					program[param1_mode == 2 ? param1 + relative_base : param1] = (int)c;
					ip += 2;
					break;

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

int solve(vector<long long> v, bool part_two)
{
	if (part_two)
	{
		v[0] = 2;
	}
	int out = 0;

	intcode_runner icr(v);

	if (part_two)
	{
		vector<string> input_sequence = {
			"A,B,A,B,C,C,B,A,B,C",
			"L,8,R,12,R,12,R,10",
			"R,10,R,12,R,10",
			"L,10,R,10,L,6",
			"n"
		};
		icr.set_input(input_sequence);

		while (icr.keep_running)
		{
			int temp = icr.process_intcode(0);
			if (temp > 0)
			{
				out = temp;
			}
		}
	}
	else
	{
		vector<vector<char>> board;
		vector<char> temp;
		while (icr.keep_running)
		{
			char c = char(icr.process_intcode(0));
			if (c == '\n')
			{
				board.push_back(temp);
				temp.clear();
			}
			else
			{
				temp.push_back(c);
			}
		}

		int sum = 0;
		for (size_t i = 1; i < board.size() - 1; i++)
		{
			for (size_t j = 1; j < board[i].size() - 1; j++)
			{
				if ((board[i][j] == '#') &&
					(board[i][j-1] == '#') && (board[i][j+1] == '#') &&
					(board[i-1][j] == '#') && (board[i+1][j] == '#'))
				{
					sum += (i * j);
				}
			}
		}
		out = sum;
	}

	return out;
}

int main()
{
	string s;
	getline(cin, s);
	vector<long long> v = extract_nums_from<long long>(s);

	cout << "Part 1: " << solve(v, false) << endl;
	cout << "Part 2: " << solve(v, true) << endl;
}

// my sequence
// L8, R12, R12, R10
// R10, R12, R10
// L8, R12, R12, R10
// R10, R12, R10
// L10, R10, L6
// L10, R10, L6
// R10, R12, R10
// L8, R12, R12, R10
// R10, R12, R10
// L10, R10, L6
