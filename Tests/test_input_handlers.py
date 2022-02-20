import input_handlers
import unittest
import tcod.event

from actions import EscapeAction, MovementAction


class Test_Input_Handlers(unittest.TestCase):
    # ev_quit will only trigger on tcod.event.Quit() events, no need to negative test
    def test_ev_quit(self):
        # TODO: the assertEquals seems like it might be wrong (but its working)
        # seems like the exception code should be 1, not none
        '''
        tests that the a quit action will raise an exception
        '''
        event_handler = input_handlers.EventHandler()
        event = tcod.event.Quit()
        with self.assertRaises(SystemExit) as action:
            event_handler.dispatch(event)
        self.assertEqual(action.exception.code, None)

    # tcod.event.KeyDown() events will trigger ev_keydown
    def test_ev_keydown_up(self):
        '''
        tests that pressing up will move the player up
        '''
        event_handler = input_handlers.EventHandler()
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.UP, sym=tcod.event.K_UP, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, MovementAction)
        self.assertEqual(action.dx, 0)
        self.assertEqual(action.dy, -1)

    def test_ev_keydown_down(self):
        '''
        tests that pressing down will move the player down
        '''
        event_handler = input_handlers.EventHandler()
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.DOWN, sym=tcod.event.K_DOWN, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, MovementAction)
        self.assertEqual(action.dx, 0)
        self.assertEqual(action.dy, 1)

    def test_ev_keydown_left(self):
        '''
        tests that pressing left will move the player left
        '''
        event_handler = input_handlers.EventHandler()
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.LEFT, sym=tcod.event.K_LEFT, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, MovementAction)
        self.assertEqual(action.dx, -1)
        self.assertEqual(action.dy, 0)

    def test_ev_keydown_right(self):
        '''
        tests that pressing right will move the player right
        '''
        event_handler = input_handlers.EventHandler()
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.RIGHT, sym=tcod.event.K_RIGHT, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, MovementAction)
        self.assertEqual(action.dx, 1)
        self.assertEqual(action.dy, 0)

    def test_ev_keydown_escape(self):
        '''
        tests that pressing escape results in an EscapeAction
        '''
        event_handler = input_handlers.EventHandler()
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.ESCAPE, sym=tcod.event.K_ESCAPE, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsInstance(action, EscapeAction)

    # using the HOME button as an unassigned button
    def test_ev_keydown_other(self):
        '''
        tests that pressing an unassigned button will do nothing
        '''
        event_handler = input_handlers.EventHandler()
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.HOME, sym=tcod.event.K_HOME, mod=tcod.event.Modifier.NONE)
        action = event_handler.dispatch(event)
        self.assertIsNone(action)


if __name__ == '__main__':
    unittest.main()
