from numpy import block
from entity import Entity
from game_map import GameMap
import unittest


class Test_Entity(unittest.TestCase):
    def test_init(self):
        '''
        tests initializing a new entity assigns values correctly
        '''
        x_val = 1
        y_val = 2
        char = '@'
        color = [100, 100, 100]
        name = 'nuzcraft'
        blocks_movement = True
        ent = Entity(x_val, y_val, char, color, name, blocks_movement)
        self.assertEqual(ent.x, x_val)
        self.assertEqual(ent.y, y_val)
        self.assertEqual(ent.char, char)
        self.assertEqual(ent.color, color)
        self.assertEqual(ent.name, name)
        self.assertEqual(ent.blocks_movement, blocks_movement)

    def test_spawn(self):
        '''
        tests that spawn will copy the entity
        '''
        gm = GameMap(10, 10, {})
        ent = Entity(name="test")
        ent.spawn(gm, 5, 5)
        # check that entities is filled with something
        self.assertTrue(gm.entities)
        # pull the entity out, make sure it matches as expected
        ents = gm.entities
        ent2 = list(ents)[0]
        self.assertEqual(ent2.name, "test")
        self.assertEqual(ent2.x, 5)
        self.assertEqual(ent2.y, 5)

    def test_move(self):
        '''
        tests moving an entity
        '''
        x_val = 1
        y_val = 2
        char = '@'
        color = [100, 100, 100]
        dx = 1
        dy = 2
        ent = Entity(x_val, y_val, char, color)
        ent.move(dx, dy)
        self.assertEqual(ent.x, x_val + dx)
        self.assertEqual(ent.y, y_val + dy)
