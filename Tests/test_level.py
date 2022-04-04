import unittest
from unittest.mock import patch

from components.level import Level
from components.ai import BaseAI
from components.fighter import Fighter
from components.inventory import Inventory
from engine import Engine
from entity import Actor
from game_map import GameMap

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

    def test_property_experience_to_next_level(self):
        '''
        test that the experience to next level property returns properly
        '''
        lvl = Level(
            current_level=5,
            level_up_base=200,
            level_up_factor=150,
        )
        expected_return = 200 + 5*150
        self.assertEqual(lvl.experience_to_next_level, expected_return)

    def test_property_requires_level_up_true(self):
        '''
        test that the requires level up property will return true when current xp
        is greater than the experience needed for the next level
        '''
        lvl = Level(
            current_level=1,
            current_xp=1000,
            level_up_base=200,
            level_up_factor=150,
        )
        self.assertTrue(lvl.requires_level_up)

    def test_property_requires_level_up_false(self):
        '''
        test that the requires level up property will return true when current xp
        is greater than the experience needed for the next level
        '''
        lvl = Level(
            current_level=1,
            current_xp=100,
            level_up_base=200,
            level_up_factor=150,
        )
        self.assertFalse(lvl.requires_level_up)

    def test_add_xp_no_xp(self):
        '''
        test that calling add_xp adding 0 xp will not add xp
        '''
        lvl = Level(current_xp=0, level_up_base=200)
        lvl.add_xp(xp=0)
        self.assertEqual(lvl.current_xp, 0)

    def test_add_xp_no_level_up_base(self):
        '''
        test that calling add_xp adding xp while level up base is 0 will not add xp
        '''
        lvl = Level(current_xp=0, level_up_base=0)
        lvl.add_xp(xp=100)
        self.assertEqual(lvl.current_xp, 0)

    def test_add_xp(self):
        '''
        test that calling add_xp adding xp will also add a message to the log
        '''
        actor = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        actor.parent = gm
        lvl = Level(
            current_level=1,
            level_up_base=200,
            level_up_factor=150,
        )
        lvl.parent=actor

        with patch('message_log.MessageLog.add_message') as patch_add_message:
            lvl.add_xp(xp=100)

        self.assertEqual(lvl.current_xp, 100)
        patch_add_message.assert_any_call(
            f"You gain 100 experience points."
        )

    def test_add_xp_with_level_up(self):
        '''
        test that calling add_xp adding xp will also add a message to the log
        when the 
        '''
        actor = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        actor.parent = gm
        lvl = Level(
            current_level=1,
            level_up_base=200,
            level_up_factor=150,
        )
        lvl.parent=actor

        with patch('message_log.MessageLog.add_message') as patch_add_message:
            lvl.add_xp(xp=1000)

        self.assertEqual(lvl.current_xp, 1000)
        patch_add_message.assert_any_call(
            f"You gain 1000 experience points."
        )
        patch_add_message.assert_any_call(
            f"You advance to level 2!"
        )

    def test_increase_level(self):
        '''
        test that calling increase_level will increase the level 
        '''
        actor = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        actor.parent = gm
        lvl = Level(
            current_level=1,
            level_up_base=200,
            level_up_factor=150,
        )
        lvl.parent=actor
        lvl.increase_level()
        self.assertEqual(lvl.current_level, 2)

    def test_increase_max_hp(self):
        '''
        test that calling increase_max_hp will increase the max_hp and hp
        '''
        actor = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        actor.fighter.hp = 3
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        actor.parent = gm
        lvl = Level(
            current_level=1,
            level_up_base=200,
            level_up_factor=150,
        )
        lvl.parent=actor

        with patch('message_log.MessageLog.add_message') as patch_add_message:
            lvl.increase_max_hp(amount=5)
        self.assertEqual(actor.fighter.hp, 8)
        self.assertEqual(actor.fighter.max_hp, 15)
        patch_add_message.assert_called_once()

    def test_increase_power(self):
        '''
        test that calling increase_power will increase the power
        '''
        actor = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        actor.parent = gm
        lvl = Level(
            current_level=1,
            level_up_base=200,
            level_up_factor=150,
        )
        lvl.parent=actor

        with patch('message_log.MessageLog.add_message') as patch_add_message:
            lvl.increase_power(amount=5)
        self.assertEqual(actor.fighter.power, 15)
        patch_add_message.assert_called_once()

    def test_increase_defense(self):
        '''
        test that calling increase_defense will increase the defense
        '''
        actor = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        actor.parent = gm
        lvl = Level(
            current_level=1,
            level_up_base=200,
            level_up_factor=150,
        )
        lvl.parent=actor

        with patch('message_log.MessageLog.add_message') as patch_add_message:
            lvl.increase_defense(amount=5)
        self.assertEqual(actor.fighter.defense, 15)
        patch_add_message.assert_called_once()

