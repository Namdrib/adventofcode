#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/24

// numeric_limits<int>::max();

const regex group_regex("(\\d+) units each with (\\d+) hit points (\\(.*\\) )?with an attack that does (\\d+) (\\w+) damage at initiative (\\d+)");

class group {
public:
	// self attributes
	int id;
	int num_units;
	int hp;
	int attack;
	string attack_type;
	int initiative;
	set<string> weaknesses, immunities;

	// misc stuff (E.g. for combat, target selection)
	int target_group = -1;

	group() {
		;
	}

	group(int num_units, int hp, int attack, string attack_type, int initiative) : group(num_units, hp, attack, attack_type, initiative, set<string>(), set<string>()) {
		;
	}

	group(int num_units, int hp, int attack, string attack_type, int initiative, set<string> weaknesses, set<string> immunities) : num_units(num_units), hp(hp), attack(attack), attack_type(attack_type), initiative(initiative), weaknesses(weaknesses), immunities(immunities) {
		id = 1;
	}

	friend ostream& operator << (ostream &os, const group &a) {

		os << "Group " << a.id << " contains " << a.num_units << " units";

		return os;
	}

	int damage_to(group &defender) {
		int ep = num_units * attack; // effective power

		int damage = ep;

		if (defender.immunities.count(attack_type)) {
			damage = 0;
		}
		else if (defender.weaknesses.count(attack_type)) {
			damage *= 2;
		}

		return damage;
	}

};

void construct_set(set<string> &s, string &str) {
	if (str.empty()) {
		return;
	}
	size_t split_pos = str.find("to ");
	string after = str.substr(split_pos + 3);

	auto temp = split_string_by(after, ", ");
	s = set<string>(all(temp));
}

void fight(vector<group> &a, vector<group> &b)
{

	// pre-cursor
	for (auto thing : a)
	{
		cout << thing << endl;
	}
	for (auto thing : b)
	{
		cout << thing << endl;
	}

	// target selection

	int damage_to = 0;

	const auto target_order = [](group &a, group &b) {
		int ep_a = a.num_units * a.attack;
		int ep_b = b.num_units * b.attack;
		if (ep_a == ep_b) {
			return a.initiative < b.initiative;
		}
		return ep_a < ep_b;
	};

	sort(all(a), target_order);
	sort(all(b), target_order);

	for (size_t i = 0; i < a.size(); i++)
	{
		int best_damage = -1;
		int target = -1;

		for(size_t j = 0; j < b.size(); j++) {
			int damage = a[i].damage_to(b[j]);
			if (damage > best_damage) {
				best_damage = damage;
				target = j;
			}
			else if (damage == best_damage) {

			}
		}
	}

	// attacking

}

int solve(vs &input, bool part_two) {

	vector<group> immune_system, infection;

	vector<group> *target = &immune_system;

	for (auto &s : input) {
		smatch match;
		regex_search(s, match, group_regex);
		if (match.empty()) {
			if (s.size() > 1) {
				target = (s[1] == 'm') ? &immune_system : &infection;
			}
			continue;
		}

		// set vars
		int num_units = stoi(match[1]);
		int hp = stoi(match[2]);
		string changes = match[3];
		int attack = stoi(match[4]);
		string attack_type = match[5];
		int initiative = stoi(match[6]);
		set<string> weaknesses, immunities;

		// process changes
		if (changes.size() > 1) {
			changes = changes.substr(1, changes.size() - 3);
		}

		string weak, immune;
		size_t split_loc = changes.find("; ");
		if (split_loc != string::npos) {
			immune = changes.substr(0, split_loc);
			weak = changes.substr(split_loc+2);
		}
		else {
			if (!changes.empty()) {
				if (changes[1] == 'w') {
					weak = changes;
				}
				else {
					immune = changes;
				}
			}
		}
		// cout << "weak, immune: " << weak << ", " << immune << endl;

		construct_set(weaknesses, weak);
		construct_set(immunities, immune);

		// cout << "weaknesses: " << weaknesses << endl;
		// cout << "immunities: " << immunities << endl;

		// cout << num_units << " " << hp << " " << changes << " " << attack << " " << attack_type << " " << initiative << endl;

		target->push_back(group(num_units, hp, attack, attack_type, initiative, weaknesses, immunities));
		if (target->size() > 1) {
			target->back().id = (*target)[target->size()-2].id + 1;
		}
	}

	// while (!immune_system.empty() && !infection.empty()) {
	// 	fight(immune_system, infection);
	// }

	int out = 0;
	return out;
}

int main() {
	vs input = split_istream_per_line(cin);

	cout << "Part 1: " << solve(input, false) << endl;
	// cout << "Part 2: " << solve(bots, true) << endl;
}
