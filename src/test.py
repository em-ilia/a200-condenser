import unittest

import a200_string

class TestA200String(unittest.TestCase):
    def test_transferlist_to_a200_strings(self):
        tl = [
            ('A', 0, 0, 0, 0),  # 1st bit is 1
            ('A', 0, 0, 1, 0),  # No effect
            ('A', 0, 0, 0, 3),  # 4th bit is 1
            ('A', 0, 0, 4, 3),  # (12+4th) bit is 1
        ]

        res = a200_string.transferlist_to_a200_strings(tl)

        self.assertEqual(res[0], "900,900,900,900,100,100,100,100")
