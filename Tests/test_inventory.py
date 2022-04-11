import unittest
from unittest.mock import patch

from components.inventory import Inventory
from components.ai import BaseAI
from components.equipment import Equipment
from components.fighter import Fighter
from components.consumable import Consumable
from components.level import Level
from entity import Actor, Item
from engine import Engine
from game_map import GameMap


class TestInventory(unittest.TestCase):
    def test_init(self):
        '''
        test that initializing an inventory component does so without issues
        '''
        inv = Inventory(capacity=5)
        self.assertEqual(inv.capacity, 5)
        self.assertEqual(inv.items, [])

    def test_set_parent(self):
        '''
        test that the parent (actor) of an inventory can be set without issues
        '''
        actor = Actor(ai_cls=BaseAI, equipment=Equipment(), fighter=Fighter(hp=10, base_defense=10, base_power=10), inventory=Inventory(capacity=5),
                      level=Level())
        inv = Inventory(capacity=5)
        inv.parent = actor
        self.assertEqual(inv.parent, actor)

    def test_drop(self):
        '''
        test that an item can be dropped
        from the inventory and onto the map
        '''
        actor = Actor(ai_cls=BaseAI, equipment=Equipment(), fighter=Fighter(hp=10, base_defense=10, base_power=10), inventory=Inventory(capacity=5),
                      level=Level())
        inv = Inventory(capacity=5)
        inv.parent = actor
        item = Item(consumable=Consumable())
        inv.items.append(item)
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        eng.game_map = gm
        actor.parent = gm
        self.assertIn(item, inv.items)

        with patch('message_log.MessageLog.add_message') as patch_add_message:
            inv.drop(item=item)

        self.assertEqual([], inv.items)
        self.assertIn(item, gm.entities)
        patch_add_message.assert_called_once()
