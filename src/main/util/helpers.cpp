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
ostream& operator << (ostream &os, const Container<T> &v)
{
	const char* delim = " ";
	copy(v.begin(), --v.end(), ostream_iterator<T>(os, delim));
	os << v.back();
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
bool isPrime(T n)
{
	for (T i=2; i<sqrt(n); i++)
	{
		if (n % i == 0)
		{
			return false;
		}
	}
	return true;
}

template <typename T>
T manhattan_distance(T x1, T y1, T x2, T y2)
{
	return abs(x1 - x2) + abs(y1 - y2);
}

bool to_bool(string s)
{
	return !(s[0] == '0');
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


#endif // HELPERS_CPP
