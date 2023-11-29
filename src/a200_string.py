# The a200 wants a sequence of 8x12 bits,
# formatted in a weird string of hexadecimal digits.
# This string looks like:
# nnn,nnn,nnn,nnn,nnn,nnn,nnn,nnn

from intermediate_picklist import TransferList


def transferlist_to_a200_strings(tl: TransferList) -> [str]:
    grids = []
    for type in ['A', 'B', 'C', 'D']:
        filtered = list(filter(lambda x: x[0] == type, tl))

        # We can look at the plate as a 2x12 grid,
        # representable in 3 bytes

        grid = bytearray(3)

        # If you look at this approach and say,
        # "this is too complicated", I would agree.
        # I was moderately worried about just using [bool; 24]
        # for performance reasons, but that may have been better.

        for well in filtered:
            row = well[3]
            col = well[4]

            # Map coordinate to the 2x12 block
            bit_number = col + (row // 4) * 12

            # First, access the byte where the bit is located
            # Then, left shift 1 to the appropriate position in the bytes
            # and or-assign; this sets the bit to one.
            # We subtract from 7 so that the order of the bits is reversed
            grid[bit_number // 8] |= 1 << (7 - bit_number % 8)

        grids.append(grid)

    # We want to combine the A,B,C grids via bitwise or:
    abc_grid = bytearray(
        [x | y | z for (x, y, z) in zip(grids[0], grids[1], grids[2])])

    # If your plate is full (i.e. every well will then be touched by the a200)
    # then you should be able to verify that A|B|C|D is 8 x 0xFFF

    return [bytes_to_a200_string(abc_grid), bytes_to_a200_string(grids[3])]


def bytes_to_a200_string(b: bytearray) -> str:
    # Grab the first byte and move it over 4 bits
    # so that we have 0bNNNNNNNN0000, then
    # grab the second byte and truncate the 4 least significant bits.
    # Then or these to get a 12 bit result.
    n1 = b[0] << 4 | (b[1] >> 4)
    # Grab the second bit and mask with 0b00001111 to get the four least
    # significant bits, then shift 8 bits to the left and
    # or with the third bit.
    n2 = (b[1] & 0x0f) << 8 | b[2]

    strs = [f'{n1:03x}'] * 4 + [f'{n2:03x}'] * 4

    return ','.join(strs)


"""Alternative (psuedocode) implementation for above functions

...
grid = [False] * 24

for well in filtered:
    row = well[3]
    col = well[4]

    i = col + (row // 4) * 12
    grid[i] |= True

...
n = bool_array_to_int(grid[0:13])
...
"""


def pretty_print_a200_string(s: str) -> None:
    # First convert the string back into bits and all
    # First split s at commas
    # Then convert each string into an int
    # The get the binary representation as a string
    # Then convert the string into a list of characters
    cols = [format(int(x, base=16), '012b') for x in s.split(',')]

    for row in cols:
        print(row)
