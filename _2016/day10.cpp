#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2016/day/10


class day10
{
public:
	// rules[i] dictates how bot[i] handles its two values
	// bots[i] shows which values bot i currently has
	// if both values are populated, it should follow rules[i]
	// otherwise, it should wait until it has two values (first and second != 0)
	map<int, pair<pair<bool, int>, pair<bool, int>>> rules; // <bot, <output? lo_dest>, <output?, hi_dest>>>
	map<int, pair<int, int>> bots; // <bot, <value1, value2>>
	map<int, int> output; // <bin, value>

	const int DEFAULT_VALUE = 0;
	const pair<int, int> DEFAULT_PAIR = make_pair(DEFAULT_VALUE, DEFAULT_VALUE);
	pair<int, int> target;
	int part1;

	day10()
	{
		;
	}

	// parse instructions. populate rules and bots initial state
	void init(vector<string> input)
	{
		sort(all(input));

		for (string line : input)
		{
			auto v = split_str_by_whitespace<string>(line);

			// build the rules
			if (line[0] == 'b')
			{
				int bot_num = stoi(v[1]);
				bool lo_output = v[5] == "output";
				int lo_dest = stoi(v[6]);
				bool hi_output = v[10] == "output";
				int hi_dest = stoi(v[11]);

				rules[bot_num] = make_pair(make_pair(lo_output, lo_dest), make_pair(hi_output, hi_dest));
			}
			else // distribute initial chips
			{
				int value = stoi(v[1]);
				int dest_bot = stoi(v[5]);

				give_bot(dest_bot, value);
			}
		}
	}

	// keep processing until none of the bots have enough chips to process
	void solve()
	{
		while (true)
		{
			map<int, pair<int, int>>::iterator it;
			for (it = bots.begin(); it != bots.end(); ++it)
			{
				if (it->second.first > DEFAULT_VALUE && it->second.second > DEFAULT_VALUE)
				{
					break;
				}
			}

			// temrinating cond
			// no bot has enough chips to process
			if (it == bots.end())
			{
				break;
			}

			process(it->first);
		}
	}

	// recursively give numbers from a bot by following rules
	// if a bot we are about to give a number is already full,
	// process that bot first, etc.
	// this only works on the assumption there are no cyclic things
	void process(int bot)
	{
		auto &p = bots[bot];
		if (p.first < 1 || p.second < 1)
		{
			return;
		}

		if (p == target)
		{
			part1 = bot;
		}

		auto rule = rules[bot];
		auto rule_lo = rule.first;
		auto rule_hi = rule.second;

		// process low number
		if (rule_lo.first)
		{
			output[rule_lo.second] = p.first;
		}
		else
		{
			process(rule_lo.second);
			give_bot(rule_lo.second, p.first);
		}

		// process high number
		if (rule_hi.first)
		{
			output[rule_hi.second] = p.second;
		}
		else
		{
			process(rule_hi.second);
			give_bot(rule_hi.second, p.second);
		}
		bots.erase(bot);
	}

	void give_bot(int bot_num, int value)
	{
		// populate bots[dest_bot] if DNE
		if (bots.count(bot_num) == 0)
		{
			bots[bot_num] = DEFAULT_PAIR;
		}

		auto &p = bots[bot_num];
		if (p.first == DEFAULT_VALUE)
		{
			p.first = value;
		}
		else if (p.second == DEFAULT_VALUE)
		{
			p.second = value;
		}

		// maintain order. p.first should be lowest
		auto temp = make_pair(min(p.first, p.second), max(p.first, p.second));
		p = temp;
	}
};

int main()
{
	vector<string> input;
	for (string temp; getline(cin, temp);)
	{
		input.push_back(temp);
	}

	day10 a;
	a.init(input);

	// cout << "rules: " << a.rules << endl;
	// cout << "bots: " << a.bots << endl;

	a.target = make_pair(17, 61);
	a.solve(); // part 1 in here

	cout << "Part 1: " << a.part1 << endl;
	cout << "Part 2: " << a.output[0] * a.output[1] * a.output[2] << endl;
}
