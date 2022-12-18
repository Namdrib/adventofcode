#include "../../main/util/helpers.cpp"

void test_clamp()
{
	assert(clamp(-1, 0, 1) == 0);
	assert(clamp(0, 0, 1) == 0);
	assert(clamp(1, 0, 1) == 1);
	assert(clamp(2, 0, 1) == 1);
	assert(clamp(2, 1, 0) == 0);

	// being cheeky
	assert(clamp('a', 'b', 'z') == 'b');
}

void test_extract_nums_from()
{
	assert(extract_nums_from("1 2 3 4") == (vector<int>{1, 2, 3, 4}));
	assert(extract_nums_from("-1 2 -3 4") == (vector<int>{-1, 2, -3, 4}));
	assert(extract_nums_from("words with 2 numbers 1") == (vector<int>{2, 1}));
	assert(extract_nums_from("with negative -10 numbers") == (vector<int>{-10}));
	assert(extract_nums_from("false-negatives 10") == (vector<int>{10}));
	assert(extract_nums_from("no numbers") == (vector<int>{}));
	assert(extract_nums_from("") == (vector<int>{}));
	assert(extract_nums_from("no decimals 3.14") == (vector<int>{3, 14}));
	assert(extract_nums_from("no decimals -3.14") == (vector<int>{-3, 14}));
	assert(extract_nums_from("position=< 9,  1> velocity=< 0,  2>") == (vector<int>{9, 1, 0, 2})); // 2018 day 10
	assert(extract_nums_from("After:  [3, 2, 2, 1]") == (vector<int>{3, 2, 2, 1})); // 2018 day 16
	assert(extract_nums_from("x=498, y=2..4") == (vector<int>{498, 2, 4})); // 2018 day 17
}

void test_in_range()
{
	assert(in_range(1, 1, 1) == true);
	assert(in_range(2, 1, 2) == true);
	assert(in_range(2, 1, 2) == true);
	assert(in_range(3, 1, 2) == false);
	assert(in_range(-1, 1, 2) == false);
}

void test_in_bounds()
{
	vector<int> v(5);

	assert(in_bounds(v, -1) == false);
	for (int i = 0; i < 5; i++) {
		assert(in_bounds(v, i) == true);
	}
	for (int j = 5; j < 10; j++) {
		assert(in_bounds(v, j) == false);
	}

	v.resize(0);
	assert(in_bounds(v, 0) == false);
}

void test_roughly_equal()
{
	// TODO
}

int main()
{
	test_clamp();
	test_extract_nums_from();
	test_in_bounds();
	test_roughly_equal();
	cout << "Tests successful" << endl;
}
