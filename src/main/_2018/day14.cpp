#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/14

// i is current pos
string next_n_recipes(vector<int> &recipes, int i, int n) {
	string out;
	for (int j = 0; j < n; j++) {
		out += char('0' + recipes[i]);
		i = (i + 1) % recipes.size();
	}
	return out;
}

string solve(string input, bool part_two) {

	size_t n = stoi(input);

	vector<int> board = {3, 7};
	int e1 = 0;
	int e2 = 1; // elf positions

	int num_its = 0;
	while ( (part_two) ? (num_its < 30000000) : (board.size() < n + 10) ) {
		int sum = board[e1] + board[e2];
		if (sum / 10) {
			board.push_back(sum / 10);
		}
		board.push_back(sum % 10);

		e1 = (e1 + 1 + board[e1]) % board.size();
		e2 = (e2 + 1 + board[e2]) % board.size();

		num_its++;
	}

	if (part_two) {
		vector<int> digits = digits_of(input);
		for (size_t i=0; i<board.size()-digits.size(); i++) {
			vector<int> sub(board.begin()+i, board.begin()+i+digits.size());
			if (sub == digits) {
				return to_string(i);
			}
		}
	}

	return next_n_recipes(board, n, 10);
}

int main() {
	string input;
	cin >> input;

	assert(solve("9", false) == "5158916779");
	assert(solve("5", false) == "0124515891");
	assert(solve("18", false) == "9251071085");
	assert(solve("2018", false) == "5941429882");

	assert(solve("51589", true) == "9");
	assert(solve("01245", true) == "5");
	assert(solve("92510", true) == "18");
	assert(solve("59414", true) == "2018");

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}
