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
