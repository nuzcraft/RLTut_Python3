import unittest
from unittest.mock import patch
from tcod import console_get_char_background, console_get_char_foreground
import tcod.event
from tcod.console import Console
from input_handlers import (
    EventHandler,
    MainGameEventHandler,
    GameOverEventHandler,
    HistoryViewer,
    AskUserEventHandler,
    InventoryEventHandler,
    InventoryActivateHandler,
    InventoryDropHandler,
    SelectIndexHandler,
)

from actions import (
    BumpAction,
    WaitAction,
    PickupAction,
    DropItem,
)
from engine import Engine
from entity import Entity, Actor, Item
from game_map import GameMap
from exceptions import Impossible
from components.ai import BaseAI
from components.fighter import Fighter
from components.inventory import Inventory
from components.consumable import Consumable
import color


class Test_EventHandler(unittest.TestCase):
    def test_init(self):
        '''
        test that initializing the event handler sets correctly
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = EventHandler(engine=eng)
        self.assertEqual(event_handler.engine, eng)

    def test_handle_events(self):
        '''
        test that the handle_events function calls the handle_action
        function
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = EventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.UP, sym=tcod.event.K_UP, mod=tcod.event.Modifier.NONE
        )
        with patch('input_handlers.EventHandler.handle_action') as patch_handle_action:
            event_handler.handle_events(event=event)

        patch_handle_action.assert_called_once()

    def test_handle_action_none(self):
        '''
        tests that the handle_action function will return false
        if the action is none
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = EventHandler(engine=eng)
        pass_turn_bool = event_handler.handle_action(None)
        self.assertFalse(pass_turn_bool)

    @patch('engine.Engine.handle_enemy_turns')
    @patch('engine.Engine.update_fov')
    def test_handle_action_any(self, patch_handle_enemy_turns, patch_update_fov):
        '''
        tests that the handle_action function will return true
        when a real action is passed in
        '''
        ent = Entity()
        eng = Engine(player=ent)
        gm = GameMap(engine=eng, width=10, height=10)
        eng.game_map = gm
        event_handler = EventHandler(engine=eng)
        action = WaitAction(entity=ent)
        pass_turn_bool = event_handler.handle_action(action)
        self.assertTrue(pass_turn_bool)
        patch_handle_enemy_turns.assert_called_once()
        patch_update_fov.assert_called_once()

    @patch('engine.Engine.handle_enemy_turns')
    @patch('engine.Engine.update_fov')
    def test_handle_action_impossible(self, patch_handle_enemy_turns, patch_update_fov):
        '''
        tests that the handle_action function will return false
        when the perform action excepts with an impossible exception
        '''
        ent = Entity()
        eng = Engine(player=ent)
        gm = GameMap(engine=eng, width=10, height=10)
        eng.game_map = gm
        event_handler = EventHandler(engine=eng)
        action = WaitAction(entity=ent)

        with patch('actions.WaitAction.perform') as patch_peform:
            patch_peform.side_effect = Impossible('lol, error')
            pass_turn_bool = event_handler.handle_action(action)
        self.assertFalse(pass_turn_bool)
        self.assertEqual(
            'lol, error', event_handler.engine.message_log.messages[0].full_text)
        patch_handle_enemy_turns.assert_not_called()
        patch_update_fov.assert_not_called()

    def test_ev_mousemotion_in_bounds(self):
        '''
        test that moving the mouse will set the engine.mouse_location
        '''
        ent = Entity()
        eng = Engine(player=ent)
        gm = GameMap(engine=eng, width=10, height=10)
        eng.game_map = gm
        event_handler = EventHandler(engine=eng)
        event = tcod.event.MouseMotion(tile=(5, 6))
        event_handler.ev_mousemotion(event=event)
        self.assertEqual(event_handler.engine.mouse_location, (5, 6))

    def test_ev_mousemotion_not_in_bounds(self):
        '''
        test that moving the mouse out of bounds 
        will not set the engine.mouse_location
        '''
        ent = Entity()
        eng = Engine(player=ent)
        gm = GameMap(engine=eng, width=10, height=10)
        eng.game_map = gm
        event_handler = EventHandler(engine=eng)
        event = tcod.event.MouseMotion(tile=(12, 12))
        event_handler.ev_mousemotion(event=event)
        # check for 0,0 to assert that the mouse_location did not move
        self.assertEqual(event_handler.engine.mouse_location, (0, 0))

    # ev_quit will only trigger on tcod.event.Quit() events, no need to negative test
    def test_ev_quit(self):
        # TODO: the assertEquals seems like it might be wrong (but its working)
        # seems like the exception code should be 1, not none
        '''
        tests that the a quit action will raise an exception
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = EventHandler(engine=eng)
        event = tcod.event.Quit()
        with self.assertRaises(SystemExit) as action:
            event_handler.dispatch(event)
        self.assertEqual(action.exception.code, None)


class Test_MainGameEventHandler(unittest.TestCase):
    # tcod.event.KeyDown() events will trigger ev_keydown
    def test_ev_keydown_up(self):
        '''
        tests that pressing up will move the player up
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.UP, sym=tcod.event.K_UP, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, BumpAction)
        self.assertEqual(action.dx, 0)
        self.assertEqual(action.dy, -1)

    def test_ev_keydown_down(self):
        '''
        tests that pressing down will move the player down
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.DOWN, sym=tcod.event.K_DOWN, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, BumpAction)
        self.assertEqual(action.dx, 0)
        self.assertEqual(action.dy, 1)

    def test_ev_keydown_left(self):
        '''
        tests that pressing left will move the player left
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.LEFT, sym=tcod.event.K_LEFT, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, BumpAction)
        self.assertEqual(action.dx, -1)
        self.assertEqual(action.dy, 0)

    def test_ev_keydown_right(self):
        '''
        tests that pressing right will move the player right
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.RIGHT, sym=tcod.event.K_RIGHT, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, BumpAction)
        self.assertEqual(action.dx, 1)
        self.assertEqual(action.dy, 0)

    def test_ev_keydown_home(self):
        '''
        tests that pressing home will move the player up and left
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.HOME, sym=tcod.event.K_HOME, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, BumpAction)
        self.assertEqual(action.dx, -1)
        self.assertEqual(action.dy, -1)

    def test_ev_keydown_end(self):
        '''
        tests that pressing end will move the player down and left
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.END, sym=tcod.event.K_END, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, BumpAction)
        self.assertEqual(action.dx, -1)
        self.assertEqual(action.dy, 1)

    def test_ev_keydown_pageup(self):
        '''
        tests that pressing pageup will move the player right and up
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.PAGEUP, sym=tcod.event.K_PAGEUP, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, BumpAction)
        self.assertEqual(action.dx, 1)
        self.assertEqual(action.dy, -1)

    def test_ev_keydown_pagedown(self):
        '''
        tests that pressing right will move the player right
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.PAGEDOWN, sym=tcod.event.K_PAGEDOWN, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, BumpAction)
        self.assertEqual(action.dx, 1)
        self.assertEqual(action.dy, 1)

    def test_ev_keydown_kp8(self):
        '''
        tests that pressing keypad 8 will move the player up
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.KP_8, sym=tcod.event.K_KP_8, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, BumpAction)
        self.assertEqual(action.dx, 0)
        self.assertEqual(action.dy, -1)

    def test_ev_keydown_kp2(self):
        '''
        tests that pressing keypad 2 will move the player down
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.KP_2, sym=tcod.event.K_KP_2, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, BumpAction)
        self.assertEqual(action.dx, 0)
        self.assertEqual(action.dy, 1)

    def test_ev_keydown_kp4(self):
        '''
        tests that pressing keypad 4 will move the player left
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.KP_4, sym=tcod.event.K_KP_4, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, BumpAction)
        self.assertEqual(action.dx, -1)
        self.assertEqual(action.dy, 0)

    def test_ev_keydown_kp6(self):
        '''
        tests that pressing keypad 6 will move the player right
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.KP_6, sym=tcod.event.K_KP_6, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, BumpAction)
        self.assertEqual(action.dx, 1)
        self.assertEqual(action.dy, 0)

    def test_ev_keydown_kp7(self):
        '''
        tests that pressing kp 7 will move the player up and left
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.KP_7, sym=tcod.event.K_KP_7, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, BumpAction)
        self.assertEqual(action.dx, -1)
        self.assertEqual(action.dy, -1)

    def test_ev_keydown_kp1(self):
        '''
        tests that pressing end will move the player down and left
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.KP_1, sym=tcod.event.K_KP_1, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, BumpAction)
        self.assertEqual(action.dx, -1)
        self.assertEqual(action.dy, 1)

    def test_ev_keydown_kp9(self):
        '''
        tests that pressing pageup will move the player right and up
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.KP_9, sym=tcod.event.K_KP_9, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, BumpAction)
        self.assertEqual(action.dx, 1)
        self.assertEqual(action.dy, -1)

    def test_ev_keydown_kp3(self):
        '''
        tests that pressing right will move the player right
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.KP_3, sym=tcod.event.K_KP_3, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, BumpAction)
        self.assertEqual(action.dx, 1)
        self.assertEqual(action.dy, 1)

    def test_ev_keydown_k(self):
        '''
        tests that pressing k will move the player up
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.K, sym=tcod.event.K_k, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, BumpAction)
        self.assertEqual(action.dx, 0)
        self.assertEqual(action.dy, -1)

    def test_ev_keydown_j(self):
        '''
        tests that pressing j will move the player down
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.J, sym=tcod.event.K_j, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, BumpAction)
        self.assertEqual(action.dx, 0)
        self.assertEqual(action.dy, 1)

    def test_ev_keydown_h(self):
        '''
        tests that pressing h will move the player left
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.H, sym=tcod.event.K_h, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, BumpAction)
        self.assertEqual(action.dx, -1)
        self.assertEqual(action.dy, 0)

    def test_ev_keydown_l(self):
        '''
        tests that pressing keypad 6 will move the player right
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.L, sym=tcod.event.K_l, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, BumpAction)
        self.assertEqual(action.dx, 1)
        self.assertEqual(action.dy, 0)

    def test_ev_keydown_y(self):
        '''
        tests that pressing y will move the player up and left
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.Y, sym=tcod.event.K_y, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, BumpAction)
        self.assertEqual(action.dx, -1)
        self.assertEqual(action.dy, -1)

    def test_ev_keydown_b(self):
        '''
        tests that pressing end will move the player down and left
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.B, sym=tcod.event.K_b, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, BumpAction)
        self.assertEqual(action.dx, -1)
        self.assertEqual(action.dy, 1)

    def test_ev_keydown_u(self):
        '''
        tests that pressing pageup will move the player right and up
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.U, sym=tcod.event.K_u, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, BumpAction)
        self.assertEqual(action.dx, 1)
        self.assertEqual(action.dy, -1)

    def test_ev_keydown_n(self):
        '''
        tests that pressing right will move the player right
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.N, sym=tcod.event.K_n, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, BumpAction)
        self.assertEqual(action.dx, 1)
        self.assertEqual(action.dy, 1)

    def test_ev_keydown_period(self):
        '''
        tests that pressing period will cause the player to wait
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.PERIOD, sym=tcod.event.K_PERIOD, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, WaitAction)

    def test_ev_keydown_kp5(self):
        '''
        tests that pressing keypad 5 will cause the player to wait
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.KP_5, sym=tcod.event.K_KP_5, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, WaitAction)

    def test_ev_keydown_clear(self):
        '''
        tests that pressing clear will cause the player to wait
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.CLEAR, sym=tcod.event.K_CLEAR, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, WaitAction)

    def test_ev_keydown_escape(self):
        '''
        tests that pressing escape results in an EscapeAction
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.ESCAPE, sym=tcod.event.K_ESCAPE, mod=tcod.event.Modifier.NONE)
        with self.assertRaises(SystemExit):
            action = event_handler.dispatch(event)

    def test_ev_keydown_v(self):
        '''
        tests that pressing v results in opening up the history viewer
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.V, sym=tcod.event.K_v, mod=tcod.event.Modifier.NONE)
        event_handler.ev_keydown(event=event)
        self.assertIsInstance(
            event_handler.engine.event_handler, HistoryViewer)

    def test_ev_keydown_g(self):
        '''
        tests that pressing g returns a pickup action
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.G, sym=tcod.event.K_g, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, PickupAction)

    def test_ev_keydown_i(self):
        '''
        tests that pressing i will update the event_handler to InventoryActivateHandler
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.I, sym=tcod.event.K_i, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(
            event_handler.engine.event_handler, InventoryActivateHandler)

    def test_ev_keydown_d(self):
        '''
        tests that pressing d will update the event_handler to InventoryDropHandler
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.D, sym=tcod.event.K_d, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(
            event_handler.engine.event_handler, InventoryDropHandler)

    # using the backslash button as an unassigned button
    def test_ev_keydown_other(self):
        '''
        tests that pressing an unassigned button will do nothing
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = MainGameEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.BACKSLASH, sym=tcod.event.K_BACKSLASH, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsNone(action)

    def test_handle_events(self):
        '''
        TODO: implement this test
        this is predicated on being able to add events to the tcod event list
        and I'm not sure how to do that, so this will need to wait
        '''


class Test_GameOverEventHandler(unittest.TestCase):
    def test_handle_events(self):
        '''
        TODO: implement this test
        this is predicated on being able to add events to the tcod event list
        and I'm not sure how to do that, so this will need to wait
        '''

    def test_ev_keydown_escape(self):
        '''
        tests that pressing escape results in an EscapeAction
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = GameOverEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.ESCAPE, sym=tcod.event.K_ESCAPE, mod=tcod.event.Modifier.NONE)

        with self.assertRaises(SystemExit):
            event_handler.dispatch(event)

    def test_ev_keydown_other(self):
        '''
        tests that pressing an unassigned button will do nothing
        note that we're using UP, which will do something in other event handlers
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = GameOverEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.UP, sym=tcod.event.K_UP, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsNone(action)


class Test_HistoryViewer(unittest.TestCase):
    def test_init(self):
        '''
        test that the HistoryViewer class can be initialized
        '''
        ent = Entity()
        eng = Engine(player=ent)
        eng.message_log.add_message('Hello')
        eng.message_log.add_message('World')
        eng.message_log.add_message('by Nuzcraft')
        event_handler = HistoryViewer(engine=eng)
        self.assertEqual(event_handler.log_length, 3)
        self.assertEqual(event_handler.cursor, 2)

    def test_on_render(self):
        '''
        I'm not actually sure what's worth testing here :/
        we could make sure all the tcod.console commands are ran,
        but there's no logic here to break. either they work or they dont
        '''

    def test_ev_keydown_top_to_bottom(self):
        '''
        test that moving up while at the top will push us to the bottom 
        i.e. set the cursor equal to the length of the log - 1
        '''
        ent = Entity()
        eng = Engine(player=ent)
        eng.message_log.add_message('Hello')
        eng.message_log.add_message('World')
        eng.message_log.add_message('by Nuzcraft')
        event_handler = HistoryViewer(engine=eng)
        event_handler.cursor = 0
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.UP, sym=tcod.event.K_UP, mod=tcod.event.Modifier.NONE)

        event_handler.ev_keydown(event=event)
        self.assertEqual(event_handler.cursor, event_handler.log_length - 1)

    def test_ev_keydown_bottom_to_top(self):
        '''
        test that moving down while at the bottom will push us to the top 
        i.e. set the cursor equal to 0
        '''
        ent = Entity()
        eng = Engine(player=ent)
        eng.message_log.add_message('Hello')
        eng.message_log.add_message('World')
        eng.message_log.add_message('by Nuzcraft')
        event_handler = HistoryViewer(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.DOWN, sym=tcod.event.K_DOWN, mod=tcod.event.Modifier.NONE)

        event_handler.ev_keydown(event=event)
        self.assertEqual(event_handler.cursor, 0)

    def test_ev_keydown_up(self):
        '''
        test that moving up will push the cursor up 1
        '''
        ent = Entity()
        eng = Engine(player=ent)
        for x in range(0, 20):  # 20 messages
            eng.message_log.add_message('Message Number: %d' % x)
        event_handler = HistoryViewer(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.UP, sym=tcod.event.K_UP, mod=tcod.event.Modifier.NONE)
        self.assertEqual(event_handler.cursor, 19)
        event_handler.ev_keydown(event=event)
        self.assertEqual(event_handler.cursor, 18)

    def test_ev_keydown_pg_up(self):
        '''
        test that pushing pgup will push the cursor up 10
        '''
        ent = Entity()
        eng = Engine(player=ent)
        for x in range(0, 20):  # 20 messages
            eng.message_log.add_message('Message Number: %d' % x)
        event_handler = HistoryViewer(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.PAGEUP, sym=tcod.event.K_PAGEUP, mod=tcod.event.Modifier.NONE)
        self.assertEqual(event_handler.cursor, 19)
        event_handler.ev_keydown(event=event)
        self.assertEqual(event_handler.cursor, 9)

    def test_ev_keydown_down(self):
        '''
        test that pushing down will push the cursor down 1
        '''
        ent = Entity()
        eng = Engine(player=ent)
        for x in range(0, 20):  # 20 messages
            eng.message_log.add_message('Message Number: %d' % x)
        event_handler = HistoryViewer(engine=eng)
        event_handler.cursor = 0
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.DOWN, sym=tcod.event.K_DOWN, mod=tcod.event.Modifier.NONE)
        self.assertEqual(event_handler.cursor, 0)
        event_handler.ev_keydown(event=event)
        self.assertEqual(event_handler.cursor, 1)

    def test_ev_keydown_pg_down(self):
        '''
        test that pushing pgdown will push the cursor down 10
        '''
        ent = Entity()
        eng = Engine(player=ent)
        for x in range(0, 20):  # 20 messages
            eng.message_log.add_message('Message Number: %d' % x)
        event_handler = HistoryViewer(engine=eng)
        event_handler.cursor = 0
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.PAGEDOWN, sym=tcod.event.K_PAGEDOWN, mod=tcod.event.Modifier.NONE)
        self.assertEqual(event_handler.cursor, 0)
        event_handler.ev_keydown(event=event)
        self.assertEqual(event_handler.cursor, 10)

    def test_ev_keydown_home(self):
        '''
        test that pushing home will move the cursor to the top 
        '''
        ent = Entity()
        eng = Engine(player=ent)
        for x in range(0, 20):  # 20 messages
            eng.message_log.add_message('Message Number: %d' % x)
        event_handler = HistoryViewer(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.HOME, sym=tcod.event.K_HOME, mod=tcod.event.Modifier.NONE)
        self.assertEqual(event_handler.cursor, 19)
        event_handler.ev_keydown(event=event)
        self.assertEqual(event_handler.cursor, 0)

    def test_ev_keydown_end(self):
        '''
        test that pushing end will move the cursor to the bottom
        '''
        ent = Entity()
        eng = Engine(player=ent)
        for x in range(0, 20):  # 20 messages
            eng.message_log.add_message('Message Number: %d' % x)
        event_handler = HistoryViewer(engine=eng)
        event_handler.cursor = 5
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.END, sym=tcod.event.K_END, mod=tcod.event.Modifier.NONE)
        self.assertEqual(event_handler.cursor, 5)
        event_handler.ev_keydown(event=event)
        self.assertEqual(event_handler.cursor, 19)

    def test_ev_keydown_other(self):
        '''
        test that pushing any other button will exit the event
        and set the engine event handler to MainGameEventHander
        '''
        ent = Entity()
        eng = Engine(player=ent)
        for x in range(0, 20):  # 20 messages
            eng.message_log.add_message('Message Number: %d' % x)
        event_handler = HistoryViewer(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.K, sym=tcod.event.K_k, mod=tcod.event.Modifier.NONE)
        event_handler.ev_keydown(event=event)
        self.assertIsInstance(
            event_handler.engine.event_handler, MainGameEventHandler)


class TestAskUserEventHandler(unittest.TestCase):
    def test_handle_action_True(self):
        '''
        test that the handle action function resets the event handler of the engine
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = AskUserEventHandler(engine=eng)
        eng.event_handler = event_handler
        action = WaitAction(entity=ent)

        with patch('input_handlers.EventHandler.handle_action') as patch_handle_action:
            patch_handle_action.return_value = True
            ret = event_handler.handle_action(action=action)

        self.assertTrue(ret)
        self.assertIsInstance(
            event_handler.engine.event_handler, MainGameEventHandler)

    def test_handle_action_False(self):
        '''
        test that the handle action function does not reset the event handler of the engine
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = AskUserEventHandler(engine=eng)
        eng.event_handler = event_handler
        action = WaitAction(entity=ent)

        with patch('input_handlers.EventHandler.handle_action') as patch_handle_action:
            patch_handle_action.return_value = False
            ret = event_handler.handle_action(action=action)

        self.assertFalse(ret)
        self.assertNotIsInstance(
            event_handler.engine.event_handler, MainGameEventHandler)
        self.assertIsInstance(
            event_handler.engine.event_handler, AskUserEventHandler)

    def test_ev_keydown_LSHIFT(self):
        '''
        test that sending a keydown event for LSHIFT will return none 
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = AskUserEventHandler(engine=eng)
        eng.event_handler = event_handler
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.LSHIFT, sym=tcod.event.K_LSHIFT, mod=tcod.event.Modifier.NONE)
        ret = event_handler.ev_keydown(event=event)
        self.assertIsNone(ret)

    def test_ev_keydown_RSHIFT(self):
        '''
        test that sending a keydown event for RSHIFT will return none 
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = AskUserEventHandler(engine=eng)
        eng.event_handler = event_handler
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.RSHIFT, sym=tcod.event.K_RSHIFT, mod=tcod.event.Modifier.NONE)
        ret = event_handler.ev_keydown(event=event)
        self.assertIsNone(ret)

    def test_ev_keydown_LCTRL(self):
        '''
        test that sending a keydown event for LCTRL will return none 
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = AskUserEventHandler(engine=eng)
        eng.event_handler = event_handler
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.LCTRL, sym=tcod.event.K_LCTRL, mod=tcod.event.Modifier.NONE)
        ret = event_handler.ev_keydown(event=event)
        self.assertIsNone(ret)

    def test_ev_keydown_RCTRL(self):
        '''
        test that sending a keydown event for RCTRL will return none 
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = AskUserEventHandler(engine=eng)
        eng.event_handler = event_handler
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.RCTRL, sym=tcod.event.K_RCTRL, mod=tcod.event.Modifier.NONE)
        ret = event_handler.ev_keydown(event=event)
        self.assertIsNone(ret)

    def test_ev_keydown_LALT(self):
        '''
        test that sending a keydown event for LALT will return none 
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = AskUserEventHandler(engine=eng)
        eng.event_handler = event_handler
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.LALT, sym=tcod.event.K_LALT, mod=tcod.event.Modifier.NONE)
        ret = event_handler.ev_keydown(event=event)
        self.assertIsNone(ret)

    def test_ev_keydown_RALT(self):
        '''
        test that sending a keydown event for RALT will return none 
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = AskUserEventHandler(engine=eng)
        eng.event_handler = event_handler
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.RALT, sym=tcod.event.K_RALT, mod=tcod.event.Modifier.NONE)
        ret = event_handler.ev_keydown(event=event)
        self.assertIsNone(ret)

    def test_ev_keydown_other(self):
        '''
        test that sending a keydown event for g will call self.on_exit 
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = AskUserEventHandler(engine=eng)
        eng.event_handler = event_handler
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.G, sym=tcod.event.K_g, mod=tcod.event.Modifier.NONE)
        with patch("input_handlers.AskUserEventHandler.on_exit") as patch_on_exit:
            ret = event_handler.ev_keydown(event=event)
        patch_on_exit.assert_called_once()

    def test_ev_mousebuttondown(self):
        '''
        test that sending a mouse click will call self.on_exit 
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = AskUserEventHandler(engine=eng)
        eng.event_handler = event_handler
        event = tcod.event.MouseButtonDown()
        with patch("input_handlers.AskUserEventHandler.on_exit") as patch_on_exit:
            ret = event_handler.ev_mousebuttondown(event=event)
        patch_on_exit.assert_called_once()

    def test_on_exit(self):
        '''
        test that on_exit will update the engine event handler and return none
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = AskUserEventHandler(engine=eng)
        eng.event_handler = event_handler
        ret = event_handler.on_exit()
        self.assertIsInstance(
            event_handler.engine.event_handler, MainGameEventHandler)
        self.assertIsNone(ret)


class TestIventoryEventHandler(unittest.TestCase):
    def test_on_render_player_on_left(self):
        '''
        test that when the player is on the left, the window is offset
        '''
        console = Console(width=50, height=50, order='F')
        player = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=50, height=50)
        eng.game_map = gm
        player.parent = gm
        event_handler = InventoryEventHandler(engine=eng)
        with patch('tcod.console.Console.draw_frame') as patch_draw_frame:
            event_handler.on_render(console=console)
        patch_draw_frame.assert_called_once_with(
            x=40,
            y=0,
            width=19,
            height=3,
            title="<missing title>",
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

    def test_on_render_player_on_right(self):
        '''
        test that when the player is on the right, the window is not offset
        '''
        console = Console(width=50, height=50, order='F')
        player = Actor(
            x=40,
            y=40,
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=50, height=50)
        eng.game_map = gm
        player.parent = gm
        event_handler = InventoryEventHandler(engine=eng)
        with patch('tcod.console.Console.draw_frame') as patch_draw_frame:
            event_handler.on_render(console=console)
        patch_draw_frame.assert_called_once_with(
            x=0,
            y=0,
            width=19,
            height=3,
            title="<missing title>",
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

    def test_on_render_height_calulated(self):
        '''
        test that when the player has multiple items, the height of the 
        window is calculated properly (num items + 2)
        '''
        console = Console(width=50, height=50, order='F')
        player = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        player.inventory.items = [
            Item(consumable=Consumable),
            Item(consumable=Consumable),
            Item(consumable=Consumable),
        ]
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=50, height=50)
        eng.game_map = gm
        player.parent = gm
        event_handler = InventoryEventHandler(engine=eng)
        with patch('tcod.console.Console.draw_frame') as patch_draw_frame:
            event_handler.on_render(console=console)
        patch_draw_frame.assert_called_once_with(
            x=40,
            y=0,
            width=19,
            height=5,
            title="<missing title>",
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

    def test_on_render_items_printed(self):
        '''
        test that when the player has multiple items, they are printed
        on screen with the correct name and index
        '''
        console = Console(width=50, height=50, order='F')
        player = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        player.inventory.items = [
            Item(name="item1", consumable=Consumable),
            Item(name="item2", consumable=Consumable),
            Item(name="item3", consumable=Consumable),
        ]
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=50, height=50)
        eng.game_map = gm
        player.parent = gm
        event_handler = InventoryEventHandler(engine=eng)
        with patch('tcod.console.Console.print') as patch_print:
            event_handler.on_render(console=console)
        patch_print.assert_any_call(41, 1, '(a) item1')
        patch_print.assert_any_call(41, 2, '(b) item2')
        patch_print.assert_any_call(41, 3, '(c) item3')

    def test_on_render_no_items(self):
        '''
        test that when the player has no items, one (Empty) row is printed
        '''
        console = Console(width=50, height=50, order='F')
        player = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=50, height=50)
        eng.game_map = gm
        player.parent = gm
        event_handler = InventoryEventHandler(engine=eng)
        with patch('tcod.console.Console.print') as patch_print:
            event_handler.on_render(console=console)
        patch_print.assert_any_call(41, 1, '(Empty)')

    def test_ev_keydown_good_index(self):
        '''
        test that hitting a letter key will grab the selected item
        '''
        player = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        item1 = Item(name="item1", consumable=Consumable)
        player.inventory.items = [
            item1,
        ]
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=50, height=50)
        eng.game_map = gm
        player.parent = gm
        event_handler = InventoryEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.A, sym=tcod.event.K_a, mod=tcod.event.Modifier.NONE)
        with patch('input_handlers.InventoryEventHandler.on_item_selected') as patch_on_item_selected:
            action = event_handler.ev_keydown(event=event)
        patch_on_item_selected.assert_called_with(item1)

    def test_ev_keydown_good_index_no_item(self):
        '''
        test that hitting a letter key will return None when 
        there is no available item
        '''
        player = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        item1 = Item(name="item1", consumable=Consumable)
        player.inventory.items = [
            item1,
        ]
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=50, height=50)
        eng.game_map = gm
        player.parent = gm
        event_handler = InventoryEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.B, sym=tcod.event.K_b, mod=tcod.event.Modifier.NONE)
        with patch('message_log.MessageLog.add_message') as patch_add_message:
            action = event_handler.ev_keydown(event=event)
        patch_add_message.assert_called()
        self.assertIsNone(action)

    def test_ev_keydown_bad_index(self):
        '''
        test that hitting a non-letter key will invoke the 
        AskUserEventHandler's ev_keydown
        '''
        player = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        item1 = Item(name="item1", consumable=Consumable)
        player.inventory.items = [
            item1,
        ]
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=50, height=50)
        eng.game_map = gm
        player.parent = gm
        event_handler = InventoryEventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.N1, sym=tcod.event.K_1, mod=tcod.event.Modifier.NONE)
        with patch('input_handlers.AskUserEventHandler.ev_keydown') as patch_ev_keydown:
            action = event_handler.ev_keydown(event=event)
        patch_ev_keydown.assert_called()

    def test_on_item_selected(self):
        '''
        test that this function will raise an error
        '''
        player = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        item1 = Item(name="item1", consumable=Consumable)
        player.inventory.items = [
            item1,
        ]
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=50, height=50)
        eng.game_map = gm
        player.parent = gm
        event_handler = InventoryEventHandler(engine=eng)
        with self.assertRaises(NotImplementedError):
            event_handler.on_item_selected(item=item1)


class TestInventoryActivateHandler(unittest.TestCase):
    def test_on_item_selected(self):
        '''
        test that selecting an item will call the get_action of the consumable
        '''
        player = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        item1 = Item(name="item1", consumable=Consumable)
        player.inventory.items = [
            item1,
        ]
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=50, height=50)
        eng.game_map = gm
        player.parent = gm
        event_handler = InventoryActivateHandler(engine=eng)
        with patch('components.consumable.Consumable.get_action') as patch_get_action:
            action = event_handler.on_item_selected(item=item1)
        patch_get_action.assert_called_once()


class TestInventoryDropHandler(unittest.TestCase):
    def test_on_item_selected(self):
        '''
        test that selecting an item will return a drop item action
        '''
        player = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        item1 = Item(name="item1", consumable=Consumable)
        player.inventory.items = [
            item1,
        ]
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=50, height=50)
        eng.game_map = gm
        player.parent = gm
        event_handler = InventoryDropHandler(engine=eng)
        action = event_handler.on_item_selected(item=item1)
        self.assertIsInstance(action, DropItem)

class TestSelectIndexHandler(unittest.TestCase):
    def test_init(self):
        '''
        test that the SelectIndexHandler is initialized correctly
        '''
        player = Actor(
            x=5, y=6,
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=player)
        e_handler = SelectIndexHandler(engine=eng)
        expected_location = player.x, player.y
        self.assertEqual(e_handler.engine.mouse_location, expected_location)

    def test_on_render(self):
        '''
        test that the tile at the mouse location is rendered black on white
        '''
        player = Actor(
            x=5, y=6,
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=10, height=10)
        eng.game_map = gm
        player.parent = gm
        e_handler = SelectIndexHandler(engine=eng)

        console = Console(width=10, height=10, order='F')

        e_handler.on_render(console=console)

        self.assertEqual(
            tcod.console_get_char_background(con=console, x=5, y=6),
            color.white
        )
        self.assertEqual(
            tcod.console_get_char_foreground(con=console, x=5, y=6),
            color.black
        )

    
    def test_ev_keydown_no_modifier(self):
        '''
        test that pressing no modifier keys will keep the modifier at 1
        '''
        player = Actor(
            x=5, y=5,
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=10, height=10)
        eng.game_map = gm
        player.parent = gm
        e_handler = SelectIndexHandler(engine=eng)
        # pressing up should move us ONE tile in the -y direction
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.UP, sym=tcod.event.K_UP, mod=tcod.event.Modifier.NONE)
        action = e_handler.ev_keydown(event=event)
        self.assertIsNone(action)
        self.assertEqual(eng.mouse_location, (5, 4))

    def test_ev_keydown_SHIFT_modifier(self):
        '''
        test that the LSHIFT and RSHIFT keys will change the modifier to 5
        '''
        player = Actor(
            x=5, y=5,
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=20, height=20)
        eng.game_map = gm
        player.parent = gm
        e_handler = SelectIndexHandler(engine=eng)
        # pressing down with LSHIFT should move us FIVE tiles in the +y direction
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.DOWN, 
            sym=tcod.event.K_DOWN, 
            mod=tcod.event.Modifier.LSHIFT
        )
        action = e_handler.ev_keydown(event=event)
        self.assertIsNone(action)
        self.assertEqual(eng.mouse_location, (5, 10))
        # pressing right with RSHIFT should move us FIVE tiles in the +x direction
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.RIGHT, 
            sym=tcod.event.K_RIGHT, 
            mod=tcod.event.Modifier.RSHIFT
        )
        action = e_handler.ev_keydown(event=event)
        self.assertIsNone(action)
        self.assertEqual(eng.mouse_location, (10, 10))

    def test_ev_keydown_CTRL_modifier(self):
        '''
        test that the LCTRL and RCTRL keys will change the modifier to 10
        '''
        player = Actor(
            x=5, y=5,
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=20, height=20)
        eng.game_map = gm
        player.parent = gm
        e_handler = SelectIndexHandler(engine=eng)
        # pressing down with LCTRL should move us TEN tiles in the +y direction
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.DOWN, 
            sym=tcod.event.K_DOWN, 
            mod=tcod.event.Modifier.LCTRL
        )
        action = e_handler.ev_keydown(event=event)
        self.assertIsNone(action)
        self.assertEqual(eng.mouse_location, (5, 15))
        # pressing right with RCTRL should move us TEN tiles in the +x direction
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.RIGHT, 
            sym=tcod.event.K_RIGHT, 
            mod=tcod.event.Modifier.RCTRL
        )
        action = e_handler.ev_keydown(event=event)
        self.assertIsNone(action)
        self.assertEqual(eng.mouse_location, (15, 15))

    def test_ev_keydown_ALT_modifier(self):
        '''
        test that the LALT and RALT keys will change the modifier to 20
        '''
        player = Actor(
            x=5, y=5,
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=30, height=30)
        eng.game_map = gm
        player.parent = gm
        e_handler = SelectIndexHandler(engine=eng)
        # pressing down with LALT should move us TWENTY tiles in the +y direction
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.DOWN, 
            sym=tcod.event.K_DOWN, 
            mod=tcod.event.Modifier.LALT
        )
        action = e_handler.ev_keydown(event=event)
        self.assertIsNone(action)
        self.assertEqual(eng.mouse_location, (5, 25))
        # pressing right with RALT should move us TWENTY tiles in the +x direction
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.RIGHT, 
            sym=tcod.event.K_RIGHT, 
            mod=tcod.event.Modifier.RALT
        )
        action = e_handler.ev_keydown(event=event)
        self.assertIsNone(action)
        self.assertEqual(eng.mouse_location, (25, 25))

    def test_ev_keydown_clamp_low(self):
        '''
        test that moving off the map too low will clamp back to 0,0
        '''
        player = Actor(
            x=1, y=1,
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=10, height=10)
        eng.game_map = gm
        player.parent = gm
        e_handler = SelectIndexHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.KP_7, 
            sym=tcod.event.K_KP_7, 
            mod=tcod.event.Modifier.RSHIFT
            )
        action = e_handler.ev_keydown(event=event)
        self.assertIsNone(action)
        self.assertEqual(eng.mouse_location, (0, 0))

    def test_ev_keydown_clamp_high(self):
        '''
        test that moving off the map too high will clamp back to the max game map corner
        '''
        player = Actor(
            x=8, y=8,
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=10, height=10)
        eng.game_map = gm
        player.parent = gm
        e_handler = SelectIndexHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.KP_3, 
            sym=tcod.event.K_KP_3, 
            mod=tcod.event.Modifier.LSHIFT
            )
        action = e_handler.ev_keydown(event=event)
        self.assertIsNone(action)
        self.assertEqual(eng.mouse_location, (9, 9))

    def test_ev_keydown_CONFIRM_KEYS(self):
        '''
        test that hitting a confirm key will return on_index_selected at the location
        '''
        player = Actor(
            x=1, y=1,
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=10, height=10)
        eng.game_map = gm
        player.parent = gm
        e_handler = SelectIndexHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.RETURN, 
            sym=tcod.event.K_RETURN, 
            mod=tcod.event.Modifier.NONE
            )
        with patch('input_handlers.SelectIndexHandler.on_index_selected') as patch_on_index_selected:
            patch_on_index_selected.return_value = None
            action = e_handler.ev_keydown(event=event)

        patch_on_index_selected.assert_called_once_with(1, 1)


    def test_ev_keydown_other_key(self):
        '''
        test that hitting a random key will call the ev_keydown function of the parent class
        '''
        player = Actor(
            x=1, y=1,
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=10, height=10)
        eng.game_map = gm
        player.parent = gm
        e_handler = SelectIndexHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.G, 
            sym=tcod.event.K_g, 
            mod=tcod.event.Modifier.NONE
            )
        with patch('input_handlers.AskUserEventHandler.ev_keydown') as patch_ev_keydown:
            action = e_handler.ev_keydown(event=event)

        patch_ev_keydown.assert_called_once_with(event)

    def test_ev_mousebuttondown_good_click(self):
        '''
        test that a left click on a tile in bounds will call on_index_selected
        '''

    def test_ev_mousebuttondown_out_of_bounds(self):
        '''
        test that clicking out of bounds will return the mousebuttonevent of the parent class
        '''

    def test_ev_mousebuttondown_right_click(self):
        '''
        test that a right click in bounds will return the mousebutton event of the parent
        '''

if __name__ == '__main__':
    unittest.main()
