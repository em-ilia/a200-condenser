# The a200 wants a sequence of 8x12 bits,
# formatted in a weird string of hexadecimal digits.
# This string looks like:
# nnn,nnn,nnn,nnn,nnn,nnn,nnn,nnn

from intermediate_picklist import TransferList


def transferlist_to_a200_strings(tl: TransferList) -> [str]:
    out = []
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
            bit_number = col + (row // 4) * 8

            # First, access the byte where the bit is located
            # Then, left shift 1 to the appropriate position in the bytes
            # and or-assign; this sets the bit to one.
            grid[bit_number // 8] |= 1 << (bit_number % 8)

        out_strs = []
        for row in range(4):
            # Grab the first byte and move it over 4 bits
            # so that we have 0bNNNNNNNN0000, then
            # grab the second byte and truncate the 4 least significant bits.
            # Then or these to get a 12 bit result.
            n = grid[0] << 4 | (grid[1] >> 4)
            out_strs.append(f'{n:03x}')
        for row in range(4):
            # Grab the second bit and mask with 0b00001111 to get the four least
            # significant bits, then shift 8 bits to the left and
            # or with the third bit.
            n = (grid[1] & 0x0f) << 8 | grid[2]
            out_strs.append(f'{n:03x}')

        out.append(','.join(out_strs))

    return out


"""Alternative (psuedocode) implementation for above function

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
