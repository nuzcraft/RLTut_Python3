from lib2to3.pytree import Base
import unittest

from components.ai import BaseAI
from entity import Entity

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

    def test_get_path_to(self):
        '''
        how should we test this function?
        let's do 3 tests
        1. test that it returns a short path in a straight line
        2. test that it avoids walls
        3. test that it avoids blocking entities
        we don't really want to test the pathfinder, just that it works
        with our walkable array + avoiding entities that block movement
        '''
