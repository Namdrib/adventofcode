#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

// http://adventofcode.com/2016/day/13

const int DIM = 50;

class Coord
{
public:
	Coord()
	{
		numSteps = 0;
	}
	Coord(int x, int y) : Coord()
	{
		this->x = x;
		this->y = y;
	}
	Coord(int x, int y, int numSteps) : Coord(x, y)
	{
		this->numSteps = numSteps;
	}
	
	friend ostream& operator << (ostream &os, Coord c)
	{
		os << "(" << c.x << "," << c.y << ") : " << c.numSteps;
		return os;
	}
	
	operator == (const Coord &rhs)
	{
		return (x == rhs.x && y == rhs.y);
	}
	
	int x;
	int y;
	int numSteps;
};

int formula(int x, int y)
{
	return x*x + 3*x + 2*x*y + y + y*y;
}

string toBinaryString(int n)
{
	string out;
	while (n >>= 1)
	{
		out = to_string(n&1) + out;
	}
	if (out.empty()) out = "0";
	return out;
}

// Generate a maze based on the instructions, given a faveNum
// Mark the END pos on the map for reference
vector<string> generateMaze(int faveNum, Coord END)
{
	vector<string> maze(DIM, string(DIM, '.'));
	for (size_t i=0; i<DIM; i++)
	{
		for (size_t j=0; j<DIM; j++)
		{
			int num = formula(j, i) + faveNum;
			string b = toBinaryString(num);
			int numOnes = count(b.begin(), b.end(), '1');
			maze[i][j] = ((numOnes&1) ? '#' : '.');
			
			if (i == END.y && j == END.x) maze[i][j] = 'O';
		}
	}
	return maze;
}

// Since the maze is unweighted, BFS will give optimal pathfinding results
int bfs(const vector<string> &maze, Coord START, Coord END)
{
	// Exploration order: Up, down, left, right
	int yDir[] = {-1, 1, 0, 0};
	int xDir[] = {0, 0, -1, 1};
	
	vector<Coord> closed;
	vector<Coord> fringe;
	fringe.push_back(START);
	
	while (!fringe.empty())
	{
		Coord current = fringe.front();
		fringe.erase(fringe.begin());
		
		// Exit condition
		if (current == END)
		{
			// cout << "Found end!" << endl;
			// cout << current << endl;
			return current.numSteps;
		}
		
		// Each direction
		for (int i=0; i<4; i++)
		{
			int dX = current.x + xDir[i];
			int dY = current.y + yDir[i];
			if (dX < 0 || dX >= DIM || dY < 0 || dY >= DIM) continue;
			if (maze[dY][dX] == '#') continue;
			
			Coord temp(dX, dY, current.numSteps+1);
			if (find(closed.begin(), closed.end(), temp) != closed.end()) continue;
			fringe.push_back(temp);
			closed.push_back(temp);
			// cerr << "Adding a thing" << endl;
		}
		if (find(closed.begin(), closed.end(), Coord(current)) == closed.end())
			closed.push_back(current);
		
	}
	// cerr << "EXHAUSTED FRINGE!" << endl;
	return 99; // Cannot reach
}

int main()
{
	Coord START(1, 1);
	Coord END(31, 39);
	// Coord END(7, 4);
	vector<string> maze(generateMaze(1350, END));
	for (size_t i=0; i<maze.size(); i++)
	{
		cout << maze[i] << endl;
	}
	
	// Part 1: How many steps from START to END
	cout << "Part 1: " << bfs(maze, START, END) << endl; 
	
	// Part 2: How many locations reachable from the start within 50 steps
	int numReachable = 0;
	for (size_t i=0; i<maze.size(); i++)
	{
		for (size_t j=0; j<maze[i].size(); j++)
		{
			// Valid starting pos
			if (maze[i][j] == '.')
			{
				if (bfs(maze, Coord(j,i), START) <= DIM)
				{
					numReachable++;
				}
			}
		}
	}
	cout << "Part 2: " << numReachable << endl;
}
