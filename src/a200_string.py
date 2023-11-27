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

        for well in filtered:
            row = well[3]
            col = well[4]

            bit_number = col + (row // 4) * 8

            grid[bit_number // 8] |= 1 << (bit_number % 8)

        out_strs = []
        for row in range(4):
            n = grid[0] << 4 | (grid[1] >> 4)
            out_strs.append(f'{n:03x}')
        for row in range(4):
            n = (grid[1] & 0x0f) << 8 | grid[2]
            out_strs.append(f'{n:03x}')

        out.append(','.join(out_strs))

    return out
