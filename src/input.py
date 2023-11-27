# This file takes a CSV file with 96 rows (for each well) and extracts a value of A-D.

from main import ArgsStruct
import csv
import sys


def input_main(args: ArgsStruct) -> [(str, str)]:
    reader = csv.DictReader(args.input)
    rows = list(reader)

    if args.type_col_name not in rows[0]:
        sys.exit("Type column could not be found")
    if args.coord_col_name not in rows[0]:
        sys.exit("Coordinate column could not be found")

    values = list(
        map(lambda x: (x[args.type_col_name], x[args.coord_col_name]), rows))

    if not validate_values(values):
        sys.exit("CSV file contained invalid data")

    return values


def validate_values(values) -> bool:
    if not all(x[0] in ['A', 'B', 'C', 'D'] for x in values):
        print("An unexpected value was encountered", file=sys.stderr)
        return False

    return True
