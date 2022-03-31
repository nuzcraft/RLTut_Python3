import math
from entity import Entity, Actor, Item
from game_map import GameMap
from engine import Engine
from render_order import RenderOrder

from components.ai import BaseAI
from components.fighter import Fighter
from components.consumable import Consumable
from components.inventory import Inventory

import unittest


class Test_Entity(unittest.TestCase):
    def test_init_no_gamemap(self):
        '''
        tests initializing a new entity assigns values correctly
        '''
        x_val = 1
        y_val = 2
        char = '@'
        color = [100, 100, 100]
        name = 'nuzcraft'
        blocks_movement = True
        ent = Entity(
            x=x_val,
            y=y_val,
            char=char,
            color=color,
            name=name,
            blocks_movement=blocks_movement,
        )
        self.assertEqual(ent.x, x_val)
        self.assertEqual(ent.y, y_val)
        self.assertEqual(ent.char, char)
        self.assertEqual(ent.color, color)
        self.assertEqual(ent.name, name)
        self.assertEqual(ent.blocks_movement, blocks_movement)
        self.assertEqual(ent.render_order, RenderOrder.CORPSE)

    def test_init_with_parent(self):
        '''
        tests that creating an entity with a parent will
        set the parent gamemap and add the entity to it
        '''
        player = Entity()
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=10, height=10)
        ent = Entity(parent=gm)
        self.assertEqual(ent.parent, gm)
        # make sure the entity gets added to the gamemap
        self.assertIn(ent, ent.parent.entities)

    def test_property_gamemap(self):
        '''
        test that the gamemap property will return
        the parent
        '''
        player = Entity()
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=10, height=10)
        player.parent = gm
        self.assertEqual(player.gamemap, gm)

    def test_spawn(self):
        '''
        tests that spawn will copy the entity
        '''
        player = Entity()
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=10, height=10)
        ent = Entity(name="test")
        ent.spawn(gm, 5, 5)
        # check that entities is filled with something
        self.assertTrue(gm.entities)
        # pull the entity out, make sure it matches as expected
        ents = gm.entities
        ent2 = list(ents)[0]
        self.assertEqual(ent2.name, "test")
        self.assertEqual(ent2.x, 5)
        self.assertEqual(ent2.y, 5)

    def test_place_no_gamemap(self):
        '''
        place the entity at a new location
        do not switch game maps
        '''
        ent = Entity()
        ent.place(x=10, y=10)
        self.assertEqual(ent.x, 10)
        self.assertEqual(ent.y, 10)

    def test_place_with_parent(self):
        '''
        place the entity at a new location in a new
        game map
        '''
        player = Entity()
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=10, height=10)
        gm2 = GameMap(engine=eng, width=10, height=10)
        ent = Entity(parent=gm)
        # place the entity at a new gamemap with a new location
        ent.place(x=10, y=10, gamemap=gm2)
        self.assertEqual(ent.x, 10)
        self.assertEqual(ent.y, 10)
        self.assertEqual(ent.parent, gm2)
        # make sure the entity gets removed from the old entity list
        # and added to the new one
        self.assertNotIn(ent, gm.entities)
        self.assertIn(ent, gm2.entities)

    def test_distance(self):
        '''
        test that the distance function returns as expected
        '''
        ent = Entity()
        dist = ent.distance(x=5, y=7)
        expected = math.sqrt((5-0)**2 + (7-0)**2)
        self.assertEqual(dist, expected)

    def test_move(self):
        '''
        tests moving an entity
        '''
        x_val = 1
        y_val = 2
        dx = 1
        dy = 2
        ent = Entity(x=x_val, y=y_val)
        ent.move(dx, dy)
        self.assertEqual(ent.x, x_val + dx)
        self.assertEqual(ent.y, y_val + dy)


class TestActor(unittest.TestCase):
    def test_init(self):
        '''
        test that initializing an actor sets the values as expected
        '''
        actor = Actor(ai_cls=BaseAI, fighter=Fighter(10, 10, 10), inventory=Inventory(capacity=5))
        # some of these are defaults
        self.assertEqual(actor.x, 0)
        self.assertEqual(actor.y, 0)
        self.assertEqual(actor.char, "?")
        self.assertEqual(actor.color, (255, 255, 255))
        self.assertEqual(actor.name, "<Unnamed>")
        self.assertEqual(actor.blocks_movement, True)
        self.assertEqual(actor.render_order, RenderOrder.ACTOR)
        # ai and fighter components reference the entity, need an extra check
        self.assertIsInstance(actor.ai, BaseAI)
        self.assertEqual(actor, actor.ai.entity)
        self.assertIsInstance(actor.fighter, Fighter)
        self.assertEqual(actor, actor.fighter.parent)
        self.assertIsInstance(actor.inventory, Inventory)
        self.assertEqual(actor, actor.inventory.parent)

    def test_property_is_alive_true(self):
        '''
        test the is_alive property returns true if there is an ai component
        '''
        actor = Actor(ai_cls=BaseAI, fighter=Fighter(10, 10, 10), inventory=Inventory(capacity=5))
        self.assertTrue(actor.is_alive)

    def test_property_is_alive_false(self):
        '''
        test the is_alive property returns false if there is no
        '''
        actor = Actor(ai_cls=BaseAI, fighter=Fighter(10, 10, 10), inventory=Inventory(capacity=5))
        actor.ai = None  # remove the ai component
        self.assertFalse(actor.is_alive)

class TestItem(unittest.TestCase):
    def test_init(self):
        '''
        test that items can get initialized without issues
        '''
        cm = Consumable()
        itm = Item(consumable=cm)
        self.assertEqual(itm.x, 0)
        self.assertEqual(itm.y, 0)
        self.assertEqual(itm.char, '?')
        self.assertEqual(itm.color, (255, 255, 255))
        self.assertEqual(itm.name, '<Unnamed>')
        self.assertIsInstance(itm.consumable, Consumable)
        self.assertEqual(itm.consumable.parent, itm)
        self.assertFalse(itm.blocks_movement)
        self.assertEqual(itm.render_order, RenderOrder.ITEM)