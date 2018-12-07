#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/7

const regex order("Step (\\w+) must be finished before step (\\w+) can begin.");
smatch match;

// some constants
const int n = 26;
const int num_workers = 5;
const int proc_time = 60 + 1; // lhs of + is main proc time, rhs is alphabet offset (A = 1)

int num_deps_in(const vector<vector<bool>> &v, int row) {
	return accumulate(all(v[row]), 0, [](int a, bool b) {
		return a + b;
	});
}

// clear col n from every row in the adj_mat
// then update fringe and closed as necessary
void bfs_body(vector<vector<bool>> &adj_mat, priority_queue<int, vector<int>, greater<int>> &fringe, set<int> &closed, int n) {

	// clear dependencies, update fringe and closed
	for (size_t i = 0; i < adj_mat.size(); i++) {

		if (adj_mat[i][n]) {
			adj_mat[i][n] = 0; // remove the current dependency

			if (closed.count(i) > 0) {
				continue;
			}

			if (num_deps_in(adj_mat, i) > 0) {
				continue;
			}

			fringe.push(i);
		}
	}

	closed.insert(n);
}

// until all jobs are done,
// finish current jobs
// assign possible jobs
int solve_part_two(vector<vector<bool>> &adj_mat, priority_queue<int, vector<int>, greater<int>> fringe) {

	string order;

	// keep track of when each work is working until and what they're workin gon
	// working_until[w] == t means worker w is working until time t
	// working_on[w] == n means worker w is working on node n
	vector<int> working_until(num_workers, 0);
	vector<int> working_on(num_workers, -1);

	set<int> closed; // completed jobs

	int elapsed;
	for (elapsed = 0; (closed.size() != adj_mat.size()); elapsed++) {

		// skip elapsed to the earliest-finishing active job
		// this avoids essentially "empty" loops where jobs are
		// just ticking away with no change in state
		vector<int> active_working_until;
		for (size_t i = 0; i < num_workers; i++) {
			if (working_on[i] >= 0) {
				active_working_until.push_back(working_until[i]);
			}
		}
		if (!active_working_until.empty()) {
			elapsed = *min_element(all(active_working_until));
		}

		// free all the workers who are done
		// also clearing any dependencies as a result
		for (size_t i = 0; i < num_workers; i++) {
			if (working_on[i] >= 0 && working_until[i] <= elapsed) {

				int current = working_on[i];

				bfs_body(adj_mat, fringe, closed, current);

				order += ('A' + current);
				working_on[i] = -1;
			}
		}

		// assign jobs to open workers
		for (size_t i = 0; i < num_workers; i++) {
			if (working_until[i] <= elapsed) {
				if (!fringe.empty()) {
					int current = fringe.top();
					fringe.pop();

					working_until[i] = elapsed + proc_time + current;
					working_on[i] = current;
				}
			}
		}
	}

	// don't want to increase elapsed after last one
	return --elapsed;
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

	priority_queue<int, vector<int>, greater<int>> fringe;
	set<int> closed;

	// add all the things w/o dependencies
	for (size_t i=0; i<adj_mat.size(); i++) {
		if (num_deps_in(adj_mat, i) == 0) {
			fringe.push(i);
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
		// get smallest
		int current = fringe.top();
		fringe.pop();

		bfs_body(adj_mat, fringe, closed, current);

		out += ('A' + current);
	}

	return out;
}

int main() {
	vector<string> input = split_istream_per_line(cin);

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}
