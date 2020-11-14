#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2019/day/11

// 0 = up, 1 = right, 2 = down, 3 = left
int d_x[4] = {0, 1, 0, -1};
int d_y[4] = {-1, 0, 1, 0};

class robot
{
public:
	// keep track of robot's internal memory
	map<size_t, long long> program;
	size_t ip;
	long long relative_base;
	bool keep_running;

	int x, y;
	int dir;
	int min_x, max_x, min_y, max_y;

	vector<int> input;
	int input_index;

	robot(map<size_t, long long> program, size_t ip = 0)
	{
		// program-related
		this->program = program;
		this->ip = ip;
		relative_base = 0;
		keep_running = true;

		// robot-related
		x = y = dir = 0;
		min_x = max_x = min_y = max_y = 0;
	}

	void set_input(const vector<int> &input)
	{
		this->input = input;
		input_index = 0;
	}

	vector<int> process_intcode()
	{
		vector<int> output;

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
					program[param1_mode == 2 ? param1 + relative_base : param1] = input.at(input_index);
					input_index++;
					ip += 2;
					break;

				case 4: // OUTPUT
					output.push_back(value1);
					ip += 2;
					if (output.size() >= 2)
					{
						return output;
					}
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
					cerr << "  something went wrong, opcode=" << opcode << ", " << param1 << ", " << param2 << ", " << param3 << endl;
					keep_running = false;
					break;
			}
		}

		return vector<int>{-1, -1};
	}

	void pretty_print_grid(const map<pair<int, int>, bool> &grid) const
	{
		vector<vector<int>> output(max_y - min_y + 1, vector<int>(max_x - min_x + 1, 0));
		for (auto p : grid)
		{
			int y = p.first.second - min_y;
			int x = p.first.first - min_x;
			output.at(y)[x] = p.second;
		}

		// pretty print
		const char direction[4] = {'^', '>', 'v', '<'};
		for (int i = 0; i < (int)output.size(); i++)
		{
			for (int j = 0; j < (int)output[i].size(); j++)
			{
				if (i == y - min_y && j == x - min_x)
				{
					cout << direction[dir];
				}
				else
				{
					cout << (output[i][j] != 0 ? "1" : " ");
				}
			}
			cout << endl;
		}
	}
};

int solve(map<size_t, long long> m, bool part_two = false)
{
	int out = 0;
	map<pair<int, int>, bool> grid;

	robot r(m, 0);

	if (part_two)
	{
		grid[make_pair(r.x, r.y)] = 1;
	}

	while (r.keep_running)
	{
		pair<int, int> pos = make_pair(r.x, r.y);
		if (grid.find(pos) == grid.end())
		{
			grid[pos] = 0;
		}

		// paint the grid
		r.set_input(vector<int> {grid[pos]});
		vector<int> out = r.process_intcode();
		if (any_of(all(out), [](int a){return a == -1;}))
		{
			break;
		}

		grid[pos] = out[0];

		// change direction and move forward
		r.dir += (out[1]) ? 1 : -1;
		r.dir = (r.dir + 4) % 4;
		r.x += d_x[r.dir];
		r.y += d_y[r.dir];

		r.min_x = min(r.min_x, r.x);
		r.max_x = max(r.max_x, r.x);
		r.min_y = min(r.min_y, r.y);
		r.max_y = max(r.max_y, r.y);
	}

	if (part_two)
	{
		r.pretty_print_grid(grid);
	}

	out = grid.size();
	return out;
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

	cout << "Part 1: " << solve(m, false) << endl; // 2392
	cout << "Part 2:\n" << solve(m, true) << endl;
}
