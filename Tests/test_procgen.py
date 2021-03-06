import unittest
from procgen import (
    RectangularRoom,
    generate_dungeon,
    tunnel_between,
    place_entities,
    get_max_value_for_floor,
)
from entity import Entity
from engine import Engine
from game_map import GameWorld


class TestMaxValue(unittest.TestCase):
    def test_get_max_value_for_floor_on_floor(self):
        '''
        test that passing in a matching floor will return 
        the exact match for the value associated with that floor
        '''
        weighted_chances = [
            (1, 2),
            (4, 3),
            (6, 5),
        ]
        ret = get_max_value_for_floor(
            weighted_chances_by_floor=weighted_chances,
            floor=4
        )
        self.assertEqual(ret, 3)

    def test_get_max_value_for_floor_between_floors(self):
        '''
        test that passing in a not matching floor will return 
        the match for the value associated with the lower floor
        '''
        weighted_chances = [
            (1, 2),
            (4, 3),
            (6, 5),
        ]
        ret = get_max_value_for_floor(
            weighted_chances_by_floor=weighted_chances,
            floor=3
        )
        self.assertEqual(ret, 2)


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

    def test_intersect_true(self):
        '''
        test that two intersecting rooms return true 
        '''
        x, y, w, h = 0, 0, 6, 6
        x2, y2, w2, h2 = 1, 1, 7, 7
        rm = RectangularRoom(x, y, w, h)
        rm2 = RectangularRoom(x2, y2, w2, h2)
        self.assertTrue(rm.intersects(rm2))

    def test_intersect_false(self):
        '''
        test that two non-intersecting rooms return false
        '''
        x, y, w, h = 0, 0, 3, 3
        x2, y2, w2, h2 = 4, 4, 7, 7
        rm = RectangularRoom(x, y, w, h)
        rm2 = RectangularRoom(x2, y2, w2, h2)
        self.assertFalse(rm.intersects(rm2))


class Test_Generate_Dungeon(unittest.TestCase):
    def test_generate_dungeon(self):
        '''
        tests that generate_dungeon returns a map of the correct size
        we don't care what the dungeon looks like, but this should test
        calling it doesn't cause an error or misshape the result
        '''
        ent = Entity()
        eng = Engine(player=ent)
        eng.game_world = GameWorld(
            engine=eng,
            map_width=50,
            map_height=50,
            max_rooms=10,
            room_min_size=3,
            room_max_size=5,
            current_floor=1
        )
        d = generate_dungeon(
            max_rooms=10,
            room_min_size=3,
            room_max_size=5,
            map_width=50,
            map_height=50,
            engine=eng
        )
        self.assertEqual(d.height, 50)
        self.assertEqual(d.width, 50)


class Test_Tunnel_Between(unittest.TestCase):
    def test_tunnel_between(self):
        '''
        test that a tunnel between two points will return a continuous
        list of points. Each point should be 1 point away from the previous point
        '''
        x_s, y_s = 1, 2
        x_t, y_t = x_s, y_s
        x_e, y_e = 7, 8
        t = tunnel_between((x_s, y_s), (x_e, y_e))
        for x, y in t:
            # dist between entries in the tunnel should always be less than 1
            dist = abs((x_t-x) + (y_t-y))
            self.assertLessEqual(dist, 1)
            # set the transitory x so the next entry is only 1 space away
            x_t, y_t = x, y


# class Test_Place_Entities(unittest.TestCase):
#     def test_place_entities(self):
#         '''
#         test that placing entities call the code that places entities
#         '''
#         x, y, w, h = 0, 0, 10, 10
#         rm = RectangularRoom(x, y, w, h)
#         d = GameMap(10, 10, {})
