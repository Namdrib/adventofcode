#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2021/day/4

class bingo_board
{
public:
	vector<vector<int>> board;
	vector<vector<bool>> marks;

	bingo_board(const vector<vector<int>> &board)
	{
		// copy the board
		this->board = board;

		// blank out the marks with the same size as board
		marks = vector<vector<bool>>(board.size(), vector<bool>(board[0].size(), false));
	}

	// mark the number n on the board
	// assumes that the number n only appears once in the board
	void mark_num(int n)
	{
		for (size_t i = 0; i <board.size(); i++)
		{
			for (size_t j = 0; j < board[i].size(); j++)
			{
				if (board[i][j] == n)
				{
					marks[i][j] = true;
					return;
				}
			}
		}
	}

	bool check_board_win() const
	{
		// if any rows are all marked
		for (auto row : marks)
		{
			if (all_of(row.begin(), row.end(), [](bool b){return b == true;}))
			{
				return true;
			}
		}

		// if any columns are all marked
		for (size_t j = 0; j < board[0].size(); j++)
		{
			bool win = true;

			for (size_t i = 0; i < board.size(); i++)
			{
				if (!marks[i][j])
				{
					win = false;
					break;
				}
			}

			if (win)
			{
				return true;
			}
		}

		return false;
	}

	int get_sum_of_unmarked_numbers()
	{
		int sum = 0;
		for (size_t i = 0; i < board.size(); i++)
		{
			for (size_t j = 0; j < board[i].size(); j++)
			{
				if (!marks[i][j])
				{
					sum += board[i][j];
				}
			}
		}

		return sum;
	}

	friend ostream& operator << (ostream &os, const bingo_board &b)
	{
		for (size_t i = 0; i < b.board.size(); i++)
		{
			for (size_t j = 0; j < b.board[i].size(); j++)
			{
				os << (b.marks[i][j] ? "*" : "") << b.board[i][j] << (b.marks[i][j] ? "* " : " ");
			}
			if (i < b.board.size() - 1)
			{
				os << endl;
			}
		}
		return os;
	}

};


// find the first board to win
// mark off the numbers one by one until a win is found
int part_one(vector<bingo_board> boards, const vector<int> &numbers)
{
	for (auto n : numbers)
	{
		for (auto &b : boards)
		{
			b.mark_num(n);

			if (b.check_board_win())
			{
				int sum = b.get_sum_of_unmarked_numbers();
				int result = sum * n;
				return result;
			}
		}
	}

	return -1;
}

// find the last board to win
// mark off the numbers one by one until the last board wins
int part_two(vector<bingo_board> boards, const vector<int> &numbers)
{
	for (auto n : numbers)
	{
		for (auto &b : boards)
		{
			b.mark_num(n);

			if (all_of(boards.begin(), boards.end(),
						[](const bingo_board &board){return board.check_board_win();}))
			{
				int sum = b.get_sum_of_unmarked_numbers();
				int result = sum * n;
				return result;
			}
		}
	}

	return -1;
}

int main()
{
	// more complicated input parsing that the usual puzzle
	string s;
	getline(cin, s);
	vector<int> numbers = extract_nums_from<int>(s);
	vector<string> lines = split_istream_per_line(cin);

	vector<bingo_board> boards;

	// turn the lines into bingo boards
	vector<vector<int>> board_numbers;
	for (const auto &s : lines)
	{
		if (s.empty())
		{
			if (!board_numbers.empty())
			{
				boards.push_back(bingo_board(board_numbers));
			}
			board_numbers.clear();
		}
		else
		{
			vector<int> board_number_row = extract_nums_from<int>(s);
			board_numbers.push_back(board_number_row);
		}
	}
	boards.push_back(bingo_board(board_numbers));

	cout << "Part 1: " << part_one(boards, numbers) << endl;
	cout << "Part 2: " << part_two(boards, numbers) << endl;
}
