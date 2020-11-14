#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/8

static int id = 0;

class node
{
public:
	vector<node> children;
	vector<size_t> metadata;

	int id;
};

void read_recurse(const vector<int> &input, node &root, int &start) {
	int num_children = input[start];
	int num_metadata = input[start+1];

	root.children.resize(num_children);
	root.metadata.resize(num_metadata);
	root.id = id;
	id++;

	for (auto &child : root.children) {
		start += 2;
		read_recurse(input, child, start);
	}

	for (auto &metadata : root.metadata) {
		start++;
		metadata = input[start+1];
	}
}

// recursively sum the metadata of a root and its children
int sum_metadata(const node &root) {

	int out = 0;

	for (auto child : root.children) {
		out += sum_metadata(child);
	}
	out += accumulate(all(root.metadata), 0);

	return out;
}

// recursively sum the _value_ of a root and its children
// a node's value is the sum of its metadata (if no children)
// or the value of its children, as referred to by the metadata
// children may be counted multiple times
int sum_value(const node &root) {

	int out = 0;

	if (root.children.empty()) {
		return sum_metadata(root);
	}

	// metadata are 1-indexed
	for (auto metadata : root.metadata) {
		metadata--;
		if (metadata < root.children.size()) {
			out += sum_value(root.children[metadata]);
		}
	}

	return out;
}

int solve(node root, bool part_two) {

	if (part_two) {
		return sum_value(root);
	}

	return sum_metadata(root);
}

int main() {
	vector<int> input = split_istream_by_whitespace<int>(cin);

	node root;
	int start = 0;
	read_recurse(input, root, start);

	cout << "Part 1: " << solve(root, false) << endl;
	cout << "Part 2: " << solve(root, true) << endl;
}
