from engine import Engine
import unittest

from entity import Entity
from input_handlers import EventHandler


class Test_Engine(unittest.TestCase):
    def test_init(self):
        ent1 = Entity(0, 0, "@", (0, 0, 0))
        ent2 = Entity(10, 10, "k", (255, 255, 255))
        ents = {ent1, ent2}
        event_handler = EventHandler()
        eng = Engine(ents, event_handler, ent1)
        self.assertIn(ent1, eng.entities)
        self.assertIn(ent2, eng.entities)
        self.assertEqual(eng.event_handler, event_handler)
        self.assertEqual(eng.player, ent1)
