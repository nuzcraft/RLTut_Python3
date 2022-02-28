import unittest
import tile_types


class Test_Tile_Types(unittest.TestCase):
    def test_new_tile(self):
        '''
        test initializing a new tile
        '''
        tile = tile_types.new_tile(
            walkable=True,
            transparent=True,
            dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
            light=(ord("a"), (0, 0, 0), (100, 100, 100)),
        )
        self.assertEqual(tile["walkable"], True)
        self.assertEqual(tile["transparent"], True)
        self.assertEqual(tile["dark"]["ch"], ord(" "))
        self.assertEqual(tile["dark"]["fg"][0], 255)
        self.assertEqual(tile["dark"]["fg"][1], 255)
        self.assertEqual(tile["dark"]["fg"][2], 255)
        self.assertEqual(tile["dark"]["bg"][0], 50)
        self.assertEqual(tile["dark"]["bg"][1], 50)
        self.assertEqual(tile["dark"]["bg"][2], 150)
        self.assertEqual(tile["light"]["ch"], ord("a"))
        self.assertEqual(tile["light"]["fg"][0], 0)
        self.assertEqual(tile["light"]["fg"][1], 0)
        self.assertEqual(tile["light"]["fg"][2], 0)
        self.assertEqual(tile["light"]["bg"][0], 100)
        self.assertEqual(tile["light"]["bg"][1], 100)
        self.assertEqual(tile["light"]["bg"][2], 100)
