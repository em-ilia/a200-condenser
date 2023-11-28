# a200-condenser

This script takes a picklist and outputs one of three things:
1. An intermediate picklist to sort/condense a plate into an A200 compatible plate
2. The weird code the A200 wants
3. A list of wells where overlap occurred

<figure>
<img src="https://github.com/em-ilia/a200-condenser/assets/23224059/359317e2-d344-486f-b926-46dd44f14dad" width=100% alt="Image showing picklist output visualization">
  <p align="center">The picklist output visualized using <a href="https://github.com/em-ilia/plate-tool">plate-tool</a></p>
</figure>


## Input/Output Formats
### Command-line options
`main.py` expects the following arguments:
- `--colname-type`: The name of the column where types are found in the picklist (should be one of [A, B, C, D])
- `--colname-coord`: The name of the column where source well coordinates are found. This is probably `Source Well`.
- `inputfile`: Either a path to a picklist file (csv) or `-` if you want to pipe in through stdin (no idea if that works on Windows).

Optionally provide:
- `-t {a200,picklist,overlap}`: This allows you to select which output you want. It defaults to `a200` for the 2nd output listed above.

### Input files
As aforementioned, all that's required is for your picklist to have a column specifying a type
and a column with a source well coordinate.
The column with the type can **only** contain values [A, B, C, D].
If your picklist only has Destination Plates, you ought to be able to modify that column to satisfy
the requirement above.
For example, if you had racks labeled `Rxn1_RackX` where `X` is the type
```bash
cat picklist.csv | sed 's/Rxn1_Rack//' | python3 main.py --colname-type "Dest Plate" --colname-coord "Source Well" -
```

### Output files
By default, everything goes to stdout; you can decide where it goes from there.

The picklist is given as a CSV, with headers, which is very minimal by default;
you'll likely want some post processing.

The A200 string is printed with each string on its own line.

## Commentary too long for the source files
I've done my best to document the source files,
but there are sections that might need to be modified depending on usage.

### `main.py`
All input is handled by `argparse`, which is part of the Python standard library.
If you were always going to be running this the same way,
it would of course be possible to pass all arguments and read from `argv`.

The *only* output comes from the `print` statements in the match arms of `main()`.
If instead you needed to redirect this data to a file, you could do so here.

### `input.py`
Not much happens in this file, just CSV reading.
As long as `input_main()` returns a list of `(Type, Coordinate)` tuples,
it can be changed.

### `intermediate_picklist.py`
A few of the functions in this file were ripped from [plate-tool](https://github.com/em-ilia/plate-tool/blob/main/src/components/transfer_menu.rs)
and translated into Python.
A limitation carried over from that implementation is that `coords_to_excel_format` would roll over if a row greater than `ZZ` was used;
there is no such microplate in existence so this is a nonissue.

`transfers_to_picklist()` exists pretty much only to tack coordinates on to the existing tuple.

`convert_values_to_triple()` handles conversion of excel format (`B7`) coordinates to numbers.

You would be most likely to modify `transferlist_to_csv`.
If CSV modification outside of the script is not possible for you,
this is where the CSV is constructed.

### `a200_string.py`
This file really does very little.
The bit operations look complicated, but if you look at the alternative implementation at the bottom of the file,
it's clear that not much is going on.
We just need to keep track of if any well in a 4x1 block is being transferred to by the A200.
