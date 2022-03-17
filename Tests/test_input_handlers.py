import unittest
import tcod.event
from input_handlers import EventHandler

from actions import EscapeAction, BumpAction, WaitAction
from engine import Engine
from entity import Entity

# TODO: rewrite all of these once new engine code is in place


class Test_Input_Handlers(unittest.TestCase):
    def test_init(self):
        '''
        test that initializing the event handler sets correctly
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = EventHandler(engine=eng)
        self.assertEqual(event_handler.engine, eng)

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

    # tcod.event.KeyDown() events will trigger ev_keydown
    def test_ev_keydown_up(self):
        '''
        tests that pressing up will move the player up
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
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
        event_handler = EventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.ESCAPE, sym=tcod.event.K_ESCAPE, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, EscapeAction)

    # using the HOME button as an unassigned button
    def test_ev_keydown_other(self):
        '''
        tests that pressing an unassigned button will do nothing
        '''
        ent = Entity()
        eng = Engine(player=ent)
        event_handler = EventHandler(engine=eng)
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.BACKSLASH, sym=tcod.event.K_BACKSLASH, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsNone(action)


if __name__ == '__main__':
    unittest.main()
