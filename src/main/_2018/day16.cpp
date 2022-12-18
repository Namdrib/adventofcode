#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/16

const vector<string> instructions = {
	"addr", "addi",
	"mulr", "muli",
	"banr", "bani",
	"borr", "bori",
	"setr", "seti",
	"gtir", "gtri", "gtrr",
	"eqir", "eqri", "eqrr",
};

void execute(vector<int> &registers, string opcode, int a, int b, int c) {
	if (opcode == "addr") {
		registers[c] = registers[a] + registers[b];
	}
	else if (opcode == "addi") {
		registers[c] = registers[a] + b;
	}
	else if (opcode == "mulr") {
		registers[c] = registers[a] * registers[b];
	}
	else if (opcode == "muli") {
		registers[c] = registers[a] * b;
	}
	else if (opcode == "banr") {
		registers[c] = registers[a] & registers[b];
	}
	else if (opcode == "bani") {
		registers[c] = registers[a] & b;
	}
	else if (opcode == "borr") {
		registers[c] = registers[a] | registers[b];
	}
	else if (opcode == "bori") {
		registers[c] = registers[a] | b;
	}
	else if (opcode == "setr") {
		registers[c] = registers[a];
	}
	else if (opcode == "seti") {
		registers[c] = a;
	}
	else if (opcode == "gtir") {
		registers[c] = (a > registers[b]) ? 1 : 0;
	}
	else if (opcode == "gtri") {
		registers[c] = (registers[a] > b) ? 1 : 0;
	}
	else if (opcode == "gtrr") {
		registers[c] = (registers[a] > registers[b]) ? 1 : 0;
	}
	else if (opcode == "eqir") {
		registers[c] = (a == registers[b]) ? 1 : 0;
	}
	else if (opcode == "eqri") {
		registers[c] = (registers[a] == b) ? 1 : 0;
	}
	else if (opcode == "eqrr") {
		registers[c] = (registers[a] == registers[b]) ? 1 : 0;
	}
}

// figure out which instructions correspond to which
// for every potential opcode, go through its options
// - if options size is 1,
// - store it into opcode_mappings
// - erase that option from all other potential instructions
void decode_instructions(map<int, set<int>> potential_instructions, map<int, int> &opcode_mappings) {
	while (!potential_instructions.empty()) {
		for (auto it = potential_instructions.begin(); it != potential_instructions.end(); ++it) {
			if (it->second.size() == 1) {
				int target = *(it->second.begin());
				opcode_mappings[it->first] = target;

				// for each other potential instruction
				for (auto it2 = potential_instructions.begin(); it2 != potential_instructions.end(); ++it2) {
					if (it != it2) {
						it2->second.erase(target);
					}
				}

				// remove it
				it = potential_instructions.erase(it);
				if (distance(it, potential_instructions.end()) == 0) {
					break;
				}
			}
		}
	}
}

int solve(vector<string> input, bool part_two) {

	// <input, potential_opcodes>
	map<int, set<int>> potential_instructions;

	// <input, actual_opcode>
	map<int, int> opcode_mappings;

	int out = 0; // only for part 1
	size_t i; // used for both parts
	for (i = 0; i < input.size(); i += 4) {
		string before = input[i];
		string test_ins = input[i+1];
		string after = input[i+2];

		// end of samples
		if (before[0] != 'B') {
			i += 2;
			break;
		}

		// see which opcodes reseult in after
		vector<int> registers = extract_nums_from(before);
		vector<int> new_registers = extract_nums_from(after);

		vector<int> ins = extract_nums_from(test_ins);

		int temp = 0;
		int saved_j;
		for (size_t j = 0; j < instructions.size(); j++) {
			vector<int> temp_registers(registers);
			execute(temp_registers, instructions[j], ins[1], ins[2], ins[3]);

			if (temp_registers == new_registers) {
				potential_instructions[ins[0]].insert(j);
				saved_j = j;
				temp++;
			}
		}
		if (temp == 1) {
			opcode_mappings[ins[0]] = saved_j;
		}
		else if (temp >= 3) {
			out++;
		}
	}

	if (!part_two) {
		return out;
	}

	decode_instructions(potential_instructions, opcode_mappings);

	// run test program
	vector<int> registers(4, 0);
	for (; i < input.size(); i++) {
		vector<int> ins = extract_nums_from(input[i]);
		execute(registers, instructions[opcode_mappings[ins[0]]], ins[1], ins[2], ins[3]);
	}

	return registers[0];
}

int main() {
	vector<string> input = split_istream_per_line(cin);

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}
