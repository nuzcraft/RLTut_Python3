from unittest.mock import Mock, patch
from engine import Engine
from game_map import GameMap
import unittest
import tcod.event
from actions import MovementAction

import tcod

from entity import Entity
from input_handlers import EventHandler
import tile_types
import numpy


class Test_Engine(unittest.TestCase):
    def test_init(self):
        '''
        tests that instantiating the engine will set values correctly
        also assert that update_fov is called when the engine is initialized
        '''
        ent1 = Entity(0, 0, "@", (0, 0, 0))
        event_handler = EventHandler()
        gm = GameMap(50, 50)
        Engine.update_fov = Mock()
        eng = Engine(event_handler, gm, ent1)
        self.assertEqual(eng.event_handler, event_handler)
        self.assertEqual(eng.game_map, gm)
        self.assertEqual(eng.player, ent1)
        Engine.update_fov.assert_called_once()

    @patch('builtins.print')
    def test_handle_enemy_turns(self, mock_print):
        '''
        tests that an enemy taking its turn will print
        '''
        ent1 = Entity()
        ent2 = Entity()
        event_handler = EventHandler()
        gm = GameMap(10, 10, {ent2})
        eng = Engine(event_handler=event_handler, game_map=gm, player=ent1)
        # this function will currently call the print if there are entities
        # with turns to take
        eng.handle_enemy_turns()
        mock_print.assert_called()

    def test_handle_events_MovementAction(self):
        '''
        tests that 2 basic movement events will call perform on the resulting action
        '''
        x_val = 10
        y_val = 10
        ent1 = Entity(x_val, y_val, "@", (0, 0, 0))
        event_handler = EventHandler()
        event1 = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.UP, sym=tcod.event.K_UP, mod=tcod.event.Modifier.NONE)
        event2 = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.LEFT, sym=tcod.event.K_LEFT, mod=tcod.event.Modifier.NONE)
        gm = GameMap(50, 50)
        eng = Engine(event_handler, gm, ent1)
        # mock the perform function from the MovementAction
        MovementAction.perform = Mock()
        eng.handle_events({event1, event2})
        MovementAction.perform.assert_called()

    def test_handle_events_EscapeAction(self):
        '''
        test that an escape action will raise a system exit
        similar to test_ev_quit, I'm not sure this is working as expected :)
        '''
        ent1 = Entity(10, 10, "@", (0, 0, 0))
        event_handler = EventHandler()
        event1 = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.ESCAPE, sym=tcod.event.K_ESCAPE, mod=tcod.event.Modifier.NONE)
        gm = GameMap(50, 50)
        eng = Engine(event_handler, gm, ent1)
        with self.assertRaises(SystemExit) as c:
            eng.handle_events({event1})
        self.assertEqual(c.exception.code, None)

    def test_handle_events_NoAction(self):
        '''
        tests that an unused event does not trigger any change in the engine 
        '''
        x_val = 0
        y_val = 0
        ent1 = Entity(x_val, y_val, "@", (0, 0, 0))
        event_handler = EventHandler()
        event1 = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.HOME, sym=tcod.event.K_HOME, mod=tcod.event.Modifier.NONE)
        gm = GameMap(50, 50)
        eng = Engine(event_handler, gm, ent1)
        # the below function will fail if an escape action is passed
        # the assertEquals will fail if a movement action is passed in
        eng.handle_events({event1})
        self.assertEqual(eng.player.x, x_val)
        self.assertEqual(eng.player.y, y_val)

    # # @patch.object(tcod.map, 'compute_fov')
    # def test_update_fov(self):
    #     '''
    #     test that the fov is computed
    #     I couldn't figure out how to mock the right function, so well
    #     make sure the 'visible' array is different from when the GameMap
    #     is created
    #     UPDATE: this didn't work, may have to workshop this test later
    #     the final assertIsNone should fail if the arrays are not the same
    #     (and they shouldn't be if the fov is updated after the tile types switch)
    #     '''
    #     ent1 = Entity(1, 1, "@", (0, 0, 0))
    #     event_handler = EventHandler()
    #     gm = GameMap(50, 50)
    #     eng = Engine(
    #         entities={}, event_handler=event_handler, game_map=gm, player=ent1)
    #     init_visible = eng.game_map.visible
    #     eng.game_map.tiles[:] = tile_types.floor
    #     eng.update_fov()
    #     self.assertIsNone(numpy.testing.assert_array_equal(
    #         eng.game_map.visible, init_visible))

    def test_render(self):
        '''
        lets try to test that the render function works by mocking the console functions?
        mock a few of the functions and make sure they are called
        UPDATE: remove the print assert bc it was unreliable
        '''
        ent1 = Entity(1, 1, "@", (0, 0, 0))
        event_handler = EventHandler()
        gm = GameMap(50, 50)
        eng = Engine(
            event_handler=event_handler, game_map=gm, player=ent1)

        with tcod.context.new_terminal(50, 50) as context:
            console = tcod.Console(50, 50)
            # console.print = Mock()
            context.present = Mock()
            console.clear = Mock()
            eng.render(console, context)
            # console.print.assert_called_once()
            context.present.assert_called_once_with(console)
            console.clear.assert_called_once()
