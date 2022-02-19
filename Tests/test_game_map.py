import unittest
from game_map import GameMap
import tcod
import tile_types


class Test_Game_Map(unittest.TestCase):
    def test_init(self):
        gm = GameMap(50, 60)
        self.assertEqual(gm.width, 50)
        self.assertEqual(gm.height, 60)
        # check that tiles were generated okay
        tileshape = gm.tiles.shape
        self.assertEqual(tileshape[0], 50)
        self.assertEqual(tileshape[1], 60)
        # initial creation puts a floor here
        self.assertEqual(gm.tiles[29, 22], tile_types.floor)
        # initial creation puts a wall here
        self.assertEqual(gm.tiles[30, 22], tile_types.wall)

    def test_in_bounds_both_in(self):
        x, y = 25, 25
        gm = GameMap(50, 50)
        self.assertTrue(gm.in_bounds(x, y))

    def test_in_bounds_both_out_low(self):
        x, y = -1, -1
        gm = GameMap(50, 50)
        self.assertFalse(gm.in_bounds(x, y))

    def test_in_bounds_both_out_high(self):
        x, y = 100, 100
        gm = GameMap(50, 50)
        self.assertFalse(gm.in_bounds(x, y))

    def test_in_bounds_x_in_y_out(self):
        x, y = 25, 100
        gm = GameMap(50, 50)
        self.assertFalse(gm.in_bounds(x, y))

    def test_in_bounds_x_out_y_in(self):
        x, y = -25, 25
        gm = GameMap(50, 50)
        self.assertFalse(gm.in_bounds(x, y))

    def test_render(self):
        gm = GameMap(50, 50)
        console = tcod.Console(50, 50)
        gm.render(console)
        # let's check the specific locations in console to make
        # sure they match the game map
        self.assertEqual(console.tiles_rgb[29, 22], gm.tiles[29, 22]["dark"])
        self.assertEqual(console.tiles_rgb[30, 22], gm.tiles[30, 22]["dark"])
