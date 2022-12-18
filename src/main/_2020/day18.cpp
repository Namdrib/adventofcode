#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2020/day/18

// recursively evaluate the expression
// parse the parenthesis first to establish the order of operations
// then do left-to-right evaluation
size_t evaluate(const string &s, size_t &acc)
{
	cout << "eval called with " << s << endl;
	if (s.empty())
	{
		cout << "evaluate called empty!" << endl;
		return 0;
	}

	// s is just the number, return just that
	if (s.find(" ") == string::npos)
	{
		cout << s << " -> " << stoi(s) << endl;
		/* acc += stoi(s); */
		return stoi(s);
	}

	// split LHS, sign and RHS
	size_t lhs_start, lhs_end, sign_pos, rhs_start, rhs_end;

	size_t open_paren_pos = s.find("(");
	size_t close_paren_pos;
	if (open_paren_pos != string::npos)
	{
		cout << "found parens at " << open_paren_pos;
		size_t close_paren_pos = 0;
		size_t depth_counter = 0;
		for (size_t i=open_paren_pos; i<s.size(); i++)
		{
			if (s[i] == '(')
			{
				++depth_counter;
			}
			else if (s[i] == ')' and depth_counter == 0)
			{
				close_paren_pos = i;
				break;
			}
		}

		cout << " till " << close_paren_pos << endl;
		lhs_start = open_paren_pos + 1;
		lhs_end = close_paren_pos;
	}
	else
	{
		lhs_start = 0;
		lhs_end = s.find(" ");
	}

	sign_pos = s.find_first_of("*+", lhs_end);
	cout << "sign at " << sign_pos << endl;

	rhs_start = s.find(" ", sign_pos) + 1;

	// Split the expression into operator and operands
	string lhs = s.substr(lhs_start, lhs_end - lhs_start);
	string rhs = s.substr(rhs_start);
	string sign = s.substr(sign_pos, 1);

	// Evaluate the expression
	cout << "breakdown = |" << lhs << "|" << sign << "|" << rhs << "|" << endl;
	size_t right_val = evaluate(rhs, acc);
	size_t left_val = evaluate(lhs, acc);
	if (sign == "*")
	{
		cout << "final = " << left_val << " * " << right_val << endl;
		return left_val * right_val;
	}
	else
	{
		cout << "final = " << left_val << " + " << right_val << endl;
		return left_val + right_val;
	}

	return 0;
}

// wrapper for evaluate(string, size_t)
size_t evaluate(const string &s)
{
	cout << "=== Evaluating " << s << " ===" << endl;
	size_t sum = 0;
	return evaluate(s, sum);
	return sum;
}

size_t solve(const vector<string> &in, bool part_two)
{
	size_t out = 0;

	for (size_t i = 0; i < in.size(); i++)
	{
		size_t sum = evaluate(in[i]);
		cout << "sum of " << in[i] << " = " << sum << endl;
		out += sum;
	}

	return out;
}

int main(int argc, char** argv)
{
	if (argc != 1)
	{
		assert(evaluate("1 + 2") == 3);
		assert(evaluate("1 + 2 * 3 + 4 * 5 + 6") == 71);
		assert(evaluate("1 + (2 * 3) + (4 * (5 + 6))") == 51);
		assert(evaluate("2 * 3 + (4 * 5)") == 26);
		assert(evaluate("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437);
		assert(evaluate("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240);
		assert(evaluate("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632);
		return 0;
	}

	vector<string> input = split_istream_per_line(cin);
	// split_istream_by_whitespace

	/* cout << "Part 1: " << solve(input, false) << endl; */
	/* cout << "Part 2: " << solve(input, true) << endl; */
}

