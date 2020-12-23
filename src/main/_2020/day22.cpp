#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2020/day/22

void play_crab_combat_turn(deque<int> &p1, deque<int> &p2)
{
	if (p1.empty() || p2.empty())
	{
		return;
	}

	cout << "Player 1's deck: " << p1 << endl;
	cout << "Player 2's deck: " << p2 << endl;

	// draw the first of each deck
	int a = p1.front();
	int b = p2.front();
	p1.pop_front();
	p2.pop_front();

	cout << "Player 1 plays: " << a << endl;
	cout << "Player 2 plays: " << b << endl;

	if (a > b)
	{
		cout << "Player 1 wins the round!" << endl;
		p1.push_back(max(a, b));
		p1.push_back(min(a, b));
	}
	else
	{
		cout << "Player 2 wins the round!" << endl;
		p2.push_back(max(a, b));
		p2.push_back(min(a, b));
	}
	cout << endl;
}

size_t solve(const vector<string> &in, bool part_two)
{
	// read input
	size_t input_idx;
	deque<int> p1;
	// read player 1
	for (input_idx = 0; input_idx < in.size(); input_idx++)
	{
		if (in[input_idx].empty())
		{
			input_idx++;
			break;
		}
		if (in[input_idx][0] != 'P')
		{
			p1.push_back(stoi(in[input_idx]));
		}
	}

	// read player 2
	deque<int> p2;
	for (; input_idx < in.size(); input_idx++)
	{
		if (in[input_idx][0] != 'P')
		{
			p2.push_back(stoi(in[input_idx]));
		}
	}

	// play play_crab combat
	size_t num_rounds = 1;
	while (!p1.empty() && !p2.empty())
	{
		cout << "-- Round " << num_rounds << " --" << endl;
		play_crab_combat_turn(p1, p2);
		num_rounds++;
		// play a round
	}

	cout << "== Post-game results ==" <<endl;
	cout << "Player 1's deck: " << p1 << endl;
	cout << "Player 2's deck: " << p2 << endl;

	size_t winner_score = 0;
	deque<int> *winner = p1.empty() ? &p2 : &p1;
	for (size_t i = 0; i < winner->size(); i++)
	{
		winner_score += (winner->size() - i) * (*winner)[i];
	}

	return winner_score;
}


int main(int argc, char** argv)
{
	vector<string> input = split_istream_per_line(cin);

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}

