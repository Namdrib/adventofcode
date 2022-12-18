#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2019/day/12

static int global_moon_id = 0;

class moon_t
{
public:

	int id;
	vector<int> pos;
	vector<int> vel;

	moon_t(int x, int y, int z)
	{
		pos.resize(3);
		this->pos[0] = x;
		this->pos[1] = y;
		this->pos[2] = z;

		vel.resize(pos.size(), 0);
		id = global_moon_id++;
	}

	friend ostream& operator << (ostream & os, const moon_t &m)
	{
		os << m.id << ": " << "pos=" << m.pos << ", vel=" << m.vel;
		return os;
	}

	int get_potential_energy() const
	{
		return accumulate(all(pos), 0, [](int a, int b){return a + abs(b);});
	}

	int get_kinetic_energy() const
	{
		return accumulate(all(vel), 0, [](int a, int b){return a + abs(b);});
	}

	int get_total_energy() const
	{
		return get_potential_energy() * get_kinetic_energy();
	}

	void apply_gravity(const vector<moon_t> &moons)
	{
		for (auto moon : moons)
		{
			// only look at other moons
			if (id == moon.id)
			{
				continue;
			}

			// update velocity for _this_ moon only
			for (size_t i = 0; i < pos.size(); i++)
			{
				if (pos[i] < moon.pos[i])
				{
					vel[i]++;
				}
				else if (pos[i] > moon.pos[i])
				{
					vel[i]--;
				}
			}
		}
	}

	void apply_velocity()
	{
		for (size_t i = 0; i < pos.size(); i++)
		{
			pos[i] += vel[i];
		}
	}
};

long lcm(long a, long b)
{
	return (a * b) / __gcd(a, b);
}

long solve(vector<moon_t> moons, bool part_two = false)
{
	long out = 0;

	const size_t limit = 1000000;

	// looped_time[i] = the time taken for dimension i of
	//  all moons' dimension i to repeat back to its initial state
	// e.g. looped_time[0] = 12 means all moon.pos[i]
	// loops back to their starting points at time = 12
	vector<long> looped_time(moons[0].pos.size(), -1);

	// record the initial positions of each moon
	// initial_pos[i] = dimension i
	// initial_pos[i][j] = dimension i of moon j
	vector<vector<long>> initial_pos(moons[0].pos.size());
	for (const auto &moon : moons)
	{
		for (size_t i = 0; i < initial_pos.size(); i++)
		{
			initial_pos[i].push_back(moon.pos[i]);
		}
	}

	// simulate
	for (size_t time = 0; time < limit; time++)
	{
		if (part_two)
		{
			if (time != 0)
			{
				vector<vector<long>> current_pos(moons.size());
				vector<int> current_x, current_y, current_z;

				// record current position of each moon
				for (const auto &moon : moons)
				{
					for (size_t j = 0; j < current_pos.size(); j++)
					{
						current_pos[j].push_back(moon.pos[j]);
					}
				}

				// if any of the dimensions has returned to its starting point
				// record the time taken for that one dimension
				for (size_t j = 0; j < looped_time.size(); j++)
				{
					if (looped_time[j] == -1)
					{
						if (current_pos[j] == initial_pos[j])
						{
							looped_time[j] = time + 1;
						}
					}
				}
			}

			// now know the period of each dimension (separately)
			// the intersection of every dimension (collectively) can be calculated from here
			if (all_of(all(looped_time), [](long a){return a != -1;}))
			{
				break;
			}
		}

		// update the moons' gravity and velocity
		for (auto &moon : moons)
		{
			moon.apply_gravity(moons);
		}

		for (auto &moon : moons)
		{
			moon.apply_velocity();
		}
	}

	// the total energy of all the moons
	out = accumulate(all(moons), 0, [](int a, const moon_t &m){
		return a + m.get_total_energy();
	});

	// the lowest common multiple of all of looped_time
	if (part_two)
	{
		out = accumulate(all(looped_time), looped_time[0], [](long a, long b){
			return lcm(a, b);
		});
	}

	return out;
}

int main()
{
	vector<moon_t> moons;
	for (string s; getline(cin, s);)
	{
		vector<int> temp = extract_nums_from<int>(s);
		moons.push_back(moon_t(temp[0], temp[1], temp[2]));
	}

	cout << "Part 1: " << solve(moons, false) << endl;
	cout << "Part 2: " << solve(moons, true) << endl;
}
