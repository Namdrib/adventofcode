#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2016/day/21

// swap position X with position Y
// the letters at indexes X and Y (counting from 0) should be swapped
void swap_by_position(string &s, int x, int y) {
	swap(s[x], s[y]);
}

// swap letter X with letter Y
// the letters X and Y should be swapped
// (regardless of where they appear in the string)
void swap_by_letter(string &s, char x, char y) {
	int index_x = s.find(x);
	int index_y = s.find(y);
	swap(s[index_x], s[index_y]);
}

// rotate left/right X steps
// the whole string should be rotated
// for example, one right rotation would turn abcd into dabc
void rotate_num_steps(string &s, bool left, int steps) {
	steps %= s.size();
	steps = (left) ? steps : s.size() - steps;
	steps %= s.size();
	rotate(s.begin(), s.begin() + steps, s.end());
}

// rotate based on position of letter X
// the whole string should be rotated to the right based on the index of
// letter X (counting from 0) as determined before this instruction does
// any rotations. Once the index is determined, rotate the string to the
// right one time, plus a number of times equal to that index, plus one
// additional time if the index was at least 4.
void rotate_on_letter(string &s, char c) {
	// calculate number of times to rotate right
	int index_c = s.find(c);
	int steps = 1 + index_c + (index_c >= 4);

	rotate_num_steps(s, false, steps);
}

// reverse positions X through Y
// the span of letters at indexes X through Y (including the letters at
// X and Y) should be reversed in order
void reverse_by_position(string &s, int x, int y) {
	int i = x;
	int j = y;
	for (; i <= j; i++, j--) {
		swap(s[i], s[j]);
	}
}

// move position X to position Y
// the letter which is at index X should be removed from the string,
// then inserted such that it ends up at index Y
void move_letter(string &s, int x, int y) {
	char c = s[x];
	s.erase(x, 1);
	s.insert(s.begin() + y, c);
}

// scramble a string s according to the input instructions
// part_two performs unscrambing instead
string scramble(string password, vector<vector<string>> input, bool part_two) {

	// try every permutation of "abc..."
	// see if scrambling them creates target
	if (part_two) {
		string permutation;
		for (size_t i = 0; i < password.size(); i++) {
			permutation += 'a' + i;
		}

		do {
			if (scramble(permutation, input, false) == password) {
				break;
			}
		} while (next_permutation(all(permutation)));
		return permutation;
	}

	for (auto it = input.begin(); it != input.end(); ++it) {
		auto instruction = *it;
		if (instruction[0] == "swap") {
			if (instruction[1] == "position") {
				swap_by_position(password, stoi(instruction[2]), stoi(instruction[5]));
			}
			else {
				swap_by_letter(password, instruction[2][0], instruction[5][0]);
			}
		}
		else if (instruction[0] == "rotate") {
			if (instruction[1] == "based") {
				rotate_on_letter(password, instruction[6][0]);
			}
			else {
				rotate_num_steps(password, instruction[1] == "left", stoi(instruction[2]));
			}
		}
		else if (instruction[0] == "reverse") {
			reverse_by_position(password, stoi(instruction[2]), stoi(instruction[4]));
		}
		else if (instruction[0] == "move") {
			move_letter(password, stoi(instruction[2]), stoi(instruction[5]));
		}
	}

	return password;
}

void test() {
	string s;

	// swap_by_position
	s = "abcd";
	swap_by_position(s, 0, 2);
	assert(s == "cbad");
	swap_by_position(s, 2, 0);
	assert(s == "abcd");

	// swap_by_letter
	s = "abcd";
	swap_by_letter(s, 'a', 'c');
	assert(s == "cbad");
	swap_by_letter(s, 'c', 'a');
	assert(s == "abcd");

	// rotate_num_steps
	s = "abcd";
	rotate_num_steps(s, false, 1);
	assert(s == "dabc");
	rotate_num_steps(s, true, 1);
	assert(s == "abcd");
	rotate_num_steps(s, true, 0);
	assert(s == "abcd");

	// rotate_on_letter
	s = "abcd";
	rotate_on_letter(s, 'a');
	assert(s == "dabc");
	rotate_on_letter(s, 'a');
	assert(s == "bcda");
	rotate_on_letter(s, 'a');
	assert(s == "bcda");
	rotate_on_letter(s, 'd');
	assert(s == "cdab");

	s = "abcdefgh";
	rotate_on_letter(s, 'a');
	assert(s == "habcdefg");
	rotate_on_letter(s, 'f');
	assert(s == "habcdefg");

	// reverse_by_position
	s = "abcd";
	reverse_by_position(s, 2, 2);
	assert(s == "abcd");
	reverse_by_position(s, 0, 3);
	assert(s == "dcba");
	reverse_by_position(s, 1, 2);
	assert(s == "dbca");
	reverse_by_position(s, 1, 2);
	assert(s == "dcba");

	// move_letter
	s = "abcde";
	move_letter(s, 0, 3);
	assert(s == "bcdae");
	move_letter(s, 3, 0);
	assert(s == "abcde");
	move_letter(s, 2, 2);
	assert(s == "abcde");

	// example
	s = "abcde";
	vector<vector<string>> instructions = {
		vector<string> {"swap", "position", "4", "with", "position", "0"},
		vector<string> {"swap", "letter", "d", "with", "letter", "b"},
		vector<string> {"reverse", "positions", "0", "through", "4"},
		vector<string> {"rotate", "left", "1", "step"},
		vector<string> {"move", "position", "1", "to", "position", "4"},
		vector<string> {"move", "position", "3", "to", "position", "0"},
		vector<string> {"rotate", "based", "on", "position", "of", "letter", "b"},
		vector<string> {"rotate", "based", "on", "position", "of", "letter", "d"},
	};
	s = scramble(s, instructions, false);
	assert(s == "decab");

	// example part 2
	s = "decab";
	s = scramble(s, instructions, true);
	assert(s == "abcde");
}

int main() {

	test();

	vector<vector<string>> input;
	auto a = split_istream_per_line(cin);
	for (auto line : a) {
		input.push_back(split_str_by_whitespace<string>(line));
	}

	string starting1 = "abcdefgh";
	string scrambled = scramble(starting1, input, false);
	cout << "Part 1: " << scrambled << endl;

	string starting2 = "fbgdceah";
	string unscrambled = scramble(starting2, input, true);
	cout << "Part 2: " << unscrambled << endl;
}
