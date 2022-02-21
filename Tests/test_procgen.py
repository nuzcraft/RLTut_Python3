import unittest
from procgen import RectangularRoom, generate_dungeon


class Test_RectangularRoom(unittest.TestCase):
    def test_init(self):
        '''
        test instantiation of a rectangle
        '''
        x, y, w, h = 5, 6, 7, 8
        rm = RectangularRoom(x, y, w, h)
        self.assertEqual(rm.x1, x)
        self.assertEqual(rm.x2, x+w)
        self.assertEqual(rm.y1, y)
        self.assertEqual(rm.y2, y+h)

    def test_center_odd_sides(self):
        '''
        tests that the center property returns correctly for odd sides
        '''
        x, y, w, h = 0, 0, 5, 5
        rm = RectangularRoom(x, y, w, h)
        # int will cut off the decimals
        # 5/2 = 2.5 = 2
        c_x, c_y = 2, 2
        self.assertEqual(rm.center[0], c_x)
        self.assertEqual(rm.center[1], c_y)

    def test_center_even_sides(self):
        '''
        tests that the center property returns correctly for even sides
        '''
        x, y, w, h = 0, 0, 6, 6
        rm = RectangularRoom(x, y, w, h)
        # int() will cut off the decimals
        # 6/2 = 3
        c_x, c_y = 3, 3
        self.assertEqual(rm.center[0], c_x)
        self.assertEqual(rm.center[1], c_y)

    def test_inner(self):
        '''
        tests that the inner property returns correctly
        '''
        x, y, w, h = 0, 0, 6, 6
        rm = RectangularRoom(x, y, w, h)
        # inner will return a tuple of slices
        # which excludes the lower bound
        self.assertEqual(rm.inner[0], slice(1, 6))
        self.assertEqual(rm.inner[1], slice(1, 6))


class Test_Generate_Dungeon(unittest.TestCase):
    def test_generate_dungeon(self):
        '''
        tests that generate_dungeon returns a map of the correct size
        we don't care what the dungeon looks like, but this should test
        calling it doesn't cause an error or misshape the result
        '''
        d = generate_dungeon(50, 50)
        self.assertEqual(d.height, 50)
        self.assertEqual(d.width, 50)
