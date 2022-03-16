from lib2to3.pytree import Base
import unittest

from components.ai import BaseAI
from entity import Entity
from game_map import GameMap
from engine import Engine

class Test_BaseAI(unittest.TestCase):
    def test_perform(self):
        '''
        all perform of this AI will be handled
        elsewhere
        '''
        ent = Entity()
        ai = BaseAI(entity=ent)
        with self.assertRaises(NotImplementedError):
            ai.perform()

    def test_get_path_to_straight_line(self):
        '''
        how should we test this function?
        let's do 3 tests
        1. test that it returns a short path in a straight line
        2. test that it avoids walls
        3. test that it avoids blocking entities
        we don't really want to test the pathfinder, just that it works
        with our walkable array + avoiding entities that block movement
        '''
        ent = Entity()
        eng = Engine(player=ent)
        gm = GameMap(engine=eng, width=10, height=10)
        ent.gamemap = gm
        ai = BaseAI(entity=ent)
        path = ai.get_path_to(dest_x=0, dest_y=9)
        self.assertEqual(len(path), 300)

