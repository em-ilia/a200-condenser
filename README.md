# a200-condenser

This script takes a picklist and outputs one of three things:
1. An intermediate picklist to sort/condense a plate into an A200 compatible plate
2. The weird code the A200 wants
3. A list of wells where overlap occurred (not implemented yet)

## Input/Output Formats
### Command-line options
`main.py` expects the following arguments:
- `--colname-type`: The name of the column where types are found in the picklist (should be one of [A, B, C, D])
- `--colname-coord`: The name of the column where source well coordinates are found. This is probably `Source Well`.
- `inputfile`: Either a path to a picklist file (csv) or `-` if you want to pipe in through stdin (no idea if that works on Windows).

Optionally provide:
- `-t {a200,picklist}`: This allows you to select which output you want. It defaults to `a200` for the 2nd output listed above.

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
