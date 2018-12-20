#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/20

void recurse(vs &solution, string output, string input, size_t pos) {

	cout << "recurse on: " << input << endl;
	cout << string(12 + pos, ' ') << "^ " << pos << ", out = " << output << endl;

	while (pos < input.size()) {

		// cout << "\tgot " << input << endl;
		// cout << string(4 + 8 + pos, ' ') << "^ " << pos << endl;
		// cout << "\tout is " << output << endl;

		// do recursion
		if (input[pos] == '(') {
			size_t matching_parenthesis = input.find_first_of(')', pos);
			string substring = input.substr(pos + 1, matching_parenthesis - pos - 1);
			cout << "\tsubstring is " << substring << endl;
			pos += substring.size() + 2;

			regex r("(\\w+)+");
			auto begin_it = sregex_iterator(all(substring), r);
			auto end_it = sregex_iterator();

			for (auto it = begin_it; it != end_it; ++it) {
				smatch match = *it;
				cout << "\tmatch in " << substring << " is " << match.str() << endl;
				recurse(solution, output + match.str(), input, pos);
			}
		}
		else {
			cout << "\tpos is " << pos << ", adding " << input[pos] << endl;
			output += input[pos];
			pos++;
		}

	}

	cout << "\t(after) out is " << output << endl;

	solution.push_back(output);
}

// given a regex-like input, generate all the possible options that can be taken
vs generate_options_from(string input) {
	vs out;

	input = input.substr(1, input.size()-2); // trim the leading ^ and trailing $

	recurse(out, "", input, 0);

	sort(all(out));
	// unique(all(out));

	cout << "out is " << out << endl;
	return out;
}

// given a list of options, draw out a map of the resulting facility
vs pathfind(vs options) {
	return options;
}

int solve(string input, bool part_two) {

	vs options = generate_options_from(input);
	vs grid = pathfind(options);

	// perhaps dfs to find room coords furthest away

	// then bfs to find shortest path there?


	int out = 0;
	return out;
}

int main() {
	string input;
	getline(cin, input);

	assert(generate_options_from("^N(SS|)N(E|S)W$") == (vs{
		"NNES",
		"NNEW",
		"NSSNEW",
		"NSSNSW",
	}));

	assert(generate_options_from("^ENWWW(NEEE|SSE(EE|N))$") == (vs{
		"ENWWWNEEE",
		"ENWWWSSEEE",
		"ENWWWSSEN",
	}));

	assert(solve("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$", false) == 23);
	assert(solve("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$", false) == 31);

	cout << "Part 1: " << solve(input, false) << endl;
	// cout << "Part 2: " << solve(input, true) << endl;
}
