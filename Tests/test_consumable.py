import unittest
from unittest.mock import patch
from components.consumable import Consumable, HealingConsumable
from components.ai import BaseAI
from components.fighter import Fighter
from entity import Item, Actor
from actions import ItemAction
from engine import Engine
from game_map import GameMap
from exceptions import Impossible


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
        '''
        actor = Actor(ai_cls=BaseAI, fighter=Fighter(hp=10, defense=10, power=10))
        consumable = Consumable()
        item = Item(consumable=consumable)
        consumable.parent = item
        action = consumable.get_action(consumer=actor)
        self.assertIsInstance(action, ItemAction)
        # ideally we'd check that the item action was created correctly
        # but I'm not sure how :)

    def test_activate(self):
        '''
        test that for a base consumable this returns an not implemented error
        '''
        actor = Actor(ai_cls=BaseAI, fighter=Fighter(hp=10, defense=10, power=10))
        consumable = Consumable()
        item = Item(consumable=consumable)
        consumable.parent = item
        action = consumable.get_action(consumer=actor)

        with self.assertRaises(NotImplementedError):
            consumable.activate(action)

class TestHealingConsumable(unittest.TestCase):
    def test_init(self):
        '''
        test that a healing consumable amount initializes without issues
        '''
        amt = 5
        cm = HealingConsumable(amount=amt)
        self.assertEqual(cm.amount, amt)

    def test_activate_with_recovery(self):
        '''
        test that activate will heal the fighter
        '''
        actor = Actor(ai_cls=BaseAI, fighter=Fighter(hp=10, defense=10, power=10))
        actor.fighter.hp = 3
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        consumable = HealingConsumable(amount=5)
        item = Item(consumable=consumable)
        item.parent = gm
        consumable.parent = item
        action = consumable.get_action(consumer=actor)

        with patch('message_log.MessageLog.add_message') as patch_add_message:
            consumable.activate(action=action)

        patch_add_message.assert_called_once()
        self.assertEqual(actor.fighter.hp, 8)

    def test_activate_without_recovery(self):
        '''
        test that activate raise Impossible when it cannot heal
        '''
        actor = Actor(ai_cls=BaseAI, fighter=Fighter(hp=10, defense=10, power=10))
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        consumable = HealingConsumable(amount=5)
        item = Item(consumable=consumable)
        item.parent = gm
        consumable.parent = item
        action = consumable.get_action(consumer=actor)

        with self.assertRaises(Impossible):
            consumable.activate(action=action)



