#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/9

const regex input_regex("(\\d+) players; last marble is worth (\\d+) points");
smatch match;

// wraparound iterator increment
void increment_iterator(list<long> &container, list<long>::iterator &it) {
	if (++it == container.end()) {
		it = container.begin();
	}
}

// wraparound iterator decrement
void decrement_iterator(list<long> &container, list<long>::iterator &it) {
	if (it == container.begin()) {
		it = container.end();
	}
	--it;
}

long solve(string input, bool part_two) {

	regex_search(input, match, input_regex);
	const int num_players = stoi(match.str(1));
	const long num_marbles = stoi(match.str(2)) * (part_two ? 100 : 1);

	const int special_mult = 23;

	// everyone starts with no points
	vector<long> players(num_players, 0);
	int player = 0;

	// designate right is clockwise, left is anticlockwise
	list<long> circle;
	circle.push_back(0);
	list<long>::iterator current = circle.begin();

	for (long i = 1; i <= num_marbles; i++) {
		if (i % special_mult == 0) {
			// keep the marble
			players[player] += i;

			// remove the marble 7 anti-clockwise of current, add to score
			for (int _ = 0; _ < 7; _++) {
				decrement_iterator(circle, current);
			}
			players[player] += *current;
			current = circle.erase(current);
		}
		else {
			increment_iterator(circle, current);
			increment_iterator(circle, current);
			current = circle.insert(current, i);
		}

		player = (player + 1) % players.size();
	}

	return *max_element(all(players));
}

int main() {
	string input;
	getline(cin, input);

	assert(solve("9 players; last marble is worth 25 points", false) == 32);
	assert(solve("10 players; last marble is worth 1618 points", false) == 8317);
	assert(solve("13 players; last marble is worth 7999 points", false) == 146373);
	assert(solve("17 players; last marble is worth 1104 points", false) == 2764);
	assert(solve("21 players; last marble is worth 6111 points", false) == 54718);
	assert(solve("30 players; last marble is worth 5807 points", false) == 37305);


	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}
