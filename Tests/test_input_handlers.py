import input_handlers
import unittest
import tcod.event

from actions import Action, EscapeAction, MovementAction


class Test_Input_Handlers(unittest.TestCase):
    def test_ev_keydown_up(self):
        event_handler = input_handlers.EventHandler()
        event = tcod.event.K_UP
        self.assertEqual(
            event_handler.dispatch(event), MovementAction)


if __name__ == '__main__':
    unittest.main()
