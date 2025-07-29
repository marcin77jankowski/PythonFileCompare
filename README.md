# PythonFileCompare

This project provides a Python script to compare two CSV files with the same structure. You can specify join columns and columns to exclude from comparison. The script returns information about the similarity of the two files.

## Usage
- Run the script with two CSV file paths as arguments.
- Specify join columns and columns to exclude from comparison.

## Features
- Compares two CSV files row-by-row using join columns.
- Excludes specified columns from comparison.
- Outputs similarity statistics.

## Requirements
- Python 3.7+
- pandas

## How to run
1. Install dependencies: `pip install pandas`
2. Run the script: `python compare_csv.py file1.csv file2.csv --join-cols col1,col2 --exclude-cols col3,col4`

## License
MIT
