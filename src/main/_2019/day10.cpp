#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2019/day/10

class blast
{
public:

	int x, y;
	double angle;
	double distance;

	blast(int x, int y, int dest_x, int dest_y)
	{
		this->x = dest_x;
		this->y = dest_y;

		int dist_x = dest_x - x;
		int dist_y = dest_y - y;

		// calculated in such a fashion that directly up from us is zero degrees
		distance = sqrt(pow(dist_x, 2) + pow(dist_y, 2));
		angle = atan2(dist_x, -dist_y) * 180 / M_PI;
	}

	bool operator < (const blast &b)
	{
		if (angle == b.angle)
		{
			return distance < b.distance;
		}
		return angle < b.angle;
	}
};

set<double> get_unique_angles_from(const vector<string> &v, size_t x, size_t y)
{
	// count number of unique angles from
	// this asteroid to all other asteroids
	set<double> unique_angles;

	// check every other position, count visible asteroids
	for (size_t i = 0; i < v.size(); i++)
	{
		for (size_t j = 0; j < v[i].size(); j++)
		{
			// only look at other asteroids
			if ((i == y && j == x) || v[i][j] == '.')
			{
				continue;
			}

			// calculated in such a fashion that directly up from us is zero degrees
			int dist_x = j - x;
			int dist_y = i - y;
			double angle = atan2(dist_x, -dist_y) * 180 / M_PI;
			unique_angles.insert(angle);
		}
	}

	return unique_angles;
}

size_t calculate_best_monitoring_location(vector<string> v, pair<size_t, size_t> &location)
{
	size_t best_visible_asteroids = 0;
	size_t best_y = 0;
	size_t best_x = 0;

	// for each position with an asteroid
	for (size_t i = 0; i < v.size(); i++)
	{
		for (size_t j = 0; j < v[i].size(); j++)
		{
			if (v[i][j] == '.')
			{
				continue;
			}

			// calculate how many asteroids we can see
			// this is base on the amount of unique angles to other asteroids from here
			set<double> unique_angles = get_unique_angles_from(v, j, i);
			size_t visible_asteroids = unique_angles.size();

			// save best
			if (visible_asteroids > best_visible_asteroids)
			{
				best_visible_asteroids = visible_asteroids;
				best_y = i;
				best_x = j;
			}
		}
	}

	location.first = best_x;
	location.second = best_y;
	return best_visible_asteroids;
}

size_t part_one(vector<string> v, bool part_two = false)
{
	// find the asteroid that can see the most other asteroids
	// return the number of asteroids visible from there
	pair<size_t, size_t> position;
	size_t asteroids_detected = calculate_best_monitoring_location(v, position);
	return asteroids_detected;
}

size_t part_two(vector<string> v)
{
	// from the best viewing position, start shooting at (and destroying) asteroids
	// start facing up, and rotate clockwise to the next visible asteroid
	// this means that asteroids directly behind other asteroids have to wait a full rotation
	// before being destroyed
	pair<size_t, size_t> position;
	calculate_best_monitoring_location(v, position);
	size_t best_x = position.first;
	size_t best_y = position.second;

	// store the angle and distance of all asteroids relative to best one
	// need to know the x and y to output the final answer
	vector<blast> blasts;
	for (size_t i = 0; i < v.size(); i++)
	{
		for (size_t j = 0; j < v[i].size(); j++)
		{
			if ((i == best_y && j == best_x) || v[i][j] == '.')
			{
				continue;
			}

			blast temp = blast(best_x, best_y, j, i);
			blasts.push_back(temp);
		}
	}
	// the next blasts element will always be the next in order
	// except for when there are multiple asteroids behind each other
	sort(all(blasts));

	set<double> unique_angles = get_unique_angles_from(v, best_x, best_y);

	// We want to know the co-ordinates of the Xth asteroid we destroy
	const size_t blast_limit = 200;

	double current_angle = 0.0;
	size_t index = 0;
	size_t last_index = 0;
	size_t final_x = 0;
	size_t final_y = 0;

	// rotate until we are looking at the one directly up from where we are
	while (blasts[index].angle != current_angle)
	{
		index++;
	}

	// keep blasting until all the asteroids are gone!
	for (size_t blast_number = 1; !blasts.empty(); blast_number++)
	{
		// save coordinates of the blast_limit blast
		if (blast_number == blast_limit)
		{
			final_x = blasts[index].x;
			final_y = blasts[index].y;
		}

		// blast the asteroid away!
		last_index = index;
		current_angle = blasts[index].angle;
		blasts.erase(blasts.begin() + index);

		// the nxet bit segfaults if we don't break early
		if (blasts.empty())
		{
			break;
		}

		// skip all the ones of the same angle (since they're behind the current one)
		while (blasts[index].angle == current_angle)
		{
			index = (index + 1) % blasts.size();

			if (last_index == index)
			{
				index = 0;
				break;
			}
		}
	}

	size_t out = final_x * 100 + final_y;
	return out;
}

int main()
{
	vector<string> input;
	for (string temp; getline(cin, temp); )
	{
		input.push_back(temp);
	}

	cout << "Part 1: " << part_one(input) << endl;
	cout << "Part 2: " << part_two(input) << endl;
}
