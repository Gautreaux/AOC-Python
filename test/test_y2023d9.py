from unittest import TestCase

from Solutions2023.y2023d9 import OasisHistory


class Test2023d9(TestCase):
    """Test cases related to y2023d09 solutions"""

    def test_oaisis_extrapolate(self):
        """Test the OasisHistory._extrapolate method"""
        r = OasisHistory._extrapolate((0, 0))
        self.assertEqual(len(r), 3)
        self.assertEqual(r, (0, 0, 0))

        r = OasisHistory._extrapolate((3, 3, 3, 3, 3))
        self.assertEqual(len(r), 6)
        self.assertEqual(r, (3, 3, 3, 3, 3, 3))

        r = OasisHistory._extrapolate((0, 3, 6, 9, 12, 15))
        self.assertEqual(len(r), 7)
        self.assertEqual(r, (0, 3, 6, 9, 12, 15, 18))

        r = OasisHistory._extrapolate((1, 3, 6, 10, 15, 21))
        self.assertEqual(len(r), 7)
        self.assertEqual(r, (1, 3, 6, 10, 15, 21, 28))

        r = OasisHistory._extrapolate((10, 13, 16, 21, 30, 45))
        self.assertEqual(len(r), 7)
        self.assertEqual(r, (10, 13, 16, 21, 30, 45, 68))

    def test_oaisis_extrapolate_backwards(self):
        """Test the OasisHistory._extrapolate_backwards method"""
        r = OasisHistory._extrapolate_backwards((0, 0))
        self.assertEqual(len(r), 3)
        self.assertEqual(r, (0, 0, 0))

        r = OasisHistory._extrapolate_backwards((0, 3, 6, 9, 12, 15))
        self.assertEqual(len(r), 7)
        self.assertEqual(r, (-3, 0, 3, 6, 9, 12, 15))

        r = OasisHistory._extrapolate_backwards((1, 3, 6, 10, 15, 21))
        self.assertEqual(len(r), 7)
        self.assertEqual(r, (0, 1, 3, 6, 10, 15, 21))

        r = OasisHistory._extrapolate_backwards((10, 13, 16, 21, 30, 45))
        self.assertEqual(len(r), 7)
        self.assertEqual(r, (5, 10, 13, 16, 21, 30, 45))
