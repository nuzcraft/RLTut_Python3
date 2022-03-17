import unittest
from game_map import GameMap
from entity import Entity, Actor
from engine import Engine
from components.ai import HostileEnemy
from components.fighter import Fighter


class Test_Game_Map(unittest.TestCase):
    def test_init(self):
        '''
        tests instantiating a new GameMap
        '''
        player = Entity()
        eng = Engine(player=player)
        ent1 = Entity(x=10, y=10, char="@", color=(100, 100, 100))
        ent2 = Entity(x=20, y=20, char="k", color=(200, 200, 200))
        gm = GameMap(engine=eng, width=50, height=60, entities={ent1, ent2})
        self.assertEqual(gm.engine, eng)
        self.assertEqual(gm.width, 50)
        self.assertEqual(gm.height, 60)
        # check that tiles were generated okay
        tiles_shape = gm.tiles.shape
        self.assertEqual(tiles_shape[0], 50)
        self.assertEqual(tiles_shape[1], 60)
        # check that the visible and explored arrays were generated okay as well
        visible_shape = gm.visible.shape
        self.assertEqual(visible_shape[0], 50)
        self.assertEqual(visible_shape[1], 60)
        explored_shape = gm.explored.shape
        self.assertEqual(explored_shape[0], 50)
        self.assertEqual(explored_shape[1], 60)
        # check that the entities set was created
        self.assertIn(ent1, gm.entities)
        self.assertIn(ent2, gm.entities)

    def test_property_actors(self):
        '''
        test that the actors property will return the correct entities
        '''
        player = Entity()
        eng = Engine(player=player)
        ent1 = Entity()
        act2 = Actor(ai_cls=HostileEnemy, fighter=Fighter)
        act3 = Actor(ai_cls=HostileEnemy, fighter=Fighter)
        act3.ai = None
        gm = GameMap(engine=eng, width=50, height=60)
        gm.entities = {ent1, act2, act3}
        actors = gm.actors
        # verify that only one of the entities made it into the actors list
        # act2 is the only 'actor' tha has an ai component
        self.assertEqual(len(list(actors)), 1)

    def test_get_blocking_entity_at_location_true(self):
        '''
        tests whether a blocking entity returns when checking
        '''
        ent = Entity(x=5, y=5, blocks_movement=True)
        eng = Engine(player=ent)
        gm = GameMap(engine=eng, width=10, height=10, entities={ent})
        ent2 = gm.get_blocking_entity_at_location(5, 5)
        self.assertEqual(ent, ent2)

    def test_get_blocking_entity_at_location_false(self):
        '''
        tests whether a blocking entity returns when checking
        '''
        ent = Entity(x=5, y=5, blocks_movement=False)
        eng = Engine(player=ent)
        gm = GameMap(engine=eng, width=10, height=10, entities={ent})
        ent2 = gm.get_blocking_entity_at_location(5, 5)
        self.assertIsNone(ent2)

    def test_in_bounds_both_in(self):
        '''
        tests whether x and y in bounds of map returns true
        '''
        ent = Entity()
        eng = Engine(player=ent)
        x, y = 25, 25
        gm = GameMap(engine=eng, width=50, height=50)
        self.assertTrue(gm.in_bounds(x, y))

    def test_in_bounds_both_out_low(self):
        '''
        tests whether x and y both out of bounds with low values returns false
        '''
        ent = Entity()
        eng = Engine(player=ent)
        x, y = -1, -1
        gm = GameMap(engine=eng, width=50, height=50)
        self.assertFalse(gm.in_bounds(x, y))

    def test_in_bounds_both_out_high(self):
        '''
        tests whether x and y both out of bounds high values returns false
        '''
        ent = Entity()
        eng = Engine(player=ent)
        x, y = 100, 100
        gm = GameMap(engine=eng, width=50, height=50)
        self.assertFalse(gm.in_bounds(x, y))

    def test_in_bounds_x_in_y_out(self):
        '''
        tests x in bounds, y out of bounds returns false
        '''
        ent = Entity()
        eng = Engine(player=ent)
        x, y = 25, 100
        gm = GameMap(engine=eng, width=50, height=50)
        self.assertFalse(gm.in_bounds(x, y))

    def test_in_bounds_x_out_y_in(self):
        '''
        tests x out of bounds, y in bounds returns false
        '''
        ent = Entity()
        eng = Engine(player=ent)
        x, y = -25, 25
        gm = GameMap(engine=eng, width=50, height=50)
        self.assertFalse(gm.in_bounds(x, y))

    # def test_render(self):
    #     '''
    #     tests that on render the console matches the GameMap
    #     removing this test until there's something easier to test
    #     '''
    #     gm = GameMap(50, 50)
    #     console = tcod.Console(50, 50)
    #     gm.render(console)
    #     # let's check the specific locations in console to make
    #     # sure they match the game map
    #     self.assertEqual(console.tiles_rgb[29, 22], gm.tiles[29, 22]["dark"])
    #     self.assertEqual(console.tiles_rgb[30, 22], gm.tiles[30, 22]["dark"])

    def test_get_actor_at_location_with_actor(self):
        '''
        tests that checking a location with an actor
        will return that actor
        '''
        act = Actor(x=5, y=6, ai_cls=HostileEnemy, fighter=Fighter(hp=10, defense=10, power=10))
        eng = Engine(player=act)
        gm = GameMap(engine=eng, width=10, height=10, entities={act})
        act.gamemap = gm
        eng.game_map = gm

        returned_act = gm.get_actor_at_location(x=5, y=6)
        self.assertEqual(act, returned_act)

    def test_get_actor_at_location_empty(self):
        '''
        tests that checking a location with an actor
        will return that actor
        '''
        act = Actor(x=5, y=6, ai_cls=HostileEnemy, fighter=Fighter(hp=10, defense=10, power=10))
        eng = Engine(player=act)
        gm = GameMap(engine=eng, width=10, height=10, entities={act})
        act.gamemap = gm
        eng.game_map = gm
        # check an empty location
        returned_act = gm.get_actor_at_location(x=6, y=7)
        self.assertIsNone(returned_act)
