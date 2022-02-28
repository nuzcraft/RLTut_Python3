import unittest
from game_map import GameMap
from entity import Entity


class Test_Game_Map(unittest.TestCase):
    def test_init(self):
        '''
        tests instantiating a new GameMap
        '''
        ent1 = Entity(x=10, y=10, char="@", color=(100, 100, 100))
        ent2 = Entity(x=20, y=20, char="k", color=(200, 200, 200))
        gm = GameMap(width=50, height=60, entities={ent1, ent2})
        self.assertEqual(gm.width, 50)
        self.assertEqual(gm.height, 60)
        # check that tiles were generated okay
        tiles_shape = gm.tiles.shape
        self.assertEqual(tiles_shape[0], 50)
        self.assertEqual(tiles_shape[1], 60)
        # check that the visible and explored arrays were generated okay as well
        visible_shape = gm.visible.shape
        self.assertEqual(visible_shape[0], 50)
        self.assertEqual(visible_shape[1], 60)
        explored_shape = gm.explored.shape
        self.assertEqual(explored_shape[0], 50)
        self.assertEqual(explored_shape[1], 60)
        # check that the entities set was created
        self.assertIn(ent1, gm.entities)
        self.assertIn(ent2, gm.entities)

    def test_in_bounds_both_in(self):
        '''
        tests whether x and y in bounds of map returns true
        '''
        x, y = 25, 25
        gm = GameMap(50, 50)
        self.assertTrue(gm.in_bounds(x, y))

    def test_in_bounds_both_out_low(self):
        '''
        tests whether x and y both out of bounds with low values returns false
        '''
        x, y = -1, -1
        gm = GameMap(50, 50)
        self.assertFalse(gm.in_bounds(x, y))

    def test_in_bounds_both_out_high(self):
        '''
        tests whether x and y both out of bounds high values returns false
        '''
        x, y = 100, 100
        gm = GameMap(50, 50)
        self.assertFalse(gm.in_bounds(x, y))

    def test_in_bounds_x_in_y_out(self):
        '''
        tests x in bounds, y out of bounds returns false
        '''
        x, y = 25, 100
        gm = GameMap(50, 50)
        self.assertFalse(gm.in_bounds(x, y))

    def test_in_bounds_x_out_y_in(self):
        '''
        tests x out of bounds, y in bounds returns false
        '''
        x, y = -25, 25
        gm = GameMap(50, 50)
        self.assertFalse(gm.in_bounds(x, y))

    # def test_render(self):
    #     '''
    #     tests that on render the console matches the GameMap
    #     removing this test until there's something easier to test
    #     '''
    #     gm = GameMap(50, 50)
    #     console = tcod.Console(50, 50)
    #     gm.render(console)
    #     # let's check the specific locations in console to make
    #     # sure they match the game map
    #     self.assertEqual(console.tiles_rgb[29, 22], gm.tiles[29, 22]["dark"])
    #     self.assertEqual(console.tiles_rgb[30, 22], gm.tiles[30, 22]["dark"])
