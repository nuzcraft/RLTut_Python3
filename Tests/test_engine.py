from unittest.mock import Mock, patch

import numpy as np
from components.ai import HostileEnemy
from engine import Engine
from game_map import GameMap
import unittest

import tcod

from entity import Entity, Actor
from components.ai import HostileEnemy
from components.fighter import Fighter


class Test_Engine(unittest.TestCase):
    def test_init(self):
        '''
        tests that instantiating the engine will set values correctly
        '''
        ent1 = Entity()
        eng = Engine(ent1)
        self.assertEqual(eng.player, ent1)

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
            hp=10, defense=10, power=10))
        eng = Engine(player=ent1)
        gm = GameMap(engine=eng, width=10,
                     height=10, entities={ent2})
        eng.game_map = gm
        ent1.gamemap = gm
        ent2.gamemap = gm

        with patch('components.ai.HostileEnemy.perform') as mock_ai_perform:
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
            hp=10, defense=10, power=10))
        eng = Engine(player=ent)
        gm = GameMap(engine=eng, width=10, height=10)
        ent.gamemap = gm
        eng.game_map = gm

        with patch('tcod.map.compute_fov') as patch_compute_fov:
            patch_compute_fov.return_value = np.full(
                (10, 10), fill_value=True, order="F"
            )
            eng.update_fov()

        patch_compute_fov.assert_called_once()

    @patch('game_map.GameMap.render')
    @patch('tcod.console.Console.print')
    @patch('tcod.context.Context.present')
    @patch('tcod.console.Console.clear')
    def test_render(self, patch_render, patch_print, patch_present, patch_clear):
        '''
        test that the render function will call the print, present, clear functions
        this one may still break the github actions, but it works fine here
        I can't get it to not pop up the window, which is probably what breaks those actions
        '''
        ent1 = Actor(ai_cls=HostileEnemy, fighter=Fighter(
            hp=10, defense=10, power=10))
        eng = Engine(player=ent1)
        eng.game_map = GameMap(engine=eng, width=10, height=10)

        console = tcod.Console(10, 10)
        context = tcod.context.new(columns=10, rows=10)

        eng.render(console=console, context=context)

        patch_render.assert_called()
        patch_print.assert_called()
        patch_present.assert_called()
        patch_clear.assert_called()
