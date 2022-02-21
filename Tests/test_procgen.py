import unittest
from procgen import RectangularRoom


class Test_RectangularRoom(unittest.TestCase):
    def test_init(self):
        x, y, w, h = 5, 6, 7, 8
        rm = RectangularRoom(x, y, w, h)
        self.assertEqual(rm.x1, x)
        self.assertEqual(rm.x2, x+w)
        self.assertEqual(rm.y1, y)
        self.assertEqual(rm.y2, y+h)

    def test_center_odd_sides(self):
        x, y, w, h = 0, 0, 5, 5
        rm = RectangularRoom(x, y, w, h)
        # int will cut off the decimals
        # 5/2 = 2.5 = 2
        c_x, c_y = 2, 2
        self.assertEqual(rm.center[0], c_x)
        self.assertEqual(rm.center[1], c_y)

    def test_center_even_sides(self):
        x, y, w, h = 0, 0, 6, 6
        rm = RectangularRoom(x, y, w, h)
        # int() will cut off the decimals
        # 6/2 = 3
        c_x, c_y = 3, 3
        self.assertEqual(rm.center[0], c_x)
        self.assertEqual(rm.center[1], c_y)

    def test_inner(self):
        x, y, w, h = 0, 0, 6, 6
        rm = RectangularRoom(x, y, w, h)
        # inner will return a tuple of slices
        # which excludes the lower bound
        self.assertEqual(rm.inner[0], slice(x+1, x+w))
        self.assertEqual(rm.inner[1], slice(y+1, y+h))
