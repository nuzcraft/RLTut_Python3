import unittest
from components.base_component import BaseComponent
from entity import Entity
from engine import Engine
from game_map import GameMap


class Test_BaseComponent(unittest.TestCase):
    def test_property_gamemap(self):
        '''
        tests that the gamemap property returns
        correctly
        '''
        base_component = BaseComponent()
        ent = Entity()
        eng = Engine(player=ent)
        gm = GameMap(engine=eng, width=10, height=10)
        ent.parent = gm
        base_component.parent = ent
        self.assertEqual(base_component.gamemap, gm)

    def test_property_engine(self):
        '''
        tests that the engine property returns
        correctly
        '''
        base_component = BaseComponent()
        ent = Entity()
        eng = Engine(player=ent)
        gm = GameMap(engine=eng, width=10, height=10)
        ent.parent = gm
        base_component.parent = ent
        self.assertEqual(base_component.engine, eng)
