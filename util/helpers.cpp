#include <bits/stdc++.h>
using namespace std;

#ifndef HELPERS_CPP
#define HELPERS_CPP

#define all(c) (c).begin(), (c).end()
#define rall(c) (c).rbegin(), (c).rend()

// output vector
template <typename T>
ostream& operator << (ostream &os, const vector<T> &v)
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
	copy(s.begin(), --s.end(), ostream_iterator<T>(os, delim));
	os << s.back();
	return os;
}

// output pair
template <typename K, typename V>
ostream& operator << (ostream &os, const pair<K, V> &p)
{
	os << "<" << p.first << ", " << p.second << ">";
	return os;
}

// output pair
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

#endif // HELPERS_CPP
