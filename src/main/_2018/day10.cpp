#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/10

const regex input_regex("position=<\\s*(-?\\d+),\\s*(-?\\d+)> velocity=<\\s*(-?\\d+),\\s*(-?\\d+)>");
smatch match;
	// regex_search(input, match, input_regex);
	// const int num_players = stoi(match.str(1));

class point {
public:
	pair<int, int> p;
	pair<int, int> v;

	point(int x, int y, int vx, int vy) : p(x, y), v(vx, vy){
		;
	}

	void tick() {
		p.first += v.first;
		p.second += v.second;
	}

	friend ostream& operator << (ostream &os, point &p) {
		os << p.p << ", " << p.v;
		return os;
	}
};

vector<point> parse(const vector<string> &v) {
	vector<point> out;

	for (auto s : v) {
		regex_search(s, match, input_regex);
		int x, y, vx, vy;
		x = stoi(match.str(1));
		y = stoi(match.str(2));
		vx = stoi(match.str(3));
		vy = stoi(match.str(4));

		out.push_back(point(x, y, vx, vy));
	}
	return out;
}

// No output value
// Manually determine the correct output
void solve(vector<point> points, bool part_two) {
	
	int lastX, lastY;
	lastX = lastY = numeric_limits<int>::max();
	for (int i=1; ; i++) {

		// Figure out bounds for the display so they don't go negative
		int minX, maxX, minY, maxY;
		minX = minY = numeric_limits<int>::max();
		maxX = maxY = numeric_limits<int>::min();
		for (auto &p : points) {
			p.tick();
			minX = min(minX, p.p.first);
			minY = min(minY, p.p.second);
			maxX = max(maxX, p.p.first);
			maxY = max(maxY, p.p.second);
		}

		int dispX = maxX-minX+1;
		int dispY = maxY-minY+1;

		if (dispY > lastY && dispX > lastX) {
			break;
		}

		// if the thing is of reasonable terminal width
		if (dispX > 80) {
			continue;
		}

		vector<string> display(dispY, string(dispX, '.'));
		lastY = display.size();
		lastX = display[0].size();

		// Populate the display field
		// pad with min{X,Y} to avoid negative values
		for (auto &p : points) {
			int destX = p.p.first - minX;
			int destY = p.p.second - minY;
			display[destY][destX] = '#';
		}

		// Output the stars
		cout << "Second " << i << endl;
		for (string s : display) {
			cout << s << endl;
		}
	}
}

int main() {
	vector<string> input = split_istream_per_line(cin);

	vector<point> points = parse(input);

	solve(points, false);

	cout << "Part 1: See ascii art letters" << endl;
	cout << "Part 2: See the \"Second n\" above part 1" << endl;
}
