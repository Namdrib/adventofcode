#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

// http://adventofcode.com/2016/day/13

const int DIM = 50;

class coord
{
public:
	coord()
	{
		num_steps = 0;
	}
	coord(size_t x, size_t y) : coord()
	{
		this->x = x;
		this->y = y;
	}
	coord(size_t x, size_t y, size_t num_steps) : coord(x, y)
	{
		this->num_steps = num_steps;
	}

	friend ostream& operator << (ostream &os, coord c)
	{
		os << "(" << c.x << "," << c.y << ") : " << c.num_steps;
		return os;
	}

	bool operator == (const coord &rhs)
	{
		return (x == rhs.x && y == rhs.y);
	}

	size_t x;
	size_t y;
	size_t num_steps;
};

int formula(int x, int y)
{
	return x*x + 3*x + 2*x*y + y + y*y;
}

string to_binary_string(int n)
{
	string out;
	while (n >>= 1)
	{
		out = to_string(n&1) + out;
	}
	if (out.empty()) out = "0";
	return out;
}

// Generate a maze based on the instructions, given a fave_num
// Mark the END pos on the map for reference
vector<string> generate_maze(int fave_num, coord END)
{
	vector<string> maze(DIM, string(DIM, '.'));
	for (size_t i=0; i<DIM; i++)
	{
		for (size_t j=0; j<DIM; j++)
		{
			int num = formula(j, i) + fave_num;
			string b = to_binary_string(num);
			int num_ones = count(all(b), '1');
			maze[i][j] = ((num_ones&1) ? '#' : '.');

			if (i == END.y && j == END.x) maze[i][j] = 'O';
		}
	}
	return maze;
}

// Since the maze is unweighted, BFS will give optimal pathfinding results
int bfs(const vector<string> &maze, coord START, coord END)
{
	// Exploration order: Up, down, left, right
	int y_dir[] = {-1, 1, 0, 0};
	int x_dir[] = {0, 0, -1, 1};

	vector<coord> closed;
	vector<coord> fringe;
	fringe.push_back(START);

	while (!fringe.empty())
	{
		coord current = fringe.front();
		fringe.erase(fringe.begin());

		// Exit condition
		if (current == END)
		{
			// cout << "Found end!" << endl;
			// cout << current << endl;
			return current.num_steps;
		}

		// Each direction
		for (int i=0; i<4; i++)
		{
			int dX = current.x + x_dir[i];
			int dY = current.y + y_dir[i];
			if (dX < 0 || dX >= DIM || dY < 0 || dY >= DIM) continue;
			if (maze[dY][dX] == '#') continue;

			coord temp(dX, dY, current.num_steps+1);
			if (find(closed.begin(), closed.end(), temp) != closed.end()) continue;
			fringe.push_back(temp);
			closed.push_back(temp);
			// cerr << "Adding a thing" << endl;
		}
		if (find(closed.begin(), closed.end(), coord(current)) == closed.end())
			closed.push_back(current);

	}
	// cerr << "EXHAUSTED FRINGE!" << endl;
	return 99; // Cannot reach
}

int main()
{
	int input;
	cin >> input;
	coord START(1, 1);
	coord END(31, 39);
	// coord END(7, 4);
	vector<string> maze(generate_maze(input, END));
	for (size_t i=0; i<maze.size(); i++)
	{
		cout << maze[i] << endl;
	}

	// Part 1: How many steps from START to END
	cout << "Part 1: " << bfs(maze, START, END) << endl; 

	// Part 2: How many locations reachable from the start within 50 steps
	int num_reachable = 0;
	for (size_t i=0; i<maze.size(); i++)
	{
		for (size_t j=0; j<maze[i].size(); j++)
		{
			// Valid starting pos
			if (maze[i][j] == '.')
			{
				if (bfs(maze, coord(j,i), START) <= DIM)
				{
					num_reachable++;
				}
			}
		}
	}
	cout << "Part 2: " << num_reachable << endl;
}
