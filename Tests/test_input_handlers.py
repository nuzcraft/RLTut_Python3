from multiprocessing import Event
import unittest
from unittest.mock import patch
import tcod.event
from input_handlers import EventHandler, MainGameEventHandler, GameOverEventHandler, HistoryViewer

from actions import EscapeAction, BumpAction, WaitAction
from engine import Engine
from entity import Entity
from game_map import GameMap


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
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, EscapeAction)

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
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, EscapeAction)

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


if __name__ == '__main__':
    unittest.main()
