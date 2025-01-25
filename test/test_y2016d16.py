from unittest import TestCase

from Solutions2016.y2016d16 import Solution_2016_16


class Test2016d16(TestCase):

    def test_do_one_round(self):
        self.assertEqual(Solution_2016_16.do_one_round("1"), "100")
        self.assertEqual(Solution_2016_16.do_one_round("0"), "001")
        self.assertEqual(Solution_2016_16.do_one_round("11111"), "11111000000")
        self.assertEqual(
            Solution_2016_16.do_one_round("111100001010"), "1111000010100101011110000"
        )
