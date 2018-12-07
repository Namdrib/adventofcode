#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/7

const regex order("Step (\\w+) must be finished before step (\\w+) can begin.");
smatch match;

// some constants
const int n = 6;
const int num_workers = 2;
const int proc_time = 0 + 1;

int num_deps_in(const vector<vector<bool>> &v, int row) {
	return accumulate(all(v[row]), 0, [](int a, bool b) {
		return a + b;
	});
}



// init workers all 0
// init elapsed = 0

// for each worker w,

// 	if there is an available job and worker.size() < num_workers,
// 		w[job] = elapsed + proc + job

// 		dont clear dependency yet

// elapsed = min_time_all(workers)
// for each worker w,
// 	if w.time <= elapsed,
// 		clear the dependency held by worker
// 		clear the worker entry


int solve_part_two(vector<vector<bool>> &adj_mat, vector<int> fringe) {

	string order;
	int elapsed = 0;

	return elapsed;
}

// use bfs to solve dependencies
string solve(vector<string> input, bool part_two) {
	// used to store deps. adj_mat[i][j] = true means node j depends on i
	vector<vector<bool>> adj_mat(n, vector<bool>(n, false));

	// populate adj_mat from input
	for (string s : input) {
		regex_search(s, match, order);
		adj_mat[match.str(2)[0] - 'A'][match.str(1)[0] - 'A'] = true;
	}

	vector<int> fringe;
	set<int> closed;

	// add all the things w/o dependencies
	for (size_t i=0; i<adj_mat.size(); i++) {
		if (num_deps_in(adj_mat, i) == 0) {
			fringe.push_back(i);
		}
	}

	if (part_two) {
		int i = solve_part_two(adj_mat, fringe);
		stringstream ss;
		ss << i;
		return ss.str();
	}

	string out;

	while (!fringe.empty()) {
		// for (auto v : adj_mat) {
		// 	cout << v << endl;
		// } cout << "----------------" << endl;

		// get smallest
		sort(all(fringe));
		int current = fringe.front();
		fringe.erase(fringe.begin());

		for (size_t i=0; i<adj_mat.size(); i++) {

			if (adj_mat[i][current]) {
				adj_mat[i][current] = 0; // remove the current dependency

				if (closed.count(i) > 0) {
					continue;
				}

				if (num_deps_in(adj_mat, i) > 0) {
					continue;
				}

				if (find(all(fringe), i) != fringe.end()) {
					continue;
				}

				fringe.push_back(i);
			}
		}

		closed.insert(current);
		out += ('A' + current);
	}

	return out;

}

int main() {
	vector<string> input = split_istream_per_line(cin);

	// assert(solve("dabAcCaCBAcCcaDA", false) == 10);
	// assert(solve("dabAcCaCBAcCcaDA", true) == 4);

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}
