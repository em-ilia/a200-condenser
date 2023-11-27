# This file builds a picklist to compact the wells from the given plate
from typing import Union, Tuple, List
import csv
import io
import sys
import re

# Should get the `type` keyword in python 3.12
# (Type, Row, Col, Row, Col)
TransferList = List[Tuple[str, int, int, int, int]]

_EXCEL_REGEX = re.compile(r"([A-Z]+)(\d+)")


def generate_intermediate_picklist(wells: [(str, str)]
                                   ) -> TransferList:
    """ Takes a list of wells and compacts them

    The return type of this function is not immediately useful.
    It should be passed to either `transferlist_to_csv` or
    a function in the `a200_string` module.

    Packing is achieved by filling columns, skipping space
    when necessary (see the while loop near the end of the function).
    """
    triples = convert_values_to_triple(wells)

    # Note: this transfer list is transposed!
    # That is, we're scanning top-to-bottom left-to-right.
    # This is because the a200 dispenses in
    # a vertically oriented tetris piece shape.
    transfers: list[(str, int, int) | None] = []

    for type in ['A', 'B', 'C', 'D']:
        # Filter so that we only deal with one type of well at a time
        filtered = list(filter(lambda well: well[0] == type, triples))

        # Add all of these wells into the transfer list
        for filtered_well in filtered:
            transfers.append(filtered_well)

        # The a200 *must* dispense into blocks of four.
        # As a result, we have to leave some wells empty.
        while len(transfers) % 4 != 0:
            transfers.append(None)

    if len(transfers) > 96:
        sys.exit("Cannot fit all wells in a single 96 well plate")

    return transfers_to_picklist(transfers)


def transferlist_to_csv(tl: TransferList) -> str:
    """ Takes a transfer list and yields a string of a csv pick list.

    Note: I include the field `Type` so that you can verify that this
    does indeed produce a plate of the desired layout.
    Your liquid handler (Fluent) might hate this!
    Nothing bad will happen if you remove this; just delete the
    `'Type'` part of the line marked # Header row
    and the entry `transfer[0]` from the call marked
    # Content rows.

    You may also need to insert other information into the picklist csv.
    You could either modify this script, or make a secondary script
    to play with the csv.
    """
    out = io.StringIO()

    writer = csv.writer(out, delimiter=',')

    writer.writerow(['Source Well', 'Destination Well', 'Type'])  # Header row
    for transfer in tl:
        source_well = coords_to_excel_format((transfer[1], transfer[2]))
        dest_well = coords_to_excel_format((transfer[3], transfer[4]))
        writer.writerow(  # Content rows
            [source_well,
             dest_well,
             transfer[0]]
        )

    return out.getvalue()


def coords_to_excel_format(coords: (int, int)) -> str:
    # Conversion method ripped from plate-tool/transfer_menu.rs
    # and translated to python.

    col = coords[1] + 1  # Switch from zero indexing to one indexing

    row = ""
    digit1 = (coords[0]+1) // 26
    digit2 = (coords[0]+1) % 26
    if digit1 > 0 and digit2 == 0:
        digit1 = digit1 - 1
        digit2 = 26
    if digit1 != 0:
        row += chr(64 + digit1)
    row += chr(64+digit2)

    return row + str(col)


def convert_values_to_triple(wells: [(str, str)]) -> [(str, int, int)]:
    """Reads the excel format coordinate and converts
    to row,col.
    """
    def letters_to_num(letters: str) -> int:
        # Stolen with love from `plate-tool` (`transfer_menu.rs`)
        num = 0
        for (i, letter) in enumerate(reversed(letters.upper())):
            n = ord(letter)
            if n not in range(65, 91):
                sys.exit("Error parsing coordinates")
            num += pow(26, i) * (n - 64)

        return num

    def excel_to_coords(value: str) -> (int, int):
        # Adapted from `plate-tool` (`transfer_menu.rs`)

        captures = _EXCEL_REGEX.match(value)
        if captures is not None and len(captures.groups()) == 2:
            letters = captures.groups()[0]
            numbers = captures.groups()[1]

            return (letters_to_num(letters), numbers)
        else:
            sys.exit("Error parsing coordinates")

    return list(
        # In lambda below, `x` is a tuple (index, value)
        map(lambda x: (x[0], *excel_to_coords(x[1])), wells)
    )


def transfers_to_picklist(transfers: [Union[Tuple[str, int, int], None]]
                          ) -> TransferList:
    # Type hinting here is obnoxious because writing it
    # as I did elsewhere yielded a TypeError;
    # I have no idea why.

    # Conversion function yields well coordinates given
    # the index of the transfer.
    def order_to_coord(i): return (i % 8, i // 8)

    output = []
    for (i, transfer) in enumerate(transfers):
        if transfer is None:  # We can just skip blank wells
            continue
        # Unpack the well info (transfer) and tack on the new coordinates
        output.append((*transfer, *order_to_coord(i)))

    return output
