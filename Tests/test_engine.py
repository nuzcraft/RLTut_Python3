from engine import Engine
import unittest
import tcod.event

from entity import Entity
from input_handlers import EventHandler


class Test_Engine(unittest.TestCase):
    def test_init(self):
        '''
        tests that instantiating the engine will set values correctly
        '''
        ent1 = Entity(0, 0, "@", (0, 0, 0))
        ent2 = Entity(10, 10, "k", (255, 255, 255))
        ents = {ent1, ent2}
        event_handler = EventHandler()
        eng = Engine(ents, event_handler, ent1)
        self.assertIn(ent1, eng.entities)
        self.assertIn(ent2, eng.entities)
        self.assertEqual(eng.event_handler, event_handler)
        self.assertEqual(eng.player, ent1)

    def test_handle_events_MovementAction(self):
        '''
        tests that 2 basic movement actions will move the player object in the engine
        '''
        x_val = 0
        y_val = 0
        ent1 = Entity(x_val, y_val, "@", (0, 0, 0))
        event_handler = EventHandler()
        event1 = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.UP, sym=tcod.event.K_UP, mod=tcod.event.Modifier.NONE)
        event2 = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.LEFT, sym=tcod.event.K_LEFT, mod=tcod.event.Modifier.NONE)
        eng = Engine({}, event_handler, ent1)
        eng.handle_events({event1, event2})
        self.assertNotEqual(eng.player.x, x_val)
        self.assertNotEqual(eng.player.y, y_val)

    def test_handle_events_EscapeAction(self):
        '''
        test that an escape action will raise a system exit
        similar to test_ev_quit, I'm not sure this is working as expected :)
        '''
        ent1 = Entity(0, 0, "@", (0, 0, 0))
        event_handler = EventHandler()
        event1 = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.ESCAPE, sym=tcod.event.K_ESCAPE, mod=tcod.event.Modifier.NONE)
        eng = Engine({}, event_handler, ent1)
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
        eng = Engine({}, event_handler, ent1)
        # the below function will fail if an escape action is passed
        # the assertEquals will fail if a movement action is passed in
        eng.handle_events({event1})
        self.assertEqual(eng.player.x, x_val)
        self.assertEqual(eng.player.y, y_val)
