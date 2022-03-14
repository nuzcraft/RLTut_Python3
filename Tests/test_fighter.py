import unittest
from components.fighter import Fighter

class Test_Fighter(unittest.TestCase):
    def test_init(self):
        '''
        test that initializing a fighter component sets
        values correctly
        '''
        ft = Fighter(hp=10, defense=20, power=30)
        self.assertEqual(ft.max_hp, 10)
        self.assertEqual(ft._hp, 10)
        self.assertEqual(ft.defense, 20)
        self.assertEqual(ft.power, 30)

    def test_property_hp(self):
        '''
        test that calling hp will return the hp value
        '''
        ft = Fighter(hp=10, defense=10, power=10)
        self.assertEqual(ft.hp, 10)

    def test_setter_hp_in_bounds(self):
        '''
        test that setting the hp works as expected
        when setting within expected range
        '''
        ft = Fighter(hp=10, defense=10, power=10)
        ft.hp = 5
        self.assertEqual(ft.hp, 5)

    def test_setter_hp_too_low(self):
        '''
        test that setting the hp works as expected
        when setting below 0
        '''
        ft = Fighter(hp=10, defense=10, power=10)
        ft.hp = -5
        self.assertEqual(ft.hp, 0)

    def test_setter_hp_too_low(self):
        '''
        test that setting the hp works as expected
        when setting below 0
        '''
        ft = Fighter(hp=10, defense=10, power=10)
        ft.hp = 15
        self.assertEqual(ft.hp, ft.max_hp)