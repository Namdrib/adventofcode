#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2019/day/8

// return number of occurrences of n in a 2d vector
int num_n_in_layer(const vector<vector<int>> &layer, int n)
{
	return accumulate(all(layer), 0, [n](int base, vector<int> v){
		return base + count(all(v), n);
	});
}

int solve(const string &s, bool part_two = false)
{
	vector<vector<vector<int>>> layers;

	const size_t width = 25;
	const size_t height = 6;
	const size_t depth = s.size() / (width * height);

	// build the layers of pixels
	// i is layer number
	int pixel_num = 0;
	for (size_t i = 0; i < depth; i++)
	{
		vector<vector<int>> layer;

		for (size_t j = 0; j < height; j++)
		{
			vector<int> row;
			for (size_t k = 0; k < width; k++)
			{
				row.push_back(s[pixel_num] - '0');

				pixel_num++;
			}
			layer.push_back(row);
		}

		layers.push_back(layer);
	}

	if (part_two)
	{
		// 0 is black
		// 1 is white
		// 2 is transparent

		// for all layer positions
		// if layer[i][j] is transparent, look at the next layer[i][j]
		vector<vector<int>> final_image;
		for (size_t i = 0; i < height; i++)
		{
			vector<int> row;
			for (size_t j = 0; j < width; j++)
			{
				for (const auto &layer : layers)
				{
					if (layer[i][j] != 2)
					{
						row.push_back(layer[i][j]);
						break;
					}
				}
			}
			final_image.push_back(row);
		}

		// pretty print final_image
		for (const auto &row : final_image)
		{
			for_each(all(row), [](int pixel){
				cout << (pixel == 1 ? '1' : ' ');
			});
			cout << endl;
		}
		return 0;
	}
	else
	{
		// Find the layer with min zeros
		auto min_zero_layer = *min_element(all(layers),
			[](vector<vector<int>> left, vector<vector<int>> right){
				return num_n_in_layer(left, 0) < num_n_in_layer(right, 0);
			}
		);
		int num_ones = num_n_in_layer(min_zero_layer, 1);
		int num_twos = num_n_in_layer(min_zero_layer, 2);

		return num_ones * num_twos;
	}

	return 0;
}

int main()
{
	string s;
	getline(cin, s);

	cout << "Part 1: " << solve(s, false) << endl;
	cout << "Part 2: " << endl;
	solve(s, true);
}
