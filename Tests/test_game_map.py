import unittest
from unittest.mock import patch
from game_map import GameMap, GameWorld
from entity import Entity, Actor, Item
from engine import Engine
from components.ai import HostileEnemy
from components.fighter import Fighter
from components.inventory import Inventory
from components.consumable import Consumable
from components.level import Level


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
        # check that the downstairs location was set
        self.assertEqual(gm.downstairs_location, (0, 0))

    def test_property_gamemap(self):
        '''
        test that the gamemap property returns the self
        '''
        player = Entity()
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=10, height=10)
        self.assertEqual(gm, gm.gamemap)

    def test_property_actors(self):
        '''
        test that the actors property will return the correct entities
        '''
        player = Entity()
        eng = Engine(player=player)
        ent1 = Entity()
        act2 = Actor(ai_cls=HostileEnemy, fighter=Fighter,
                     inventory=Inventory(capacity=5),
                     level=Level())
        act3 = Actor(ai_cls=HostileEnemy, fighter=Fighter,
                     inventory=Inventory(capacity=5),
                     level=Level())
        act3.ai = None
        gm = GameMap(engine=eng, width=50, height=60)
        gm.entities = {ent1, act2, act3}
        actors = gm.actors
        # verify that only one of the entities made it into the actors list
        # act2 is the only 'actor' tha has an ai component
        self.assertEqual(len(list(actors)), 1)

    def test_property_items(self):
        '''
        test that items will property return the correct entities
        '''
        player = Entity()
        eng = Engine(player=player)
        ent1 = Entity()
        act2 = Actor(ai_cls=HostileEnemy, fighter=Fighter,
                     inventory=Inventory(capacity=5),
                     level=Level())
        itm3 = Item(consumable=Consumable())
        gm = GameMap(engine=eng, width=50, height=60)
        gm.entities = {ent1, act2, itm3}
        items = gm.items
        # verify that only one of the entities made it into the items list
        # itm3 is the only item
        self.assertEqual(len(list(items)), 1)

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
        act = Actor(x=5, y=6, ai_cls=HostileEnemy,
                    fighter=Fighter(hp=10, defense=10, power=10), inventory=Inventory(capacity=5),
                    level=Level())
        eng = Engine(player=act)
        gm = GameMap(engine=eng, width=10, height=10, entities={act})
        act.parent = gm
        eng.game_map = gm

        returned_act = gm.get_actor_at_location(x=5, y=6)
        self.assertEqual(act, returned_act)

    def test_get_actor_at_location_empty(self):
        '''
        tests that checking a location with an actor
        will return that actor
        '''
        act = Actor(x=5, y=6, ai_cls=HostileEnemy,
                    fighter=Fighter(hp=10, defense=10, power=10), inventory=Inventory(capacity=5),
                    level=Level())
        eng = Engine(player=act)
        gm = GameMap(engine=eng, width=10, height=10, entities={act})
        act.parent = gm
        eng.game_map = gm
        # check an empty location
        returned_act = gm.get_actor_at_location(x=6, y=7)
        self.assertIsNone(returned_act)


class TestGameWorld(unittest.TestCase):
    def test_init(self):
        '''
        test that a gameworld can be initialized correctly
        '''
        eng = Engine(player=Entity())
        mw, mh = 10, 11
        mr = 6
        rmin, rmax = 3, 4
        mm, mi = 1, 2
        cf = 5
        gw = GameWorld(
            engine=eng,
            map_width=mw,
            map_height=mh,
            max_rooms=mr,
            room_min_size=rmin,
            room_max_size=rmax,
            max_monsters_per_room=mm,
            max_items_per_room=mi,
            current_floor=cf
        )
        self.assertEqual(gw.engine, eng)
        self.assertEqual(gw.map_width, mw)
        self.assertEqual(gw.map_height, mh)
        self.assertEqual(gw.max_rooms, mr)
        self.assertEqual(gw.room_min_size, rmin)
        self.assertEqual(gw.room_max_size, rmax)
        self.assertEqual(gw.max_monsters_per_room, mm)
        self.assertEqual(gw.max_items_per_room, mi)
        self.assertEqual(gw.current_floor, cf)

    def test_generate_floor(self):
        '''
        test that generating a floor will increment the current floor
        and call generate_dungeon
        '''
        gw = GameWorld(
            engine=Engine(player=Entity()),
            map_width=10,
            map_height=10,
            max_rooms=10,
            room_min_size=3,
            room_max_size=6,
            max_monsters_per_room=2,
            max_items_per_room=2
        )
        with patch('procgen.generate_dungeon') as patch_gen_dun:
            gw.generate_floor()

        self.assertEqual(gw.current_floor, 1)
        patch_gen_dun.assert_called()
