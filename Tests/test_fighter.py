from turtle import width
import unittest
from unittest.mock import patch
from components.fighter import Fighter
from components.ai import HostileEnemy
from entity import Actor
from engine import Engine
from game_map import GameMap
from render_order import RenderOrder


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

    def test_entity_set(self):
        '''
        test that an entity can be set without issues
        '''
        ft = Fighter(hp=10, defense=10, power=10)
        act = Actor(ai_cls=HostileEnemy, fighter=ft)
        ft.entity = act
        self.assertEqual(act, ft.entity)

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
        act = Actor(ai_cls=HostileEnemy, fighter=ft)
        ft.entity = act

        eng = Engine(player=act)
        gm = GameMap(engine=eng, width=10, height=10)
        act.gamemap = gm
        eng.game_map = gm

        ft.hp = -5
        self.assertEqual(ft.hp, 0)

    def test_setter_hp_too_high(self):
        '''
        test that setting the hp works as expected
        when setting above the max
        '''
        ft = Fighter(hp=10, defense=10, power=10)
        ft.hp = 15
        self.assertEqual(ft.hp, ft.max_hp)

    def test_setter_die(self):
        '''
        test that setting hp to 0 will cause the entity to die
        '''
        ft = Fighter(hp=10, defense=10, power=10)
        # this will set the ai to HostileEnemy
        act = Actor(ai_cls=HostileEnemy, fighter=ft)
        ft.entity = act

        eng = Engine(player=act)
        gm = GameMap(engine=eng, width=10, height=10)
        act.gamemap = gm
        eng.game_map = gm

        ft.hp = 0
        # triggering 'die' should remove the ai component
        self.assertIsNone(ft.entity.ai)

    @patch('builtins.print')
    def test_die_player(self, mock_print):
        '''
        test that when a player dies, they get set well
        '''
        ft = Fighter(hp=10, defense=10, power=10)
        # this will set the ai to HostileEnemy
        act = Actor(name="player", ai_cls=HostileEnemy, fighter=ft)
        ft.entity = act

        eng = Engine(player=act)
        gm = GameMap(engine=eng, width=10, height=10)
        act.gamemap = gm
        eng.game_map = gm

        ft.die()

        self.assertEqual(ft.entity.char, "%")
        self.assertEqual(ft.entity.color, (191, 0, 0))
        self.assertFalse(ft.entity.blocks_movement)
        self.assertIsNone(ft.entity.ai)
        self.assertEqual(ft.entity.name, "remains of player")
        self.assertEqual(ft.entity.render_order, RenderOrder.CORPSE)
        mock_print.assert_called_with("You died!")

    @patch('builtins.print')
    def test_die_other_actor(self, mock_print):
        '''
        test that when an actor (not player) dies, they get set well
        '''
        ft = Fighter(hp=10, defense=10, power=10)
        act = Actor(name="actor", ai_cls=HostileEnemy, fighter=ft)
        ft.entity = act

        ft2 = Fighter(hp=10, defense=10, power=10)
        act2 = Actor(name="player", ai_cls=HostileEnemy, fighter=ft2)
        ft2.entity = act2

        eng = Engine(player=act2)
        gm = GameMap(engine=eng, width=10, height=10)
        act.gamemap = gm
        act2.gamemap = gm
        eng.game_map = gm

        ft.die()

        self.assertEqual(ft.entity.char, "%")
        self.assertEqual(ft.entity.color, (191, 0, 0))
        self.assertFalse(ft.entity.blocks_movement)
        self.assertIsNone(ft.entity.ai)
        self.assertEqual(ft.entity.name, "remains of actor")
        self.assertEqual(ft.entity.render_order, RenderOrder.CORPSE)
        mock_print.assert_called_with("actor is dead!")
