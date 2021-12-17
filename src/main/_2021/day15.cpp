#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2021/day/15

const array<int, 4> dx = {0, 1, 0, -1};
const array<int, 4> dy = {-1, 0, 1, 0};

struct node
{
	size_t x;
	size_t y;

	size_t score; // distance travelled so far

	node()
	{
		x = 0;
		y = 0;
		score = 0;
	}

	node(const size_t &x, const size_t &y, const size_t &score) : x(x), y(y), score(score) {
		;
	}

	bool operator < (const node &n) const
	{
		return this->score < n.score;
	}

	bool operator > (const node& n) const
	{
		return this->score > n.score;
	}

	bool operator == (const node &n) const
	{
		return this->x == n.x && this->y == n.y;
	}

	bool operator != (const node &n) const
	{
		return !(*this == n);
	}

	friend ostream& operator << (ostream &os, const node &n)
	{
		os << n.x << ", " << n.y << ": " << n.score;
		return os;
	}
};

// perform Dijkstra's algorithm to get the shortest path from the start to target in the search space
size_t get_shortest_path(const vector<vector<int>> &search_space, pair<size_t, size_t> start, pair<size_t, size_t> target)
{
	// keep track of where to explore next (min cost)
	priority_queue<node, vector<node>, greater<node>> fringe;

	// keep track of the cumulative cost to get from the start to any space in the search space
	vector<vector<size_t>> cum_cost(search_space.size(), vector<size_t>(search_space[0].size(), numeric_limits<size_t>::max()));
	cum_cost[start.second][start.first] = 0;

	// only for debugging purposes
	map<pair<size_t, size_t>, node> prev;

	auto source = node(start.first, start.second, search_space[start.second][start.first]);
	fringe.push(source);
	while (!fringe.empty())
	{
		// get the current cheapest-cost solution
		auto current = fringe.top();
		fringe.pop();

		// we've reached the target!
		if (current.x == target.first && current.y == target.second)
		{
			// print out the path back to the start
			/* node n(target.first, target.second, current.score); */
			/* while (n != source) */
			/* { */
			/* 	cout << n << endl; */
			/* 	n = prev[make_pair(n.x, n.y)]; */
			/* } */

			return current.score - source.score;
		}

		// for each neighbour of current
		for (size_t i = 0; i < dx.size(); i++)
		{
			int new_x = current.x + dx[i];
			int new_y = current.y + dy[i];

			// out of bounds
			if (new_x < 0 || new_x >= static_cast<int>(search_space[0].size()) || new_y < 0 || new_y >= static_cast<int>(search_space.size()))
			{
				continue;
			}

			size_t new_score = current.score + search_space[new_y][new_x];
			node new_node(new_x, new_y, new_score);

			if (new_score < cum_cost[new_y][new_x])
			{
				cum_cost[new_y][new_x] = new_score;
				fringe.push(new_node);

				prev[make_pair(new_x, new_y)] = current;
			}
		}
	}

	return 1;
}

// expand the original grid by a scale of scale in both directions
// e.g. if originale 2x2, and expanded by 3, it should be a 6x6
// each time the grid is expanded, every value is incremented by 1 (mod 10)
// e.g. a 2x2 scaled by 2
// 1 9
// 2 8
// would look like this
// 1 9 2 1
// 2 8 3 9
// 2 1 3 2
// 3 9 4 1
vector<vector<int>> expand_grid(const vector<vector<int>> &original_grid, size_t scale)
{
	// create a to-size version
	vector<vector<int>> out((original_grid.size() * scale), vector<int>((original_grid[0].size() * scale), 0));

	// populate the rest
	for (size_t i = 0; i < out.size(); i++)
	{
		for (size_t j = 0; j < out[i].size(); j++)
		{
			// copy each grid position, +1 for every time the grid is replicated
			size_t orig_i = i % original_grid.size();
			size_t orig_j = j % original_grid[orig_i].size();
			size_t ith_grid = i / original_grid.size();
			size_t jth_grid = j / original_grid[orig_i].size();
			size_t offset_amount = ith_grid + jth_grid;

			out[i][j] = original_grid[orig_i][orig_j] + offset_amount;

			// correct for going over 9
			// note this is not the same as just doing % 10, since 8 -> 9 -> 1 -> 2
			// this just happens to work since the scale < 10, and it'll go over 9 twice
			if (out[i][j] > 9)
			{
				out[i][j] -= 9;
			}
		}
	}

	return out;
}

// get the shortest path from top-left to bottom-right
size_t part_one(const vector<vector<int>> &risk_grid)
{
	return get_shortest_path(
			risk_grid,
			make_pair(0, 0),
			make_pair(risk_grid[0].size()-1, risk_grid.size()-1)
	);
}

// same, but on a larger grid
size_t part_two(const vector<vector<int>> &risk_grid)
{
	auto expanded_grid = expand_grid(risk_grid, 5);

	return get_shortest_path(
			expanded_grid,
			make_pair(0, 0),
			make_pair(expanded_grid[0].size()-1, expanded_grid.size()-1)
	);
}

int main()
{
	vector<string> input = split_istream_per_line(cin);

	vector<vector<int>> risk_grid;
	for (auto s : input)
	{
		risk_grid.push_back(digits_of(s));
	}

	cout << "Part 1: " << part_one(risk_grid) << endl;
	cout << "Part 2: " << part_two(risk_grid) << endl;
}
