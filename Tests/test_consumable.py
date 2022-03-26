import unittest
from components.consumable import Consumable
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
