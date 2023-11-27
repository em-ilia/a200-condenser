# See README.md for extended rambling about this script
# tl;dr : I don't have access to APIs so something will have
# to be changed to accomodate your workflow, but I'll do my best
# to explain it all.

import argparse
import sys
from dataclasses import dataclass

import input
import intermediate_picklist
import a200_string


def main():
    args = process_arguments()

    wells = input.input_main(args)

    picklist = intermediate_picklist.generate_intermediate_picklist(wells)

    print(args.output_type)
    match args.output_type:
        case "a200":
            print(a200_string.transferlist_to_a200_strings(picklist))
        case "picklist":
            print(intermediate_picklist.transferlist_to_csv(picklist))
        case _:
            sys.exit("Unreachable case reached.")


@dataclass
class ArgsStruct:
    input: argparse.FileType
    input_col_name: str
    output_type: str


def process_arguments():
    parser = argparse.ArgumentParser(
        prog='a200 condenser',
        description=('Generate a picklist to condense a plate'
                     ' and then the weird string the a200 wants'),
    )

    parser.add_argument('inputfile',
                        type=argparse.FileType('r'),
                        nargs='?',
                        help='File to read as an input plate; should be CSV.',
                        )
    parser.add_argument('--colname',
                        type=str,
                        required=False,
                        default="reactionType"  # I really have no idea what should be here!
                        )
    parser.add_argument('-t', '--output-type',
                        choices=['a200', 'picklist'],
                        default='a200')

    args = parser.parse_args()

    if not args.inputfile:
        sys.exit(('An input file is needed either'
                 ' as a path or piped in through stdin'))

    return ArgsStruct(input=args.inputfile, input_col_name=args.colname,
                      output_type=args.output_type)


if __name__ == "__main__":
    main()