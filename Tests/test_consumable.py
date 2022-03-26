import unittest
from components.consumable import Consumable, HealingConsumable
from entity import Item


class TestConsumable(unittest.TestCase):
    def test_parent(self):
        '''
        test that an item assigned as a parent to a consumable
        works as expected
        '''
        cm = Consumable()
        item = Item(consumable=cm)
        cm.parent = item
        self.assertEqual(cm.parent, item)

    def test_get_action(self):
        '''
        test that get action returns the correct item action
        TODO: implement this once item actions are implemented
        '''

    def test_activate(self):
        '''
        test that for a base consumable this returns an not implemented error
        TODO: implement this once item actions are implemented
        '''


class TestHealingConsumable(unittest.TestCase):
    def test_init(self):
        '''
        test that a healing consumable amount initializes without issues
        '''
        amt = 5
        cm = HealingConsumable(amount=amt)
        self.assertEqual(cm.amount, amt)

    def test_activate(self):
        '''
        test that activate will heal the fighter
        TODO: implment this once item actions are implemented
        '''
