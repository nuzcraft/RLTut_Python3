from entity import Entity
import unittest


class Test_Entity(unittest.TestCase):
    def test_init(self):
        x_val = 1
        y_val = 2
        char = '@'
        color = [100, 100, 100]
        ent = Entity(x_val, y_val, char, color)
        self.assertEqual(ent.x, x_val)
        self.assertEqual(ent.y, y_val)
        self.assertEqual(ent.char, char)
        self.assertEqual(ent.color, color)

    def test_move(self):
        x_val = 1
        y_val = 2
        char = '@'
        color = [100, 100, 100]
        dx = 1
        dy = 2
        ent = Entity(x_val, y_val, char, color)
        ent.move(dx, dy)
        self.assertEqual(ent.x, x_val + dx)
        self.assertEqual(ent.y, y_val + dy)
