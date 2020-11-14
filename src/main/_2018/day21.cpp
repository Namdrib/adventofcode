#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/19

const vector<string> instructions = {
	"addr", "addi",
	"mulr", "muli",
	"banr", "bani",
	"borr", "bori",
	"setr", "seti",
	"gtir", "gtri", "gtrr",
	"eqir", "eqri", "eqrr",
};

void execute(vi &registers, const string &opcode, int a, int b, int c) {
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
	else {
		cerr << "Illegal opcode \"" << opcode << "\"" << endl;
	}
}

// got from analysing the assembly, see day19.txt
int shortcut(bool part_two) {
	int r0 = 0;
	int r5 = 964;
	if (part_two) {
		r5 += 10550400;
	}
	for (int r3 = 1; r3 <= r5; r3++) {
		if (r5 % r3 == 0) {
			r0 += r3;
		}
	}

	return r0;
}

int solve_inner(const vector<pair<string, vi>> &instructions, const int ip, int zero, bool part_two) {

	vi registers(6, 0);
	registers[0] = zero;

	int num_instructions = 0;
	int instruction_limit = 1000000;

	while (registers[ip] < instructions.size() && num_instructions < instruction_limit) {
		// target = registers[ip];
		pair<string, vi> ins = instructions[registers[ip]];

		// if (registers[ip] == 4)
		// cout << "ip=" << registers[ip] << " [" << registers << "] " << ins;

		execute(registers, ins.first, ins.second[0], ins.second[1], ins.second[2]);

		// if (registers[ip] == 4)
		// cout << " [" << registers << "]" << endl;

		registers[ip]++;
		num_instructions++;
	};

	return num_instructions;
}

int solve(vs &input, bool part_two) {

	int ip = extract_nums_from(input[0])[0];

	// preprocess the input
	vector<pair<string, vi>> instructions;
	for (size_t i = 1; i < input.size(); i++) {
		string opcode = input[i].substr(0, input[i].find_first_of(" "));
		vi args = extract_nums_from(input[i]);
		instructions.push_back(make_pair(opcode, args));
	}

	int best_i;
	int min_instructions = numeric_limits<int>::max();

	int i;
	for (i=1; ; i++) {
		cout << "solving for i = " << i << endl;

		int num_instructions = solve_inner(instructions, ip, i, part_two);
		if (num_instructions < min_instructions) {
			cout << "new minimum at " << num_instructions << "(i = " << i << ")" << endl;
			min_instructions = num_instructions;
			best_i = i;
		}
	}

	return i;
}

int main() {
	vs input = split_istream_per_line(cin);

	// cout << "Part 1: " << shortcut(false) << endl;
	// cout << "Part 2: " << shortcut(true) << endl;
	cout << "Part 1: " << solve(input, false) << endl;
	// cout << "Part 2: " << solve(input, true) << endl;
}
