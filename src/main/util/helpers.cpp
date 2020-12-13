#include <bits/stdc++.h>
using namespace std;

#ifndef HELPERS_CPP
#define HELPERS_CPP

typedef long long ll;
typedef vector<int> vi;
typedef vector<string> vs;
typedef pair<int, int> pii;
typedef vector<vi> vvi;
typedef vector<ll> vl;
typedef vector<bool> vb;
typedef vector<double> vd;

#define all(c) (c).begin(), (c).end()
#define rall(c) (c).rbegin(), (c).rend()

// output vector, list
template <typename T, template <typename, typename = allocator<T>> class Container>
ostream& operator << (ostream &os, const Container<T> &c)
{
	const char* delim = " ";
	copy(c.begin(), --c.end(), ostream_iterator<T>(os, delim));
	os << c.back();
	return os;
}

// output set
template <typename T>
ostream& operator << (ostream &os, const set<T> &s)
{
	const char* delim = " ";
	for (auto it = s.begin(); it != s.end(); ++it)
	{
		os << *it;
		if (it != --s.end())
		{
			os << delim;
		}
	}
	return os;
}

// output pair
template <typename K, typename V>
ostream& operator << (ostream &os, const pair<K, V> &p)
{
	os << "<" << p.first << ", " << p.second << ">";
	return os;
}

// pair equality
template <typename K, typename V>
const bool operator == (pair<K, V> &lhs, pair<K, V> &rhs)
{
	return lhs.first == rhs.first && lhs.second == rhs.second;
}

// output map
template <typename K, typename V>
ostream& operator << (ostream &os, const map<K, V> &m)
{
	const char* delim = ", ";
	os << "{ ";
	for (auto it = m.begin(); it != m.end(); ++it)
	{
		os << it->first << ": " << it->second;
		if (it != --m.end())
		{
			os << delim;
		}
	}
	os << " }";
	return os;
}

// used to input into a vector like
// my_vector = split_str_by_whitespace("three words here")
// {"three", "words", "here"}
template <typename T>
vector<T> split_str_by_whitespace(const string &str)
{
	stringstream ss(str);
	istream_iterator<T> begin(ss), end;
	return vector<T>(begin, end);
}

vector<string> split_string_by(string s, const string delim)
{
	vector<string> out;

	size_t pos = 0;
	string token;
	while ((pos = s.find(delim)) != string::npos)
	{
		token = s.substr(0, pos);
		out.push_back(token);
		s.erase(0, pos + delim.length());
	}
	out.push_back(s);
	return out;
}

// used to input into a vector from input stream
// could be stdin (pass cin), or a file stream
template <typename T>
vector<T> split_istream_by_whitespace(istream &is)
{
	istream_iterator<T> begin(is), end;
	return vector<T>(begin, end);
}

// used to input into a vector from input stream
// could be stdin (pass cin), or a file stream
vector<string> split_istream_per_line(istream &is)
{
	vector<string> out;
	for (string line; getline(cin, line);)
	{
		out.push_back(line);
	}
	return out;
}

// return the clamped version of v, such that
// it is between lo and hi (inclusive)
template <typename T>
T clamp(const T &v, const T &lo, const T &hi)
{
	return min(max(v, lo), hi);
}

// return true iff n is prime
template <typename T>
bool is_prime(T n)
{
	for (T i = 2; i < sqrt(n); i++)
	{
		if (n % i == 0)
		{
			return false;
		}
	}
	return true;
}

// e.g. if a[0] is x1, b[0] is x2, a[1] is y1, etc.
template <typename T>
T manhattan_distance(const vector<T> &a, const vector<T> &b)
{
	return inner_product(
		all(a), b.begin(), 0, plus<int>(),
		[](const T &a, const T &b){
			return abs(b - a);
		}
	);
}

bool to_bool(string s, char zero = '0')
{
	return !(s[0] == zero);
}

// return the digits of the string s
// assumes all characters in s are digits [0-9]
vector<int> digits_of(string s) {
	vector<int> out;

	for (char c : s) {
		if (isdigit(c)) {
			out.push_back(int(c - '0'));
		}
	}

	return out;
}

// extracts all tokens resembling numbers (positive and negative)
// does not work with decimal numbers or scientific notation (e.g. 9e9)
// integrals only
template <typename T>
vector<T> extract_nums_from(string s) {
	const regex digits_regex("(-?\\d+)+");

	auto begin_it = sregex_iterator(all(s), digits_regex);
	auto end_it = sregex_iterator();

	vector<T> out;
	for (auto it = begin_it; it != end_it; ++it) {
		smatch match = *it;
		out.push_back((T) stoll(match.str()));
	}

	return out;
}

// extracts all tokens resembling numbers (positive and negative)
// does not work with decimal numbers or scientific notation (e.g. 9e9)
// NOTE: here to maintain backward compatibility with existing programs
// might go through them and call the other one instead at some point
vector<int> extract_nums_from(string s) {
	return extract_nums_from<int>(s);
}

// whether target is between lo and hi (inclusive both sides)
template <typename R, typename S, typename T>
bool in_range(R target, S lo, T hi) {
	return target >= lo && target <= hi;
}

// returns true iff index is in the bounds of the container, false otherwise
template <typename T, template <typename, typename = allocator<T>> class Container>
bool in_bounds(const Container<T> &c, long index) {
	return index >= 0 && index < static_cast<long>(c.size());
}

bool roughly_equal(double d1, double d2, double tolerance = 0.005) {
	return abs(d1 - d2) <= tolerance;
}

#endif // HELPERS_CPP
