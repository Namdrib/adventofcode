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

			int dist_x = j - x;
			int dist_y = i - y;
			unique_angles.insert(atan2(dist_x, dist_y) * 180 / M_PI);
		}
	}

	return unique_angles;
}

int solve(vector<string> v, bool part_two = false)
{
	int out = 0;

	int best_visible_asteroids = 0;
	int best_y = 0;
	int best_x = 0;

	// for each position with a asteroid
	for (size_t i = 0; i < v.size(); i++)
	{
		for (size_t j = 0; j < v[i].size(); j++)
		{
			if (v[i][j] == '.')
			{
				continue;
			}

			int visible_asteroids = 0;
			set<double> unique_angles = get_unique_angles_from(v, j, i);
			visible_asteroids = unique_angles.size();
			// cout << j << ", " << i << " can see " << visible_asteroids << endl;

			// save best
			if (visible_asteroids > best_visible_asteroids)
			{
				best_visible_asteroids = visible_asteroids;
				best_y = i;
				best_x = j;
			}
		}
	}

	cout << "best is " << best_visible_asteroids << " at " << best_x << ", " << best_y << endl;
	if (part_two)
	{
		// store the angle and distance of all asteroids relative to best one
		// need to know the x and y to output the final answer
		vector<blast> blasts;
		for (size_t i = 0; i < v.size(); i++)
		{
			for (size_t j = 0; j < v[i].size(); j++)
			{
				if (i == best_y && j == best_x)
				{
					continue;
				}

				blast temp = blast(best_x, best_y, j, i);
				blasts.push_back(temp);
			}
		}
		sort(all(blasts));

		set<double> unique_angles = get_unique_angles_from(v, best_x, best_y);
		cout << unique_angles << endl;

		const int blast_limit = 200;
		double current_angle = 90.0;
		size_t index = 0;
		size_t last_index = 0;
		int final_x = 0;
		int final_y = 0;
		for (int blast_number = 0; !blasts.empty(); blast_number++)
		{
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

			// save coordinates of the blast_limit blast
			if (blast_number == blast_limit)
			{
				final_x = blasts[index].x;
				final_y = blasts[index].y;
			}

			// blast the asteroid away!
			last_index = index;
			current_angle = blasts[index].angle;
			if (blast_number == 0)
			{
				cout << "first angle is " << current_angle << endl;
			}
			blasts.erase(blasts.begin() + index);
		}

		cout << blast_limit << "th one at " << final_x << ", " << final_y << endl;
		out = final_x * 100 + final_y;
	}
	else
	{
		out = best_visible_asteroids;
	}

	return out;
}

int main()
{
	vector<string> input;
	for (string temp; getline(cin, temp); )
	{
		input.push_back(temp);
	}

	cout << input.size() << endl;

	// cout << atan2(0, 1) * 180 / M_PI << " " << atan2(1, 0) * 180 / M_PI << endl;
	// cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl; // incomplete, 2320 too high
}
