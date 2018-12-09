#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/9

const regex input_regex("(\\d+) players; last marble is worth (\\d+) points");
smatch match;

int solve(string input, bool part_two) {

	regex_search(input, match, input_regex);
	const int num_players = stoi(match.str(1));
	const long num_marbles = stoi(match.str(2)) * (part_two ? 100 : 1);

	cout << "num players: " << num_players << ", last_marble worth " << num_marbles << endl;

	const int special_mult = 23;

	priority_queue<int, vector<int>, greater<int>> remaining;
	for (long i=1; i<=num_marbles; i++) {
		remaining.push(i);
	}

	// everyone starts with no points
	vector<int> players(num_players, 0);
	int player = 0;

	// designate right is clockwise, left is anticlockwise
	vector<int> circle;
	circle.push_back(0);

	int current_marble = 0; // points to position in `circle`

	// cout << "[-] " << circle << endl;
	while (!remaining.empty()) {
		int current = remaining.top();
		remaining.pop();

		int dest;
		if (current % special_mult == 0) {
			// keep current marble
			players[player] += current;

			// remove the marble 7 anti-clockwise of current_marble, add to score
			dest = current_marble - 7;
			if (dest < 0) {
				dest += circle.size();
			}
			players[player] += circle[dest];
			circle.erase(circle.begin() + dest);
		}
		else {
			dest = (current_marble + 1) % circle.size() + 1;
			circle.insert(circle.begin() + dest, current);
		}
		current_marble = dest;

		// cout << "[" << player + 1 << "] " << circle << endl;
		// cout << "current is " << circle[current_marble] << endl;
		player = (player + 1) % players.size();
	}
	// cout << "score at end: " << players << endl;
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
	// cout << "Part 2: " << solve(input, true) << endl;
}
