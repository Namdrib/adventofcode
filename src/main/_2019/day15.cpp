#include <bits/stdc++.h>
#include <unistd.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2019/day/15

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
					program[param1_mode == 2 ? param1 + relative_base : param1] = input[input_index];
					input_index++;
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

// dfs
void first_search(intcode_runner &icr, map<pair<int, int>, char> &board, pair<int, int> pos, set<pair<int, int>> &visited)
{
	// north, south, west, east
	int x_dir[4] = {0, 0, -1, 1};
	int y_dir[4] = {-1, 1, 0, 0};

	cout << "dfs at " << pos << endl;

	visited.insert(pos);
	for (size_t i = 0; i < 4; i++)
	{
		pair<int, int> destination = make_pair(pos.first + x_dir[i], pos.second + y_dir[i]);
		cout << "  -> " << destination;

		if (find(all(visited), destination) == visited.end())
		{
			icr.set_input(vector<int> {i + 1});
			int result = icr.process_intcode();
			cout << " = " << result << endl;
			switch (result)
			{
				case 0:
					board[destination] = '#';
					continue;
					break;
				case 1:
					board[destination] = '.';
					// auto temp = visited;
					// temp.insert(pos);
					// neighbours.insert(destination);

					// if (find(all(visited), destination) == visited.end())
					{
						first_search(icr, board, destination, visited);
					}
					break;
				case 2:
					board[destination] = 'O';
					// neighbours.insert(destination);
					cout << "GOT 2 AT " << destination << endl;
					return;
					first_search(icr, board, destination, visited);
					break;
				default:
					break;
			}
		}
		else
		{
			cout << endl;
		}
	}
}

int solve(vector<long long> v, bool part_two)
{
	intcode_runner icr(v);
	map<pair<int, int>, char> board;

	set<pair<int, int>> visited;
	first_search(icr, board, make_pair(0, 0), visited);

	return 0;
}

int main()
{
	string s;
	getline(cin, s);
	vector<long long> v = extract_nums_from<long long>(s);

	cout << "Part 1: " << solve(v, false) << endl;
	// cout << "Part 2: " << solve(v, true) << endl;
}
