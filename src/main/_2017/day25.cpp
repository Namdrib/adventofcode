#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

class state
{
public:
	string name;

	// things to do if current value is zero
	bool write_zero;
	bool move_dir_zero; // 0 is left, 1 is right
	string next_state_zero;

	// things to do if current value is one
	bool write_one;
	bool move_dir_one; // 0 is left, 1 is right
	string next_state_one;

	void init(string &name,
			bool write_zero, bool move_dir_zero, string next_state_zero,
			bool write_one, bool move_dir_one, string next_state_one) {
		this->name = name;

		this->write_zero = write_zero;
		this->move_dir_zero = move_dir_zero;
		this->next_state_zero = next_state_zero;

		this->write_one = write_one;
		this->move_dir_one = move_dir_one;
		this->next_state_one = next_state_one;
	}

	void move(list<bool> &tape, list<bool>::iterator &it, bool dir) {
		if (dir) {
			if (++it == tape.end()) {
				tape.push_back(0);
				it = --tape.end();
			}
			// ++it;
		}
		else {
			if (it == tape.begin()) {
				tape.push_front(0);
			}
			--it;
		}
	}

	// pass tape and it by ref to allow modifications
	string do_action(list<bool> &tape, list<bool>::iterator &it) {
		// one
		if (*it) {
			*it = write_one;

			move(tape, it, move_dir_one);

			return next_state_one;

		}
		// zero
		else {
			*it = write_zero;
			
			move(tape, it, move_dir_zero);

			return next_state_zero;
		}
	}
};


// regex stuff for parsing the state inputs
const regex state_name ("In state (.*):");
const regex write_value("    - Write the value (\\d+).");
const regex move_dir("    - Move one slot to the (\\w+).");
const regex next_state("    - Continue with state (\\w+).");
smatch match;

// contains an infinite tape and a bunch of states
class state_machine
{
public:
	list<bool> tape;
	list<bool>::iterator it; // use it to navigate the tape

	map<string, state> states;

	int num_steps;

	string current_state;

	state_machine() {
		tape.push_back(0);
		it = tape.begin();
	}

	void parse(vector<string> &input) {
		size_t last_space = input[0].find_last_of(" ");
		current_state = input[0].substr(last_space+1, input[0].size()-2-last_space);

		last_space = input[1].find_last_of(" ");
		size_t first_digit = input[1].find_first_of("0123456789");
		string temp = input[1].substr(first_digit, last_space - first_digit);
		num_steps = stoi(temp);

		// each iteration of the loop is enough lines to define a single state
		for (size_t i=3; i<input.size(); i+=10) {
			string name;
			bool write_zero, write_one;
			bool move_dir_zero, move_dir_one;
			string next_state_zero, next_state_one;

			regex_search(input[i], match, state_name);
			name = match.str(1);

			// current value 0
			regex_search(input[i+2], match, write_value);
			write_zero = to_bool(match.str(1));

			regex_search(input[i+3], match, move_dir);
			move_dir_zero = match.str(1) == "right";

			regex_search(input[i+4], match, next_state);
			next_state_zero = match.str(1);

			// current value 1
			regex_search(input[i+6], match, write_value);
			write_one = to_bool(match.str(1));

			regex_search(input[i+7], match, move_dir);
			move_dir_one = match.str(1) == "right";

			regex_search(input[i+8], match, next_state);
			next_state_one = match.str(1);

			states[name].init(name,
				write_zero, move_dir_zero, next_state_zero,
				write_one, move_dir_one, next_state_one);
		}
	}

	void print_tape() {
		cout << "tape: ";
		for (auto print_it = tape.begin(); print_it != tape.end(); ++print_it) {
			cout << *print_it << " ";
		}
		cout << endl;
		cout << "      ";
		for (auto print_it = tape.begin(); print_it != tape.end(); ++print_it) {
			cout << ((print_it == it) ? "^" : " ") << " ";
		}
		cout << endl;
	}

	void step() {
		current_state = states[current_state].do_action(tape, it);
		// print_tape();

	}

	// do checksum by counting number of ones
	int checksum() {
		return accumulate(all(tape), 0);
	}
};

int solve(state_machine &sm, bool part_two) {
	if (part_two) {
		return 0;
	}
	else {
		return sm.checksum();
	}
}

int main()
{
	vector<string> input = split_istream_per_line(cin);

	state_machine sm;

	sm.parse(input);

	for (int i=0; i<sm.num_steps; i++) {
		sm.step();
	}

	cout << "Part 1: " << solve(sm, false) << endl;
}
