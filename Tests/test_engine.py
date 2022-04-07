from unittest.mock import Mock, patch

import numpy as np
from components.ai import HostileEnemy
from engine import Engine
from game_map import GameMap, GameWorld
import unittest

import tcod

from entity import Entity, Actor
from components.ai import HostileEnemy
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from message_log import MessageLog
from exceptions import Impossible


class Test_Engine(unittest.TestCase):
    def test_init(self):
        '''
        tests that instantiating the engine will set values correctly
        '''
        ent1 = Entity()
        eng = Engine(ent1)
        self.assertEqual(eng.player, ent1)
        self.assertIsInstance(eng.message_log, MessageLog)
        self.assertEqual(eng.mouse_location, (0, 0))

    def test_gamemap_set(self):
        '''
        tests that the gamemap can be set
        '''
        ent = Entity()
        eng = Engine(ent)
        gm = GameMap(eng, 10, 10)
        eng.game_map = gm
        self.assertEqual(eng.game_map, gm)

    def test_handle_enemy_turns(self):
        '''
        tests that an enemy taking its turn will print
        '''
        ent1 = Entity()
        ent2 = Actor(ai_cls=HostileEnemy, fighter=Fighter(
            hp=10, defense=10, power=10), inventory=Inventory(capacity=5),
            level=Level())
        eng = Engine(player=ent1)
        gm = GameMap(engine=eng, width=10,
                     height=10, entities={ent2})
        eng.game_map = gm
        ent1.parent = gm
        ent2.parent = gm

        with patch('components.ai.HostileEnemy.perform') as mock_ai_perform:
            eng.handle_enemy_turns()

        # verify the WaitAction.perform was called
        mock_ai_perform.assert_called_once()

    def test_handle_enemy_turns_exception(self):
        '''
        tests that an enemy taking its turn will pass
        and not raise when an exception is return from the enemy
        '''
        ent1 = Entity()
        ent2 = Actor(ai_cls=HostileEnemy, fighter=Fighter(
            hp=10, defense=10, power=10), inventory=Inventory(capacity=5),
            level=Level())
        eng = Engine(player=ent1)
        gm = GameMap(engine=eng, width=10,
                     height=10, entities={ent2})
        eng.game_map = gm
        ent1.parent = gm
        ent2.parent = gm

        with patch('components.ai.HostileEnemy.perform') as mock_ai_perform:
            mock_ai_perform.side_effect = Impossible("oops, impossible")
            eng.handle_enemy_turns()

        # verify the WaitAction.perform was called
        mock_ai_perform.assert_called_once()

    def test_update_fov(self):
        '''
        test that the fov is computed
        THIS WAS SO HARD FOR ME TO FIGURE OUT
        but hindsight is 20/20
        patch in the compute_fov function from tcod.map and configure
        the return value to match the expected output
        '''
        ent = Actor(x=5, y=5, ai_cls=HostileEnemy, fighter=Fighter(
            hp=10, defense=10, power=10), inventory=Inventory(capacity=5),
            level=Level())
        eng = Engine(player=ent)
        gm = GameMap(engine=eng, width=10, height=10)
        ent.parent = gm
        eng.game_map = gm

        with patch('tcod.map.compute_fov') as patch_compute_fov:
            patch_compute_fov.return_value = np.full(
                (10, 10), fill_value=True, order="F"
            )
            eng.update_fov()

        patch_compute_fov.assert_called_once()

    @patch('game_map.GameMap.render')
    @patch('message_log.MessageLog.render')
    @patch('render_functions.render_bar')
    @patch('render_functions.render_names_at_mouse_location')
    def test_render(self, patch_render, patch_MessageLog_render, patch_render_bar, patch_render_names):
        '''
        test that the render function will call the print, present, clear functions
        this one may still break the github actions, but it works fine here
        I can't get it to not pop up the window, which is probably what breaks those actions
        '''
        ent1 = Actor(ai_cls=HostileEnemy, fighter=Fighter(
            hp=10, defense=10, power=10), inventory=Inventory(capacity=5),
            level=Level())
        eng = Engine(player=ent1)
        eng.game_world = GameWorld(
            engine=eng,
            map_width=10,
            map_height=10,
            max_rooms=5,
            room_min_size=3,
            room_max_size=4,
        )
        eng.game_map = GameMap(engine=eng, width=10, height=10)

        console = tcod.Console(10, 10)

        eng.render(console=console)

        patch_render.assert_called()
        patch_MessageLog_render.assert_called()
        patch_render_bar.assert_called()
        patch_render_names.assert_called()
