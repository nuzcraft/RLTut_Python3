import unittest
from typing import List, Tuple

from numpy import power

from components.ai import BaseAI, HostileEnemy
from components.fighter import Fighter
from entity import Entity, Actor
from game_map import GameMap
from engine import Engine
import tile_types


class Test_BaseAI(unittest.TestCase):
    def test_entity_set(self):
        '''
        tests that the entity can be set correctly
        '''
        actor = Actor(ai_cls=BaseAI, fighter=Fighter(
            hp=10, defense=10, power=10))
        self.assertEqual(actor, actor.ai.entity)

        ai = BaseAI(actor)
        ai.entity = actor
        self.assertEqual(actor, ai.entity)

    def test_perform(self):
        '''
        all perform of this AI will be handled
        elsewhere
        '''
        ent = Entity()
        ai = BaseAI(entity=ent)
        with self.assertRaises(NotImplementedError):
            ai.perform()

    def test_get_path_to_straight_line(self):
        '''
        test get_path_to function
        1. test that it returns a short path in a straight line
        '''
        ent = Entity(x=0, y=0)
        eng = Engine(player=ent)
        gm = GameMap(engine=eng, width=10, height=10)
        # GameMaps are initialized as all wall, convert to floor
        gm.tiles[:, :] = tile_types.floor
        ent.gamemap = gm
        ai = BaseAI(entity=ent)
        #  ent starts at 0,0 - get the path straight down to 0,9 (bottom of map)
        path = ai.get_path_to(dest_x=0, dest_y=9)
        # path should be...
        # (0,1)...(0,9)
        path_should_be: List[Tuple[int, int]] = [
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9)]
        self.assertEqual(path, path_should_be)

    def test_get_path_to_avoid_wall(self):
        '''
        test get_path_to function
        2. test that it avoids walls
        '''
        ent = Entity(x=0, y=0)
        eng = Engine(player=ent)
        gm = GameMap(engine=eng, width=10, height=10)
        # GameMaps are initialized as all wall, convert to floor
        gm.tiles[:, :] = tile_types.floor
        # change a couple of the path tiles to a wall (unwalkable)
        gm.tiles[0, 5] = tile_types.wall
        gm.tiles[1, 5] = tile_types.wall
        ent.gamemap = gm
        ai = BaseAI(entity=ent)
        #  ent starts at 0,0 - get the path straight down to 0,9 (bottom of map)
        path = ai.get_path_to(dest_x=0, dest_y=9)
        # straight path should be (0,1)...(0,9)
        # but since (0,5) and (1, 5) are unwalkable,
        # the path increases to go around them (diagonal to (1,4) and (2,5) then
        # back to (1,6) before straightening out)
        path_should_be: List[Tuple[int, int]] = [
            (0, 1), (0, 2), (0, 3), (1, 4), (2, 5), (1, 6), (0, 7), (0, 8), (0, 9)]
        self.assertEqual(path, path_should_be)

    def test_get_path_to_avoid_entities(self):
        '''
        test get_path_to function
        3. test that it avoids blocking entities
        '''
        ent = Entity(x=0, y=0)
        eng = Engine(player=ent)
        gm = GameMap(engine=eng, width=10, height=10)
        # GameMaps are initialized as all wall, convert to floor
        gm.tiles[:, :] = tile_types.floor
        # add a couple entities to the gamemap that are in the way
        ent1 = Entity(x=0, y=5, blocks_movement=True)
        ent2 = Entity(x=1, y=5, blocks_movement=True)
        gm.entities = {ent1, ent2}
        ent.gamemap = gm
        ai = BaseAI(entity=ent)
        #  ent starts at 0,0 - get the path straight down to 0,9 (bottom of map)
        path = ai.get_path_to(dest_x=0, dest_y=9)
        # straight path should be (0,1)...(0,9)
        # but since (0,5) and (1, 5) have blocking entities,
        # the path increases to go around them (diagonal to (1,4) and (2,5) then
        # back to (1,6) before straightening out)
        path_should_be: List[Tuple[int, int]] = [
            (0, 1), (0, 2), (0, 3), (1, 4), (2, 5), (1, 6), (0, 7), (0, 8), (0, 9)]
        self.assertEqual(path, path_should_be)


class TestHostileEnemy(unittest.TestCase):
    def test_init(self):
        '''
        test that the hostile enemy class can be initialized without issues
        '''
        # instantiating an actor will automatically instantiate the ai class under actor.ai
        actor = Actor(ai_cls=HostileEnemy, fighter=Fighter(
            hp=10, defense=10, power=10))
        self.assertEqual(actor, actor.ai.entity)
        self.assertEqual([], actor.ai.path)
