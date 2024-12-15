#!/usr/bin/python

from jinja2 import Environment, FileSystemLoader

import argparse

from datetime import datetime
import os

def argparse_setup():
    parser = argparse.ArgumentParser(
       description="Create a python day code file out of a Jinja template"
    )

    parser.add_argument(
        '-y', '--year',
        default=datetime.now().year,
        type=int,
        help='The year of the AoC python file to create'
    )

    parser.add_argument(
        '-d', '--day',
        default=datetime.now().day,
        type=int,
        help='The day of the AoC python file to create'
    )

    parser.add_argument(
        '-t', '--test-file',
        action='store_true',
        help='Create empty test files (does nothing if they already exist)'
    )

    parser.add_argument(
        '-n', '--no-action',
        action='store_true',
        help='Take no action (do a dry-run) (NOT IMPLEMENTED YET)'
    )

    return parser

def pad_day(day: int) -> str:
    return str(day).rjust(2, '0')

def generate_test_files(year: int, day: int) -> None:
    """
    Create empty test files that match the given year and date

    :param year: The year of the file to create
    :type year: int
    :param day: The day of the file to create
    :type day: int
    """
    test_dir: str = f'src/test/_{year}'
    if not os.path.exists(test_dir):
        print(f'Creating directory {test_dir}')
        os.mkdir(test_dir)

    # Create test files if they don't exist
    # The actual input (e.g. day01_00.in)
    test_file: str = f'{test_dir}/day{pad_day(day)}_{pad_day(0)}.in'
    if os.path.isfile(test_file):
        print(f'The test file {test_file} already exists')
    else:
        print(f'Creating test file {test_file}')
        open(test_file, 'w', encoding='utf-8').close()

    # The first sample input (e.g. day01_01.in)
    test_file: str = f'{test_dir}/day{pad_day(day)}_{pad_day(1)}.in'
    if os.path.isfile(test_file):
        print(f'The test file {test_file} already exists')
    else:
        print(f'Creating test file {test_file}')
        open(test_file, 'w', encoding='utf-8').close()

def generate_source_file(template, year: int, day: int) -> None:
    """
    Create the specified python source file out of a Jinja2 template

    Create leading directories if they don't exist

    :param template: A Jinja2 template object
    :type template: _type_
    :param year: The year of the file to create
    :type year: int
    :param day: The day of the file to create
    :type day: int
    """
    src_dir: str = f'src/main/_{year}'
    # Create the dir if it doesn't exist
    if not os.path.exists(src_dir):
        print(f'Creating directory {src_dir}')
        os.mkdir(src_dir)

    src_file: str = f'{src_dir}/day{pad_day(day)}.py'
    # Do nothing if the file exists
    if os.path.isfile(src_file):
        print(f'The file {src_file} already exists')
    else:
        # Render the template into the file (e.g. day01.py)
        print(f'Creating source file {src_file}')
        with open(src_file, 'w', encoding='utf-8') as f:
            print(template.render(year=year, day=day, day_padded=pad_day(day)), file=f)

def main():

    parser = argparse_setup()
    args = parser.parse_args()

    env = Environment(loader=FileSystemLoader('src/main/template'))
    template = env.get_template('day.py.j2')

    generate_source_file(template, args.year, args.day)

    if args.test_file:
        generate_test_files(args.year, args.day)

if __name__ == '__main__':
    main()
