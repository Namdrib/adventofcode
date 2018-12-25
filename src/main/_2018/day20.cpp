#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/20

int dir_x[] = {0, 0, 1, -1};
int dir_y[] = {-1, 1, 0, 0};

map<char, int> dirs {
	{'N', 0},
	{'S', 1},
	{'E', 2},
	{'W', 3},
};

class room {
public:

	int x, y;
	int distance;

	room *parent;

	vector<room*> children; // {north, south, east, west}, like dirs

	room(int x, int y) : room(nullptr, x, y) {
	}

	room(room *parent, int x, int y) : x(x), y(y) {
		distance = 0;
		this->parent = parent;

		children = vector<room*>(4, nullptr);
	}
};

void recurse(vs &solution, string output, string input, size_t pos) {

	while (pos < input.size()) {

		// do recursion
		if (input[pos] == '(') {
			size_t matching_parenthesis = input.find_first_of(')', pos);
			string substring = input.substr(pos + 1, matching_parenthesis - pos - 1);
			pos += substring.size() + 2;

			regex r("(\\w+)+");
			auto begin_it = sregex_iterator(all(substring), r);
			auto end_it = sregex_iterator();

			for (auto it = begin_it; it != end_it; ++it) {
				smatch match = *it;
				recurse(solution, output + match.str(), input, pos);
			}
		}
		else {
			output += input[pos];
			pos++;
		}
	}

	solution.push_back(output);
}

void trace_rooms(room *root, string &input) {

	pii pos = make_pair(0, 0);
	pii old_pos = pos;

	stack<pii> s;
	stack<room*> branching_points;
	stack<int> s_num_steps;

	int num_steps = 0;
	int old_num_steps = num_steps;

	string path;

	for (size_t i = 0; i < input.size(); i++) {

		char c = toupper(input[i]);
		int dir;


		switch (c) {
			case 'N':
			case 'S':
			case 'E':
			case 'W':
				path += c;

				num_steps++;

				dir = dirs[c];
				cout << "adding a node to the " << dir << " of " << pos << endl;
				pos.first += dir_x[dir];
				pos.second += dir_y[dir];

				root->children[dir] = new room(root, pos.first, pos.second);
				root->distance = num_steps;
				root = root->children[dir];

		cout << "path so far: " << path << endl;
				break;

			case '(':

				s.push(pos);
				old_pos = pos;

				branching_points.push(root);

				s_num_steps.push(num_steps);
				old_num_steps = num_steps;

				break;

			case '|':

				pos = old_pos;
				num_steps = old_num_steps;

				path = path.substr(0, num_steps);

				break;

			case ')':

				pos = s.top();
				s.pop();

				root = branching_points.top();
				branching_points.pop();

				num_steps = s_num_steps.top();
				s_num_steps.pop();

				path = path.substr(0, num_steps);

				break;

			default:
				cout << "unknown character " << c << endl;
				break;
		}

	}
}

int solve(string input, bool part_two) {

	room *root = new room(0, 0);

	input = input.substr(1, input.size()-2);
	trace_rooms(root, input);

	// perhaps dfs to find room coords furthest away

	// then bfs to find shortest path there?

	delete root;

	int out = 0;
	return out;
}

int main() {
	string input;
	getline(cin, input);

	input = "^N(SS|)N(E|S)W$";

	// assert(generate_options_from("^N(SS|)N(E|S)W$") == (vs{
	// 	"NNES",
	// 	"NNEW",
	// 	"NSSNEW",
	// 	"NSSNSW",
	// }));

	// assert(generate_options_from("^ENWWW(NEEE|SSE(EE|N))$") == (vs{
	// 	"ENWWWNEEE",
	// 	"ENWWWSSEEE",
	// 	"ENWWWSSEN",
	// }));

	// assert(solve("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$", false) == 23);
	// assert(solve("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$", false) == 31);

	cout << "Part 1: " << solve(input, false) << endl;
	// cout << "Part 2: " << solve(input, true) << endl;
}
