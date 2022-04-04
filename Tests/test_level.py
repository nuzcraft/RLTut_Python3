import unittest

from components.level import Level

class TestLevel(unittest.TestCase):
    def test_init(self):
        '''
        test that a Level can be initialized correctly
        '''
        lvl = Level()
        self.assertEqual(lvl.current_level, 1)
        self.assertEqual(lvl.current_xp, 0)
        self.assertEqual(lvl.level_up_base, 0)
        self.assertEqual(lvl.level_up_factor, 150)
        self.assertEqual(lvl.xp_given, 0)