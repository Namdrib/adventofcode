#include <bits/stdc++.h>
#include "../util/helpers.cpp"

using namespace std;

// https: //adventofcode.com/2017/day/20

class particle {
public:
	int id, x, y, z; // id and position
	vector<int> coords;
	vector<int> v;
	vector<int> a;

	particle() : particle(0, 0, 0, 0, 0, 0, 0, 0, 0, 0) {
		;
	}

	particle(int id, int x, int y, int z, int xv, int yv, int zv, int xa, int ya, int za) : id(id) {
		coords.push_back(x);
		coords.push_back(y);
		coords.push_back(z);

		v.push_back(xv);
		v.push_back(yv);
		v.push_back(zv);

		a.push_back(xa);
		a.push_back(ya);
		a.push_back(za);
	}

	// update velocity and position
	void step() {
		for (size_t i = 0; i < coords.size(); i++) {
			v[i] += a[i];
			coords[i] += v[i];
		}
	}

	// still gaining speed in the final direction
	// i.e. any i in v[i] and a[i] have differeing signs
	bool still_accelerating() {
		for (size_t i = 0; i < coords.size(); i++) {
			if (v[i] * a[i] < 0) {
				return true;
			}
		}

		return false;
	}

	friend ostream& operator << (ostream &os, const particle &a) {
		os << "id=" << a.id << ", p=<" << a.coords << ">, v=<" << a.v << ">, a=<" << a.a << ">";
		return os;
	}
};

// delete all particles that are on the same co-ord as another particle
void handle_collisions(vector<particle> &particles) {
	for (auto it1 = particles.begin(); it1 != particles.end(); ++it1) {
		bool collision = false;
		for (auto it2 = it1 + 1; it2 != particles.end(); ++it2) {
			if (it1->coords == it2->coords) {
				it2 = --particles.erase(it2);
				collision = true;
			}
		}

		// only delete it1 after checking all other potential collisions
		// to make sure all potenetial collisions are processed
		if (collision) {
			it1 = --particles.erase(it1);
		}
	}
}

int solve(vector<particle> particles, bool part_two) {

	// used for sorting
	const vector<int> zero(3, 0);
	auto distance_lambda = [&zero](const particle &a, const particle &b) {
		return manhattan_distance(a.coords, zero) < manhattan_distance(b.coords, zero);
	};

	// keep simulating until the order doesn't change
	size_t steps = 0;
	vi order(particles.size(), 0); // strip the ids from particles to get order

	while (true) {
		bool accelerating = any_of(all(particles), [](particle &p) {
			return p.still_accelerating();
		});

		for_each(all(particles), [](particle &p) { p.step(); });

		// administer collisions - delete particles if they overlap
		if (part_two) {
			handle_collisions(particles);
		}

		// now that all the velocities are on the correct side
		// break if the order stops changing
		if (!accelerating) {
			vi old_order = order;
			sort(all(particles), distance_lambda);
			for (size_t i = 0; i < particles.size(); i++) {
				order[i] = particles[i].id;
			}

			if (old_order == order) {
				break;
			}
		}

		steps++;
	}

	// once the loop has terminated, it is impossible for any more collisions to occur
	// since all the particles are moving in the same direction as their neighbours
	// at different rates
	// at this point, the faster points are pulling ahead of the slower ones

	if (part_two) {
		return particles.size();
	}
	else {
		// get the id of the particle closest to (0,0,0)
		// the particles are already sorted
		return particles[0].id;
	}
}

int main() {

	vs raw_input = split_istream_per_line(cin);

	vector<particle> particles;
	for (size_t i = 0; i < raw_input.size(); i++) {
		vi nums = extract_nums_from(raw_input[i]);
		particles.push_back(particle(i, nums[0], nums[1], nums[2], nums[3], nums[4], nums[5], nums[6], nums[7], nums[8]));
	}

	cout << "Part 1: " << solve(particles, false) << endl;
	cout << "Part 2: " << solve(particles, true) << endl;
}
